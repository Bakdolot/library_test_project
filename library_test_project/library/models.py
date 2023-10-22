from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from library_test_project.users.models import ScoreAbs

User = get_user_model()


class Author(models.Model):
    name = models.CharField(_("Name of author"), max_length=255)


class Genre(models.Model):
    name = models.CharField(_("Name of genre"), max_length=255)


class Book(ScoreAbs, models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", verbose_name=_("author"))
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre", verbose_name=_("genre"))
    name = models.CharField(_("Name of book"), max_length=255)
    description = models.TextField(_("Description"))
    published_date = models.DateTimeField(_("Published date"), auto_now_add=True)
    scored_users = models.ManyToManyField(User, through="BookScoredUsers")


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Owner"))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Book"))
    text = models.TextField(_("Text"))
    created_at = models.DateTimeField(_("Date of creation"), auto_now_add=True)


class UserFavoriteBooks(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")

    class Meta:
        unique_together = ["book", "user"]


class BookScoredUsers(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = ["book", "user"]
