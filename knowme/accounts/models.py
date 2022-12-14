from django.db import models

from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.datetime_safe import datetime

from knowme.accounts.utils.mixins import ChoicesEnumMixin
from knowme.posts.utils.validators import validate_file_size


class KnowMeUser(AbstractBaseUser, PermissionsMixin):
    MAX_LEN_USERNAME = 50
    MIN_LEN_USERNAME = 3

    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        unique=True,
        max_length=MAX_LEN_USERNAME,
        help_text=("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator, validators.MinLengthValidator(MIN_LEN_USERNAME)],
        error_messages={
            "unique": "A user with that username already exists.",
        }
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "A user with that email address already exists."
        }
    )

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)
    last_login = models.DateTimeField(
        ('last login'),
        default=datetime.now
    )
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.username

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class Gender(ChoicesEnumMixin, Enum):
    Male = 'Male'
    Female = "Female"
    DoNotShow = 'Do not show'


class Profile(models.Model):
    MAX_LEN_BIO = 50
    MAX_LEN_FIRST_NAME = 50
    MAX_LEN_LAST_NAME = 50

    user = models.OneToOneField(
        KnowMeUser,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(
        max_length=MAX_LEN_FIRST_NAME,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=MAX_LEN_LAST_NAME,
        null=True,
        blank=True,
    )

    picture = models.ImageField(
        blank=True,
        null=True,
        upload_to='profile_pics',
        #TODO: import it
        validators=(validate_file_size,)
    )
    birth_date = models.DateField(
        blank=True,
        null=True
    )
    gender = models.CharField(
        blank=True,
        null=True,
        choices=Gender.choices(),
        max_length=Gender.max_len(),
    )
    bio = models.CharField(
        max_length=MAX_LEN_BIO,
        null=True,
        blank=True,
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return f"{self.first_name}"
        elif self.last_name:
            return f"{self.last_name}"

    @receiver(post_save, sender=KnowMeUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=KnowMeUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        username = str(KnowMeUser.objects.filter(pk=self.user_id).get())
        return username


class ProfileReport(models.Model):
    MAX_LEN_TEXT = 100

    to_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='reported'
    )
    from_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='reporting'
    )
    date = models.DateTimeField(
        auto_now=True,
    )
    text = models.TextField(
        max_length=MAX_LEN_TEXT
    )

