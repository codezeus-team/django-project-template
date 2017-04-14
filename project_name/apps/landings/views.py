from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Home View
    """
    return render(request, 'home.html', {})


@login_required
def dashboard(request):
    """
    Dashboard View
    """
    return render(request, 'dashboard.html', {})
