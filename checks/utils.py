from omcb import redis_connection


def get_initial_state(redis_client):
    checks_bitset = redis_client.get(redis_connection.CHECKS_BITSET_KEY)
    if not checks_bitset:
        raise Exception('bitset not found')

    count = redis_client.bitcount(redis_connection.CHECKS_BITSET_KEY)

    statuses = []
    for b in checks_bitset:
        for i in range(7, -1, -1):
            status = (b >> i) & 1
            statuses.append(status)

    context = {'statuses': enumerate(statuses), 'count': count}
    return context
