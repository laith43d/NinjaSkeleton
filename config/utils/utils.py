import random
import string
from math import ceil

from cryptography.fernet import Fernet


def create_random_key(size: int = 140) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


def create_random_encryption_key() -> bytes:
    return Fernet.generate_key()


ALLOWED_INT = '0123456789'


def random_string_generator(size=10, chars=ALLOWED_INT) -> str:
    """
    Description:Generate random values based on the size and chars passed.\n
    """
    return ''.join(random.choice(chars) for _ in range(size))


def custom_key_generator(instance, size=6):
    """
    Description:Generate a unique key for every instance passed.\n
    """
    new_key = random_string_generator(size=size)

    # get the class from the instance
    Klass = instance.__class__

    # qs_exists = Klass.objects.filter(key=new_key).exclude(is_active=True).exists()
    qs_exists = Klass.objects.filter(key=new_key).exists()
    if qs_exists:
        return custom_key_generator(size=size)

    return new_key


def paginated_response(queryset, *, per_page=10, page=1):
    try:
        total_count = len(queryset)
    except TypeError:
        total_count = 1
    limit = per_page
    offset = per_page * (page - 1)
    page_count = ceil(total_count / per_page)

    try:
        data = list(queryset[offset: limit + offset])
    except TypeError:
        data = queryset

    return {
        'total_count': total_count,
        'per_page': limit,
        'from_record': offset + 1,
        'to_record': (offset + limit) if (offset + limit) <= total_count else (total_count % per_page) + offset,
        'previous_page': page - 1 if page > 2 else 1,
        'current_page': page,
        'next_page': min(page + 1, page_count),
        'page_count': page_count,
        'data': data,
    }


def response(status, data, *, paginated: bool = False, per_page: int = 10, page: int = 1):
    if paginated:
        return status, paginated_response(data, per_page, page)

    return status, data
