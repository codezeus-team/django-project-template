import uuid
from contextlib import contextmanager

import pytest
import factory

from registration.models import RegistrationProfile

from conftest import fake_image
from user_auth.models import Account


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RegistrationProfile

    user = factory.SubFactory(
        'user_auth.tests.fixtures.UserFactory',
        profile=None
    )


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    email = factory.Sequence(lambda n: "user%s@email.com" % n)
    username = uuid.uuid4()
    password = factory.PostGenerationMethodCall('set_password', 'password')
    profile = factory.RelatedFactory(ProfileFactory, 'user')
    is_active = True

    @staticmethod
    @contextmanager
    def login(client, user):
        """login is a contextmanager which allows us to run tests if they are
        logged in and if they are not then we don't run them.
        """
        yield client.post('/login/', {
            'email': user.email,
            'password': 'password',
        })


@pytest.fixture()
def active_user(db, client):
    """Return an active user"""
    user = UserFactory()
    user.login = lambda: UserFactory.login(client, user)
    return user


@pytest.fixture()
def inactive_user(db, client):
    """Return an inactive user"""
    user = UserFactory(is_active=False)
    user.login = lambda: UserFactory.login(client, user)
    return user


@pytest.fixture()
def avatar_user(active_user):
    """Return a user with an avatar"""
    active_user.avatar = fake_image()
    return active_user
