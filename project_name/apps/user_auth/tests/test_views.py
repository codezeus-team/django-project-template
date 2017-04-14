import os
import pytest

from conftest import fake_image, mock_messages
from user_auth.tests.fixtures import (
    active_user,
    inactive_user,
    avatar_user,
)
from user_auth.views import (
    edit_profile,
    edit_avatar,
    remove_avatar,
    resend_email,
)


class DescribeLogin:
    """Test the login view"""
    def it_loads(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    def it_allows_login(self, active_user):
        with active_user.login() as login_response:
            assert login_response.status_code == 302
            assert login_response.url == '/dashboard'

    def it_does_not_allow_login_for_inactive_user(self, inactive_user):
        with inactive_user.login() as response:
            messages = dict(response.context).get('messages')
            assert len(messages) == 1
            assert 'resend_email' in messages._loaded_messages[0].message

    @pytest.mark.django_db
    def it_does_not_allow_login_for_wrong_credentials(self, client):
        response = client.post('/login/', {
            'username': 'nobody',
            'password': 'nothing',
        })
        assert response.status_code == 200
        messages = dict(response.context).get('messages')
        assert len(messages) == 1
        msg = 'Your email or password appears to be incorrect'
        assert messages._loaded_messages[0].message == msg


class DescribeRegistration:
    """Test the login view"""
    def it_loads(self, client):
        response = client.get('/register/')
        assert response.status_code == 200

    @pytest.mark.django_db
    def it_allows_registration(self, client):
        response = client.post('/register/', {
            'email': 'nobody@nowhere.com',
            'password': 'nothing',
            'confirm_password': 'nothing',
        })
        assert response.status_code == 302
        assert response.url == '/register/email_sent/'

    @pytest.mark.django_db
    def it_doesnt_allow_registration_on_invalid_data(self, client):
        response = client.post('/register/', {
            'email': 'nobody',
            'password': 'nothing',
            'confirm_password': 'nothing',
        })
        assert response.status_code == 200
        assert 'email' in dict(response.context).get('form').errors


class DescribeResendemail:
    """Test the resend email view"""
    def it_resends_activation_email(self, rf, inactive_user):
        request = rf.get('/resend_email/', {
            'email': inactive_user.email
        })
        request.user = inactive_user
        response = resend_email(request)
        assert response.status_code == 302
        assert response.url == '/register/email_sent/'

    def it_fails_without_email(self, rf, inactive_user):
        request = rf.get('/resend_email/')
        request.user = inactive_user
        mock_messages(request)
        response = resend_email(request)
        assert response.status_code == 302
        assert response.url == '/'


class DescribeLogout:
    """Test the logout view"""
    def it_doesnt_load_with_get_request(self, client, active_user):
        with active_user.login():
            response = client.get('/logout/')
            assert response.status_code == 405

    def it_allows_post(self, client, active_user):
        with active_user.login():
            response = client.post('/logout/', {})
            assert response.url == '/'


class DescribeProfile:
    """Test the profile actions"""
    def it_loads(self, client, active_user):
        with active_user.login():
            url = '/profile/view/{}/'.format(active_user.username)
            response = client.get(url)
            assert response.status_code == 200
            assert response.context['selected_user'] == active_user

    def it_loads_edit_page(self, client, active_user):
        with active_user.login():
            response = client.get('/profile/edit/')
            assert response.status_code == 200
            assert response.context['user'] == active_user

    def it_allows_editing(self, rf, active_user):
        with active_user.login():
            request = rf.post('/profile/edit/', {
                'email': active_user.email,
                'username': 'test',
                'first_name': 'Test',
                'last_name': 'User',
            })
            request.user = active_user
            mock_messages(request)
            edit_profile(request)
            assert active_user.first_name == 'Test'
            assert active_user.last_name == 'User'


class DescribeAvatar:
    """Test the avatar actions"""
    def it_allows_delete(self, rf, avatar_user):
        with avatar_user.login():
            fake_image(avatar_user.avatar.path)
            request = rf.post('/profile/picture/remove/', {})
            request.user = avatar_user
            mock_messages(request)
            response = remove_avatar(request)
            assert response.url == '/profile/picture/'
            assert not avatar_user.avatar

    def it_doesnt_allow_delete_with_no_image(self, rf, active_user):
        with active_user.login():
            request = rf.post('/profile/picture/remove/', {})
            request.user = active_user
            mock_messages(request)
            response = remove_avatar(request)
            url = '/profile/view/{}/'.format(active_user.username)
            assert response.url == url

    def it_doesnt_delete_with_bad_img_path(self, rf, avatar_user):
        with avatar_user.login():
            request = rf.post('/profile/picture/remove/', {})
            request.user = avatar_user
            mock_messages(request)
            response = remove_avatar(request)
            assert response.url == '/profile/picture/'
            assert avatar_user.avatar is not None

    def it_loads_edit_page(self, client, active_user):
        with active_user.login():
            response = client.get('/profile/picture/')
            assert response.status_code == 200
            assert response.context['user'] == active_user

    def it_allows_editing(self, rf, active_user):
        with active_user.login():
            assert not active_user.avatar
            img = fake_image()
            request = rf.post('/profile/picture/', {'avatar': img})
            request.user = active_user
            mock_messages(request)
            edit_avatar(request)
            assert active_user.avatar
            os.remove(img.path)
            os.remove(active_user.avatar.path)
