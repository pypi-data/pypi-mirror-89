def is_relative_to(first, second):
    try:
        first.relative_to(second)
        return True
    except ValueError:
        return False
