from django.shortcuts import render

from checks.utils import get_checks
from omcb import redis_connection


def home(request):
    return render(request, 'checks/home.html')


def more_checks(request):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])

    redis_client = redis_connection.get_redis_client()
    checks = get_checks(redis_client=redis_client, limit=limit, offset=offset)

    context = {
        'checks': checks,
        'limit': limit,
        'offset': limit + offset
    }
    return render(request, 'checks/more_checks.html', context=context)
