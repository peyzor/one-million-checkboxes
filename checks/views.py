from django.shortcuts import render


def home(request):
    context = {'the_loop': range(1000)}
    return render(request, 'checks/home.html', context=context)
