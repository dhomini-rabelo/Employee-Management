from django.core.cache import cache


def save_cache_list(list_name: str, new_key_name: str):
    cache_list: list[str] = cache.get(list_name) or []
    if new_key_name not in cache_list:
        cache.set(list_name, [*cache_list, new_key_name], None)