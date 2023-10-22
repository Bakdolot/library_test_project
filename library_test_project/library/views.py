from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .filters import BookListFilter
from .models import Book, UserFavoriteBooks
from .serializers import (
    AddBookScoreSerializer,
    AddFavoriteSerializer,
    BookDetailSerializer,
    BookListSerializer,
    CommentSerializer,
)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related("author", "genre")
    serializer_class = BookListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookListFilter

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        is_favorite = UserFavoriteBooks.objects.filter(book=OuterRef("pk"), user=user)
        return super().get_queryset().annotate(is_favorite=Exists(is_favorite))


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related("author", "genre").prefetch_related("comments")
    serializer_class = BookDetailSerializer


class AddFavoriteView(generics.CreateAPIView):
    serializer_class = AddFavoriteSerializer
    permission_classes = [IsAuthenticated]


class DeleteFavoriteView(generics.DestroyAPIView):
    queryset = UserFavoriteBooks.objects
    permission_classes = [IsAuthenticated]


class AddBookScoreView(generics.CreateAPIView):
    serializer_class = AddBookScoreSerializer
    permission_classes = [IsAuthenticated]


class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
