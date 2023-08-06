from typing import Any

from jsm_user_services import local_threading


def add_to_local_threading(key: str, value: Any):
    setattr(local_threading, key, value)


def remove_from_local_threading(key: str):
    try:
        delattr(local_threading, key)
    except:
        pass


def get_from_local_threading(key: str, default_value=None) -> Any:
    return getattr(local_threading, key, default_value)
