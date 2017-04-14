import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from registration.models import RegistrationProfile
from django_toolset.decorators import authenticated_redirect

from .forms import ProfileForm, AvatarForm, RegistrationForm
from .models import Account


@login_required
def view_profile(request, username):
    """View Profile"""
    selected_user = Account.objects.get(username=username)

    context = {
        'selected_user': selected_user
    }

    return render(request, 'view_profile.html', context)


@login_required
def edit_profile(request):
    """Edit Profile"""
    user = request.user
    form = ProfileForm(request.POST or None, user=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your profile has been updated successfully')
        return redirect('view-profile', username=user.username)

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'edit_profile.html', context)


@login_required
def edit_avatar(request):
    """Edit User Avatar"""
    user = request.user
    form = AvatarForm(request.POST or None, request.FILES or None, user=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, ('Your profile picture has been updated '
                                   'successfully'))
        return redirect('edit-avatar')

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'avatar.html', context)


@login_required
def remove_avatar(request):
    """Remove User Avatar"""
    try:
        file_path = request.user.avatar.path
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception:
        messages.error(request, ('There was an error removing your profile '
                                 'picture'))
        return redirect('view-profile', username=request.user.username)

    request.user.avatar = None
    request.user.save()
    messages.success(request, ('Your profile picture has been removed '
                               'successfully'))

    return redirect('edit-avatar')


@authenticated_redirect(path='dashboard')
def auth_login(request):
    """Login Page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                msg = 'Welcome back {}!'.format(user.get_identification())
                messages.success(request, msg)
                return redirect('dashboard')
            else:
                URL = reverse('resend-email')
                link = '<a href="{}?email={}">here</a>'.format(URL, email)
                messages.error(request, 'You have not activated your account. '
                               'Click {} to resend the email'.format(link))
        else:
            messages.error(request, ('Your email or password appears to be '
                                     'incorrect'))

    return render(request, 'user_auth/login.html', {})


def resend_email(request):
    """Resend an activation email"""
    sent = RegistrationProfile.objects.resend_activation_mail(
        request.GET.get('email'),
        get_current_site(request),
        request,
    )

    if sent:
        return redirect('registration-complete')
    else:
        messages.error(request, 'There was an error while sending the link')
        return redirect('home')


@authenticated_redirect(path='dashboard')
def auth_register(request):
    """Register Page"""
    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.profile.send_activation_email(
                get_current_site(request), request
            )
            return redirect('registration-complete')

    context = {'form': form}
    return render(request, 'user_auth/registration/form.html', context)


@csrf_exempt
@login_required
@require_POST
def auth_logout(request):
    """Logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect('home')
