import random
import string

from .models import URLMap

LINK_SYMBOLS = '^[A-Za-z0-9]*$'
MAX_LINK_LENGTH = 16
AUTO_LINK_LENGTH = 6


def get_unique_short_id():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    link = ''.join(random.choice(chars) for _ in range(AUTO_LINK_LENGTH))
    if URLMap.query.filter_by(short=link).first():
        return get_unique_short_id()
    return link
