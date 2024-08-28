from django.apps import AppConfig

from omcb import redis_connection


class ChecksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checks'

    def ready(self):
        redis_client = redis_connection.get_redis_client()

        if not redis_client.exists(redis_connection.CHECKS_BITSET_KEY):
            redis_client.setbit(redis_connection.CHECKS_BITSET_KEY, redis_connection.CHECKS_BITSET_LENGTH - 1, 0)
