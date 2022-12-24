import random
import string

from .models import URLMap

LINK_SYMBOLS = '^[A-Za-z0-9]*$'


def get_unique_short_id():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    link = ''.join(random.choice(chars) for _ in range(6))
    if URLMap.query.filter_by(short=link).first():
        return get_unique_short_id()
    return link
