from django.conf.urls import url

from landings import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
]
