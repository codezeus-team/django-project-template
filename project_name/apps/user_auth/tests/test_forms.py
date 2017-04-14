import pytest

from user_auth.tests.fixtures import UserFactory, active_user
from user_auth.forms import ProfileForm, RegistrationForm

@pytest.mark.django_db
class DescribeProfileForm:
    """Test if the ProfileForm functions correctly"""
    def it_is_validated(self, active_user):
        data = {
            'email': active_user.email,
            'username': active_user.username,
            'first_name': active_user.first_name,
            'last_name': active_user.last_name,
        }
        form = ProfileForm(data, user=active_user)
        assert form.is_valid()

    def it_requires_email(self, active_user):
        data = {
            'username': active_user.username,
            'first_name': active_user.first_name,
            'last_name': active_user.last_name,
        }
        form = ProfileForm(data, user=active_user)
        assert not form.is_valid()
        assert 'email' in form.errors.keys()

    def it_requires_username(self, active_user):
        data = {
            'email': active_user.email,
            'first_name': active_user.first_name,
            'last_name': active_user.last_name,
        }
        form = ProfileForm(data, user=active_user)
        assert not form.is_valid()
        assert 'username' in form.errors.keys()

    def it_checks_email(self, active_user):
        existing_email = 'existing@test.com'
        UserFactory(username='existing', email=existing_email)

        data = {
            'email': existing_email,
            'username': active_user.username,
            'first_name': active_user.first_name,
            'last_name': active_user.last_name,
        }
        form = ProfileForm(data, user=active_user)
        assert not form.is_valid()
        assert 'email' in form.errors.keys()
        assert form.errors['email'][0] == 'That email already exists.'

    def it_checks_username(self, active_user):
        existing_username = 'existing'
        UserFactory(username=existing_username)

        data = {
            'email': active_user.username,
            'username': existing_username,
            'first_name': active_user.first_name,
            'last_name': active_user.last_name,
        }
        form = ProfileForm(data, user=active_user)
        assert not form.is_valid()
        assert 'username' in form.errors.keys()
        assert form.errors['username'][0] == 'That username already exists.'


@pytest.mark.django_db
class DescribeRegistrationForm:
    """Test if the RegistrationForm functions correctly"""
    def it_is_validated(self):
        data = {
            'email': 'test@test.com',
            'password': 'password',
            'confirm_password': 'password',
        }
        form = RegistrationForm(data)
        assert form.is_valid()

    def it_checks_email(self):
        existing_email = 'existing@test.com'
        UserFactory(email=existing_email)

        data = {
            'email': existing_email,
            'password': 'password',
            'confirm_password': 'password',
        }
        form = RegistrationForm(data)
        assert not form.is_valid()
        assert 'email' in form.errors.keys()
        assert form.errors['email'][0] == 'Your email already is in use'

    def it_checks_passwords(self):
        data = {
            'email': 'test@test.com',
            'password': 'password',
            'confirm_password': 'pass',
        }
        form = RegistrationForm(data)
        assert not form.is_valid()
        assert '__all__' in form.errors.keys()
        assert form.errors['__all__'][0] == 'Your passwords do not match'
