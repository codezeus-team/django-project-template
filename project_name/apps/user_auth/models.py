from __future__ import unicode_literals
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from registration.models import RegistrationProfile
from imagekit.models import ProcessedImageField


class AccountManager(BaseUserManager):
    """Required by Django and provides a way to manage accounts easier"""
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        kwargs['email'] = self.normalize_email(email)
        account = self.model(**kwargs)
        account.set_password(password)
        account.save()

        RegistrationProfile.objects.create_profile(account)

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    """Custom User Model
    Provides an enhanced base user with the ability to add any fields we want
    to it in order to make it work for the application.
    """
    username = models.CharField(max_length=50, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    avatar = ProcessedImageField(
        upload_to='avatars',
        format='JPEG',
        options={'quality': 80}
    )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    @property
    def date_joined(self):
        """Get the dat the user joined"""
        return self.created_at

    @property
    def profile(self):
        """Get the attached user profile"""
        return RegistrationProfile.objects.get(user=self)

    def get_full_name(self):
        """Get the first and last name combined"""
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        """Get just the first name"""
        return self.first_name

    def get_identification(self):
        """Get the full name if there is a first name otherwise the email"""
        return self.get_full_name() if self.first_name else self.email
