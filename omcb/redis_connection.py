import redis

CHECKS_BITSET_LIMIT = 2 ** 10
CHECKS_BITSET_LENGTH = 2 ** 20
CHECKS_BITSET_KEY = 'checks'


def get_redis_client():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    return redis_client
