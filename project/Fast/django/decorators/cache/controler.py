from django.core.cache import cache


def renew_global_cache(urls: list | str):
    urls = urls if isinstance(urls, list) else [urls]
    none_cache = { url: None for url in urls }
    cache.set_many(none_cache)
