import weakref
import collections
import time

from functools import wraps


def miniCache(expire=60 * 60 * 12):
    caches = LocalCache()

    def wrapper(func):
        @wraps(func)
        def wrapper1(request):
            key = func.__name__

            day = str(request.GET.get('day', ''))
            task_name = str(request.GET.get('task_name', ''))
            filter_province = '0000' if request.GET.get('just_choose_province', None) == 'true' else ''
            key += (day + filter_province + task_name)

            result = caches.get(key)
            if result is caches.notFound:
                result = func(request)
                caches.set(key, {r'result': result, r'expire': expire + caches.getNowTime()})
                return result
            else:
                result = result[r'result']
                return result

        return wrapper1

    return wrapper


class LocalCache:
    notFound = object()

    class Dict(dict):
        def __del__(self):
            pass

    def __init__(self, maxLen=10):
        self.weak = weakref.WeakValueDictionary()
        self.strong = collections.deque(maxlen=maxLen)

    @staticmethod
    def getNowTime():
        return int(time.time())

    def get(self, key):
        value = self.weak.get(key, self.notFound)
        if value is self.notFound or self.getNowTime() > value[r'expire']:
            return self.notFound
        return value

    def set(self, key, value):
        self.weak[key] = strongRef = LocalCache.Dict(value)
        self.strong.append(strongRef)



"""
import weakref
import collections
import time
import json

from flask import request
from functools import wraps


def miniCache(expire=60 * 60 * 12):
    caches = LocalCache()

    def wrapper(func):
        @wraps(func)
        def wrapper1():
            key = func.__name__

            model = request.json.get("model")
            kwargs = json.dumps(request.json.get("kwargs", {}), ensure_ascii=False)
            key += (model + kwargs)

            result = caches.get(key)
            if result is caches.notFound:
                result = func()
                caches.set(key, {r'result': result, r'expire': expire + caches.getNowTime()})
                return result
            else:
                result = result[r'result']
                return result

        return wrapper1

    return wrapper


class LocalCache:
    notFound = object()

    class Dict(dict):
        def __del__(self):
            pass

    def __init__(self, maxLen=10):
        self.weak = weakref.WeakValueDictionary()
        self.strong = collections.deque(maxlen=maxLen)

    @staticmethod
    def getNowTime():
        return int(time.time())

    def get(self, key):
        temp = self.weak.copy()
        for key, value in temp.items():
            if self.getNowTime() > value[r'expire']:
                self.weak.pop(key)
        value = self.weak.get(key, self.notFound)
        if value is self.notFound or self.getNowTime() > value[r'expire']:
            return self.notFound
        return value

    def set(self, key, value):
        self.weak[key] = strongRef = LocalCache.Dict(value)
        self.strong.append(strongRef)
"""