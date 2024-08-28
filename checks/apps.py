from django.apps import AppConfig
from omcb.redis_connection import get_redis_client, CHECKS_BITSET_KEY


class ChecksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checks'

    def ready(self):
        redis_client = get_redis_client()

        if not redis_client.exists(CHECKS_BITSET_KEY):
            redis_client.setbit(CHECKS_BITSET_KEY, 1000 - 1, 0)
