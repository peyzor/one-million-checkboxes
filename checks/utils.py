from omcb import redis_connection


def get_checks(redis_client, limit, offset):
    checks_bitset = redis_client.get(redis_connection.CHECKS_BITSET_KEY)
    assert checks_bitset is not None

    start = offset // 8
    end = start + limit // 8

    checks = []
    for i in range(start, end):
        b = checks_bitset[i]

        for j in range(7, -1, -1):
            status = (b >> j) & 1
            offset = i * 8 + (7 - j)
            checks.append((offset, status))

    return checks
