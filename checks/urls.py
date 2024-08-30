from django.urls import path

from checks import views

urlpatterns = [
    path('', views.home, name='home'),
    path('more-checks/', views.more_checks, name='more_checks')
]
