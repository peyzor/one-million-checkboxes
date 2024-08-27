from django.urls import path

from checks import views

urlpatterns = [
    path('', views.home),
]
