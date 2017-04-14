from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    password_change,
)

from registration.backends.default.views import ActivationView

from user_auth import views

urlpatterns = [
    url(r'^login/$', views.auth_login, name='login'),
    url(r'^logout/$', views.auth_logout, name='logout'),
    url(r'^register/$', views.auth_register, name='register'),
    url(r'^resend_email/$', views.resend_email, name='resend-email'),
    url(r'profile/edit/$', views.edit_profile, name='edit-profile'),
    url(r'profile/picture/$', views.edit_avatar, name='edit-avatar'),
    url(
        r'profile/view/(?P<username>[\w0-9-_]+)/$',
        views.view_profile,
        name='view-profile'
    ),
    url(
        r'profile/picture/remove/$',
        views.remove_avatar,
        name='remove-avatar'
    ),
    url(
        r'^reset/$',
        password_reset,
        {
            'template_name': 'user_auth/passwordreset/reset.html',
            'email_template_name': 'user_auth/passwordreset/email.html',
            'subject_template_name': 'user_auth/passwordreset/subject.txt',
        },
        name='password-reset'
    ),
    url(
        r'^reset/sent/$',
        password_reset_done,
        {
            'template_name': 'user_auth/passwordreset/sent.html',
        },
        name='password_reset_done'
    ),
    url(
        r'^reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {
            'template_name': 'user_auth/passwordreset/confirm.html',
        },
        name='password-reset-confirm'
    ),
    url(
        r'^reset/done/$',
        password_reset_complete,
        {
            'template_name': 'user_auth/passwordreset/done.html',
        },
        name='password_reset_complete'
    ),
    url(
        r'^password_change/$',
        password_change,
        {
            'template_name': 'user_auth/change_password.html',
            'post_change_redirect': 'home',
        },
        name='change-password'
    ),
    url(
        r'^activate/complete/$',
        TemplateView.as_view(
            template_name='user_auth/activation/complete.html'
        ),
        name='registration_activation_complete'
    ),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(
            template_name='user_auth/activation/activate.html'
        ),
        name='registration_activate'
    ),
    url(
        r'^register/email_sent/$',
        TemplateView.as_view(
           template_name='user_auth/registration/complete.html'
        ),
        name='registration-complete'
    ),
]
