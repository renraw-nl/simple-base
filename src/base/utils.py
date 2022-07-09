"""
File   : src/base / utils.py
Since  : 2022-07-04
"""

import uuid


def get_uuid():
    """Returns a UUID4"""
    return str(uuid.uuid4())
