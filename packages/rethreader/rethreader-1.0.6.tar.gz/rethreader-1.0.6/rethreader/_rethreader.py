import ctypes
from collections import namedtuple
from threading import Thread
from time import sleep
from typing import Optional, Iterable, List, Set

Key = namedtuple("Key", ["id", "target", "args", "kwargs"])


class Description:
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    def __eq__(self, other):
        return type(self) == type(other) and self.string == other.string

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.string}')"


_no_id = Description("No Id")
_not_returned = Description("Not Returned")
_thread_info_descriptor = Description("Thread Info")


class ThreadInfo(Description):
    def __init__(self, k, sep=None):
        _sep = sep or '; '
        _, a, b, c = k
        tup = str(a), str(b), str(c)

        def cond():
            return any(map(lambda x: _sep in x, tup))

        if sep and cond():
            raise ValueError('An argument contains the separator')
        while cond():
            _sep = ';' + _sep
        string = _sep.join(str(i) for i in tup)
        super(ThreadInfo, self).__init__(string)
        self.sep = _sep

    def key(self):
        return Key(_thread_info_descriptor, *self.string.split(self.sep))


class KeyThread(Thread):
    def __init__(self, key: Key, daemon: Optional[bool] = None):
        assert _is_unpacked(key)
        assert key.id != _thread_info_descriptor
        self.key = key
        n, target, args, kwargs = key
        if kwargs is None:
            kwargs = {}
        self.id = n
        self._result = _not_returned
        super(KeyThread, self).__init__(target=target, args=args, kwargs=kwargs, daemon=daemon)

    @property
    def info(self):
        return ThreadInfo(self.key)

    def kill(self):
        if self.is_alive():
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, 0)
            self.join(0)

    @classmethod
    def of(cls, target=None, args=(), kwargs=None, daemon=None):
        return cls(Key(_no_id, target, args, kwargs), daemon)

    @property
    def result(self):
        return self._result

    def run(self):
        self._result = self._target(*self._args, **self._kwargs)
        return self

    def start(self):
        super(KeyThread, self).start()
        return self


def _is_unpacked(_object) -> bool:
    if isinstance(_object, Key):
        return True
    return isinstance(_object, tuple) and len(_object) == 4 and isinstance(_object[0], (int, type(None))) and \
           callable(_object[1]) and isinstance(_object[2], tuple) and isinstance(_object[3], dict)


def thread_info(self) -> ThreadInfo:
    if isinstance(self, KeyThread):
        return self.info
    elif _is_unpacked(self):
        return ThreadInfo(self)


class Rethreader:
    def __init__(self, target=None, queue: Optional[Iterable] = None, max_threads: int = 16, clock_delay: float = 0.01,
                 auto_quit: Optional[bool] = None, save_results=True, daemon: bool = False):
        if target is not None:
            assert callable(target)
        self._target = target
        self._main: Set[KeyThread] = set()
        self._in_delay_queue: int = 0
        if save_results:
            self._finished: Set[KeyThread] = set()
        else:
            self._finished: int = 0
        self._daemonic: bool = daemon
        self._clock: float = clock_delay
        self._max_threads: int = 0 if max_threads < 0 else max_threads
        self._queue: List[Key] = []
        if queue:
            [self.add(_t) for _t in queue]
        self._auto_quit: bool = auto_quit if auto_quit else bool(queue)
        self._running: bool = False
        self._start_thread = None

    def __add__(self, *args, **kwargs):
        self._append(self._unpack(*args, **kwargs))
        return self

    def __enter__(self):
        if not self._running:
            self.start()
        return self.auto_quit(False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._auto_quit = True

    def __len__(self) -> int:
        return self.remaining + self.finished

    def _unpack(self, *_object, **kwargs) -> Key:
        if isinstance(_object, tuple) and len(_object) == 1:
            _object = _object[0]
        if _object and isinstance(_object, Key):
            return _object
        target = None if self._target is None else self._target
        args = None
        _list = None
        if _object and isinstance(_object, Iterable) and not isinstance(_object, str):
            _list = list(_object)
            if not target and callable(_list[0]):
                target = _list.pop(0)
            if not kwargs:
                if _is_unpacked(_object):
                    _, target, args, kwargs = _object
                elif isinstance(_object, dict):
                    args, kwargs = (), _object
                elif _list:
                    if isinstance(_list[-1], dict):
                        kwargs = _list.pop(-1)
                else:
                    args = ()
        if target is not None:
            if args is None:
                if _list:
                    if len(_list) == 1 and isinstance(_list[0], tuple):
                        args = _list[0]
                    else:
                        args = tuple(_list)
                elif isinstance(_object, tuple):
                    args = _object
                else:
                    args = (_object,)
            return Key(len(self), target, args, kwargs)
        return Key(len(self), _object, (), kwargs)

    def _info_unpack(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], ThreadInfo):
            return args[0].key()
        return self._unpack(*args, **kwargs)

    def _get_thread(self, target=None, args=(), kwargs=None) -> KeyThread:
        if isinstance(target, Key):
            return KeyThread(target, self._daemonic)
        return KeyThread.of(target, args, kwargs, self._daemonic)

    def _load_target(self, target) -> KeyThread:
        if isinstance(target, KeyThread):
            return target
        return self._get_thread(self._unpack(target))

    def _start_next(self):
        next_target = self._queue.pop(0)
        next_thread = self._load_target(next_target)
        next_thread.start()
        self._main.add(next_thread)

    def run(self):
        _save = type(self._finished) == set
        self._running = True
        while self._running:
            for t in self._main.copy():
                if not t.is_alive():
                    if _save:
                        self._finished.add(t)
                    else:
                        self._finished += 1
                    self._main.remove(t)
            while self._queue:
                if 0 < self._max_threads <= len(self._main):
                    break
                self._start_next()
            if self._auto_quit and self.is_empty():
                self._running = False
            else:
                sleep(self._clock)
        return self

    def _append(self, _object, _delay: int = 0):
        self._in_delay_queue += 1
        if _delay:
            sleep(_delay)
        self._queue.append(_object)
        self._in_delay_queue -= 1

    def _find(self, _thread_info: ThreadInfo):
        _lists = [self._main, self._queue]
        if isinstance(self._finished, set):
            _lists.append(self._finished)
        for _list in _lists:
            for thread in _list.copy():
                if thread_info(thread) == _thread_info:
                    return thread

    def _insert(self, _object, _index: int = 0):
        self._queue.insert(_index, _object)

    def add(self, *args, **kwargs):
        self._append(self._unpack(*args, **kwargs))
        return self

    def find(self, *args, **kwargs):
        thi = ThreadInfo(self._info_unpack(*args, **kwargs))
        if thread := self._find(thi):
            return thread

    def extend(self, _list: list):
        for i in _list:
            self.add(i)
        return self

    def insert(self, _index: int, *args, **kwargs):
        self._insert(self._unpack(*args, **kwargs), _index)
        return self

    def prioritize(self, _list: list):
        for i in reversed(_list):
            self._insert(self._unpack(i))
        return self

    def remove(self, *args, **kwargs):
        _thi = ThreadInfo(self._info_unpack(*args, **kwargs))
        if thread := self._find(_thi):
            _list = self._queue
            if isinstance(thread, KeyThread):
                thread.kill()
                _list = self._main
            try:
                _list.remove(thread)
            except KeyError:
                pass
        return self

    def postpone(self, delay, *args, **kwargs):
        _object = self._unpack(*args, **kwargs)
        self.remove(_object)
        self._get_thread(self._append, (_object, delay)).start()
        return self

    def auto_quit(self, _bool: bool = True):
        self._auto_quit = _bool
        return self

    @property
    def finished(self) -> int:
        if isinstance(self._finished, set):
            return len(self._finished)
        return self._finished

    @property
    def in_queue(self) -> int:
        return len(self._queue) + self._in_delay_queue

    def is_empty(self) -> bool:
        return self.remaining == 0

    def is_alive(self) -> bool:
        return self._running

    def kill(self):
        self._queue.clear()
        for thread in self._main:
            thread.kill()
        self._main.clear()
        self._running = False
        if self._start_thread:
            self._start_thread.kill()
        return self

    def quit(self):
        self.auto_quit()
        while self._running:
            sleep(self._clock)

    @property
    def remaining(self) -> int:
        return len(self._main) + self.in_queue

    @property
    def results(self) -> list:
        if isinstance(self._finished, set):
            return [None if i == _not_returned else i.result
                    for i in sorted(self._finished, key=lambda x: x.id)]

    def start(self):
        self._start_thread = self._get_thread(self.run)
        self._start_thread.start()
        return self


if __name__ == '__main__':
    print("Hello world!")
