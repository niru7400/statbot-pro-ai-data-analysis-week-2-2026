def is_safe_query(q):
    blocked = ["os", "sys", "delete", "rm", "subprocess"]

    for word in blocked:
        if word in q.lower():
            return False

    return True