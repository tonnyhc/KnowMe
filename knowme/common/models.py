from django.db import models

from knowme.accounts.models import Profile
from knowme.posts.models import Post


class Comment(models.Model):
    MAX_LEN_TEXT = 50

    text = models.CharField(
        max_length=MAX_LEN_TEXT,
        null=False,
        blank=False,
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    to_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    publish_date = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.text


class CommentReport(models.Model):
    MAX_LEN_TEXT = 300

    text = models.TextField(
        max_length=MAX_LEN_TEXT
    )
    to_comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )


class Like(models.Model):
    to_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    to_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    publish_date = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-publish_date']


class SavePost(models.Model):
    to_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    to_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    save_date = models.DateField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-save_date']


class Followers(models.Model):
    profile = models.ForeignKey(
        Profile,
        related_name='following',
        on_delete=models.CASCADE
    )
    following_profile = models.ForeignKey(
        Profile,
        related_name='followers',
        on_delete=models.CASCADE
    )
    follow_date = models.DateField(
        auto_now=True,
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile_id', 'following_profile_id'], name="unique_followers")
        ]

        ordering = ["-follow_date"]
