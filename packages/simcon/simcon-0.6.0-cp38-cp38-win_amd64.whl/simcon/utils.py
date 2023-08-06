import asyncio
import dataclasses
import functools
import threading
import time
import typing

from collections import deque
from .base import HasExceptions, Closeable


@dataclasses.dataclass()
class GlobalEvent(HasExceptions, Closeable):

    _value: bool = dataclasses.field(default=False, init=False)
    _lock: threading.Lock = dataclasses.field(default_factory=threading.Lock, init=False)

    def is_set(self) -> bool:
        return self._value

    async def wait(self, timeout: typing.Optional[float] = None) -> None:
        with self._lock:
            self.check_exception()
            self.check_closed()
            if self._value:
                return
            waiter = self.add_waiter()
        await asyncio.wait_for(waiter, timeout)
        self.check_exception()
        self.check_closed()

    def set(self) -> None:
        with self._lock:
            if self._value:
                return
            self._value = True
            self.notify_all()

    def clear(self) -> None:
        self._value = False


class Autoincrement:

    _last_value: typing.Optional[int]
    _max_value = typing.Optional[int]
    _lock: threading.Lock

    def __init__(self, last_value: int = None, max_value: int = None):
        self._last_value = last_value
        self._max_value = None
        self._lock = threading.Lock()

    @property
    def last_value(self) -> int:
        return self._last_value

    def next(self, skip: typing.Optional[typing.Iterable] = None) -> int:
        with self._lock:
            while True:
                if self._last_value is None:
                    self._last_value = 0
                else:
                    self._last_value += 1
                if self._max_value is not None and self._last_value > self._max_value:
                    self._last_value = 0
                if skip is None or self._last_value not in skip:
                    return self._last_value


class AutoincrementDWORD(Autoincrement):

    def __init__(self, last_value: int = None):
        super().__init__(last_value=last_value, max_value=2**32 - 1)


def no_async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            asyncio.get_running_loop()
            raise Exception("This code cannot run in asyncio loops. Use async interface instead")
        except RuntimeError:  # No running loop, as expected
            pass
        return func(*args, **kwargs)
    return wrapper


class AsyncThreadingLock:

    _lock: threading.Lock
    _waiters = "deque[asyncio.Future]"

    def __init__(self):
        self._lock = threading.Lock()
        self._waiters = deque()

    def __repr__(self):
        return self._lock.__repr__()

    @no_async
    def acquire(self, blocking=True, timeout: float = -1) -> bool:
        return self._lock.acquire(blocking, timeout)

    async def async_acquire(self, blocking=True, timeout: float = -1) -> bool:
        if timeout != -1 and not blocking:
            raise ValueError("can't specify a timeout for a non-blocking call")
        if timeout != -1 and timeout < 0:
            raise ValueError("timeout value must be positive")
        timeout_at = time.monotonic() + timeout
        while True:
            if self._lock.acquire(blocking=False):
                return True
            elif timeout == 0:
                return False
            waiter = asyncio.get_event_loop().create_future()
            self._waiters.append(waiter)
            # Double check that the lock is still acquired and we well be notified
            if self._lock.acquire(blocking=False):
                return True
            if timeout == -1:
                async_timeout = None
            else:
                async_timeout = timeout_at - time.monotonic()
            await asyncio.wait_for(waiter, async_timeout)
            first = False

    def _notify(self):
        while True:  # Try all waiters until one succeeds or none are left
            try:
                waiter = self._waiters.popleft()
            except IndexError:  # Empty list
                return

            def notify_fallback():
                try:
                    waiter.set_result(None)
                except asyncio.InvalidStateError:  # Future cancelled
                    self._notify()

            try:
                waiter.get_loop().call_soon_threadsafe(notify_fallback)
                return
            except RuntimeError:  # Loop isn't running
                continue

    def release(self):
        self._lock.release()
        self._notify()

    async def __aenter__(self):
        return await self.async_acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()

    @no_async
    def __enter__(self):
        return self._lock.__enter__()

    @no_async
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
