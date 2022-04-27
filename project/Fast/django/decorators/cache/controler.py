from django.core.cache import cache


def renew_global_cache(urls: list | str):
    urls = urls if isinstance(urls, list) else [urls]
    none_cache = { url: None for url in urls }
    if len(none_cache.keys()) > 0:
        cache.set_many(none_cache)
