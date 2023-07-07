import typing
import functools
import asyncio
import types
import sys
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

DEFAULT_WORKERS = (cpu_count() *2)+1

def asyncify(
    func: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        bound = functools.partial(func, self, *args, **kwargs)
        return await asyncio.to_thread(bound)
    return wrapper


def aio(max_workers: int = DEFAULT_WORKERS) -> typing.Callable[[typing.Type], typing.Type]:
    """Decorator that converts all the methods of a class into async methods."""
    
    def decorator(cls: typing.Type) -> typing.Type:
        attrs: typing.Dict[str, typing.Any] = {}
        if hasattr(cls, "executor") is False:
            attrs["executor"] = ThreadPoolExecutor(max_workers=max_workers)
        assert isinstance(cls.executor, ThreadPoolExecutor)
        for attr_name, attr_value in cls.__dict__.items():
            if (
                isinstance(attr_value, types.FunctionType)
                and attr_name.startswith("__") is False
            ):
                attrs[attr_name] = asyncify(attr_value)
            else:
                attrs[attr_name] = attr_value
        return type(cls.__name__, cls.__bases__, attrs)

    return decorator