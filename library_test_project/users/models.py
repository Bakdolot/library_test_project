from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from library_test_project.users.managers import UserManager


class ScoreAbs(models.Model):
    score_sum = models.PositiveBigIntegerField(_("Score sum"), default=0)
    score_count = models.PositiveIntegerField(_("Score count"), default=0)

    @property
    def score(self):
        if not self.score_sum or not self.score_count:
            return 0
        return round(self.score_sum / self.score_count, 2)

    class Meta:
        abstract = True


class User(AbstractUser, ScoreAbs):
    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    register_code = models.UUIDField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
