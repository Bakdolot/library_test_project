from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers

from .models import Author, Book, BookScoredUsers, Comment, Genre, UserFavoriteBooks

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    author = AuthorSerializer()
    is_favorite = serializers.BooleanField()

    class Meta:
        model = Book
        fields = ["name", "score", "genre", "author", "is_favorite"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BookDetailSerializer(BookListSerializer):
    genre = GenreSerializer()
    author = AuthorSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Book
        fields = ["name", "score", "description", "published_date", "genre", "author", "comments"]


class AddFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteBooks
        fields = "__all__"


class AddBookScoreSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(max_value=10, min_value=1)

    class Meta:
        model = BookScoredUsers
        fields = "__all__"

    def create(self, validated_data: Any) -> Any:
        instance = super().create(validated_data)
        Book.objects.filter(pk=instance.book.pk).update(
            score_sum=F("score_sum") + instance.score, score_count=F("score_count") + 1
        )
        return instance
