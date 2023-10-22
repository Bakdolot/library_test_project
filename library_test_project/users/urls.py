from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from library_test_project.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", UserViewSet)

urlpatterns = router.urls
