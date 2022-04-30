from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.response import Response
from Fast.django.decorators.cache.support import save_cache_list


def global_cache_page(cache_timeout: int):
    def decorator_function(view_function):
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.path) is None:
                response = view_function(*args, **kwargs)
                cache.set(request.path, response.data, cache_timeout)
                return response
            return Response(cache.get(request.path))
        return wrapper_function
    return decorator_function


def static_global_cache_page_renewable(cache_list_name: str):
    """
    Create global cache page without timeout and dinamic url
    """
    def decorator_function(view_function):
        def wrapper_function(*args, **kwargs):
            request = args[0]
            path = request.path.replace('/', '')
            if cache.get(path) is None:
                response = view_function(*args, **kwargs)
                cache.set(path, response.data, None)
                save_cache_list(cache_list_name, path)
                return response
            return Response(cache.get(path))
        return wrapper_function
    return decorator_function


def dinamic_global_cache_page_renewable(cache_list_name: str, group_name: str, name_id: str):
    """
    Create global cache page for dinamic url without timeout
    """
    def decorator_function(view_function):
        def wrapper_function(*args, **kwargs):
            cache_group = cache.get(group_name) or {}
            if cache_group.get(name_id) is None:
                response = view_function(*args, **kwargs)
                cache.set(group_name, {**cache_group, name_id: response.data}, None)
                save_cache_list(cache_list_name, group_name)
                return response
            return Response(cache_group.get(name_id))
        return wrapper_function
    return decorator_function


def double_cache_page(cache_timeout: int):
    def decorator_function(view_function):
        @cache_page(cache_timeout)
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.path) is None:
                response = view_function(*args, **kwargs)
                cache.set(request.path, response.data, cache_timeout)
                return response
            return Response(cache.get(request.path))
        return wrapper_function
    return decorator_function


def super_cache_page(global_cache_timeout: int, browser_cache_timeout: int):
    def decorator_function(view_function):
        @cache_page(browser_cache_timeout)
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.path) is None:
                response = view_function(*args, **kwargs)
                cache.set(request.path, response.data, global_cache_timeout)
                return response
            return Response(cache.get(request.path))
        return wrapper_function
    return decorator_function


def static_page(view_function):
    @cache_page(settings.STATIC_PAGE_CACHE_TIMEOUT)
    def wrapper_function(*args, **kwargs):
        request = args[0]
        if cache.get(request.path) is None:
            response = view_function(*args, **kwargs)
            cache.set(request.path, response.data, None)
            return response
        return Response(cache.get(request.path))
    return wrapper_function


def renew_or_cache_page(cache_timeout):
    def decorator_function(view_function):
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if request.headers.get('renew'):
                return view_function(*args, **kwargs)
            return cache_page(cache_timeout)(view_function)(*args, **kwargs)
        return wrapper_function
    return decorator_function


def control_cache_page(cache_timeout: int = 60*60*2):
    def decorator_function(view_function):
        @renew_or_cache_page(cache_timeout)
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.path) is None or request.headers.get('renew') == settings.SECRET_KEY:
                response = view_function(*args, **kwargs)
                cache.set(request.path, response.data, None)
                return response
            return Response(cache.get(request.path))
        return wrapper_function
    return decorator_function
    