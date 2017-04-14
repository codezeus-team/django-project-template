import pytest
from registration.models import RegistrationProfile

from user_auth.models import Account
from user_auth.tests.fixtures import UserFactory


@pytest.mark.django_db
class DescribeAccount:
    """Tests for the account model"""
    def it_is_represented_as_an_email(self):
        user = UserFactory()
        assert unicode(user) == user.email

    def it_has_date_joined_as_created_at(self):
        user = UserFactory()
        assert user.date_joined == user.created_at

    def it_returns_the_full_name(self):
        user = UserFactory(first_name='first', last_name='last')
        name = ' '.join([user.first_name, user.last_name])
        assert user.get_full_name() == name

    def it_returns_the_short_name(self):
        user = UserFactory(first_name='first', last_name='last')
        assert user.get_short_name() == user.first_name

    def it_returns_the_email_for_identification(self):
        user = UserFactory()
        user.first_name = ''
        assert user.get_identification() == user.email

    def it_returns_the_full_name_for_identification(self):
        user = UserFactory(first_name='first', last_name='last')
        assert user.get_identification() == user.get_full_name()

    def it_returns_the_profile(self):
        user = UserFactory(first_name='first', last_name='last')
        assert isinstance(user.profile, RegistrationProfile)


@pytest.mark.django_db
class DescribeAccountManager:
    """Test if the manager is working properly"""
    def it_can_create_user(self):
        user = Account.objects.create_user('test@test.com', 'password')
        assert user.email == 'test@test.com'
        assert user.check_password('password')
        Account.objects.get(pk=user.pk).delete()

    @pytest.mark.django_db
    def it_cannot_create_user_without_email(self):
        with pytest.raises(ValueError) as e:
            Account.objects.create_user('', 'password')
            assert e.message == 'Users must have a valid email address.'

    @pytest.mark.django_db
    def it_can_create_super_user(self):
        user = Account.objects.create_superuser('test@test.com', 'password')
        assert user.is_admin
        Account.objects.get(pk=user.pk).delete()
