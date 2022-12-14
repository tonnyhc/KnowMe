from django.db import models

from knowme.accounts.models import Profile


class Message(models.Model):
    MAX_LEN_TEXT = 1000

    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='from_profile',
    )

    recipient = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='to_profile',
    )
    text = models.TextField(
        max_length=MAX_LEN_TEXT,
        blank=True,
        null=True,
    )
    date = models.DateTimeField(
        auto_now=True,
    )
    is_read = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['date']
