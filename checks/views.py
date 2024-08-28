from django.shortcuts import render

from omcb import redis_connection


def home(request):
    context = {'the_loop': range(redis_connection.CHECKS_BITSET_LENGTH)}
    return render(request, 'checks/home.html', context=context)
