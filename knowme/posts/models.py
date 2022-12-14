from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone




# TODO: add a function for tagging other users to the model
from knowme.accounts.models import Profile
from knowme.posts.utils.validators import validate_file_size


class Post(models.Model):
    MAX_LEN_DESCRIPTION = 49
    MAX_LEN_LOCATION = 30

    photo = models.ImageField(
        validators=[validate_file_size],
        upload_to='posts',
    )
    description = models.CharField(
        max_length=MAX_LEN_DESCRIPTION,
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=MAX_LEN_LOCATION,
        null=True,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    publish_date = models.DateTimeField(
        default=timezone.now
    )


class Report(models.Model):
    MAX_LEN_TEXT = 300

    text = models.TextField(
        max_length=MAX_LEN_TEXT
    )

    to_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
