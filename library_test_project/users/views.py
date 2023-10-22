from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from library_test_project.utils import is_valid_uuid

from .serializers import RegisterSerializer, UserSerializer
from .tasks import send_mail_task

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "register":
            return RegisterSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(["POST"], detail=False)
    def register(self, request: HttpRequest):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if settings.VERIFICATION:
            redirect_url = (
                request.get_host()
                + f"/api/users/{instance.pk}/verification/?register_code={str(instance.register_code)}"
            )
            send_mail_task.delay("Registration verification", redirect_url, instance.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(["GET"], detail=True)
    def verification(self, request: HttpRequest, pk):
        register_code = request.GET.get("register_code")
        if register_code is None or not is_valid_uuid(register_code):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(pk=pk, register_code=register_code)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.update(is_active=True)
        return Response(status=status.HTTP_202_ACCEPTED)
