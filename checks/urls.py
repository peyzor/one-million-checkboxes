from django.urls import path

from checks.views import my_test_view

urlpatterns = [
    path('home/', my_test_view),
]
