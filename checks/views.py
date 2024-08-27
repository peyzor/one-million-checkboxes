from django.shortcuts import render


def home(request):
    context = {'loop_64': range(64)}
    return render(request, 'checks/home.html', context=context)
