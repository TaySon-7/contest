from functools import update_wrapper
from typing import Callable
class cached_method:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.name_cached = f"{func.__name__}_cached"
        update_wrapper(self, func)

    def __get__(self, instance: object | None, owner: type | None) -> Callable | object:
        if instance is None:
            return self

        def wrapper() -> object:
            if self.name_cached not in instance.__dict__:
                instance.__dict__[self.name_cached] = self.func(instance)
            return instance.__dict__[self.name_cached]

        update_wrapper(wrapper, self.func)
        return wrapper

    def reset(self, instance: object) -> None:
        instance.__dict__.pop(self.name_cached, None)