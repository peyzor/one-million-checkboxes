from django.shortcuts import render


def my_test_view(request):
    return render(request, 'checks/my_test.html')
