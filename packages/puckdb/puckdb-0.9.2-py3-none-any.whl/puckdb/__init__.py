#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of puckdb
# (see https://github.com/carstencodes/puckdb).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""PuckDB is a thread-safe implementation of pickleDB. It uses
pickleDB under the hood, but can be used from multi-threaded applications.
"""

from os import PathLike
import time
from typing import Any, Iterable, KeysView, Literal, Optional, Union
import queue
import threading

import pickledb


class PuckDB(pickledb.PickleDB):
    """PuckDB is a concurrent revision of pickleDB. Since it is derived from pickleDB,
    it offers the same methods but declares a thread safe interface.
    """

    def __init__(self, location: PathLike, auto_dump: bool, sig: bool):
        """Creates a database object and loads the data from the location path.
        If the file does not exist it will be created on the first update.
        """
        self.__lock = threading.RLock()
        self.__scheduler = _DumpingScheduler(self)
        self.__must_auto_dump = auto_dump
        super().__init__(location, auto_dump, sig)

    def load(self, location: PathLike, auto_dump: bool) -> Literal[True]:
        """Loads, reloads or changes the path to the db file"""
        with self.__lock:
            self.__must_auto_dump = auto_dump
            return super().load(location, auto_dump)

    def dump(self) -> Literal[True]:
        """Force dump memory db to file"""
        with self.__lock:
            return super().dump()

    def set(self, key: str, value: Any) -> Union[Literal[True], TypeError]:
        """Set the str value of a key"""
        with self.__lock:
            return super().set(key, value)

    def get(self, key: str) -> Union[Any, Literal[False]]:
        """Get the value of a key"""
        with self.__lock:
            return super().get(key)

    def getall(self) -> Union[KeysView, Any]:
        """Return a list of all keys in db"""
        with self.__lock:
            return super().getall()

    def exists(self, key: str) -> bool:
        """Return True if key exists in db, return False if not"""
        with self.__lock:
            return super().exists(key)

    def rem(self, key: str) -> Literal[True]:
        """Delete a key"""
        with self.__lock:
            return super().rem(key)

    def totalkeys(self, name: Any = None) -> int:
        """Get a total number of keys, lists, and dicts inside the db"""
        with self.__lock:
            return super().totalkeys(name)

    def append(self, key: str, more: Any) -> Literal[True]:
        """Add more to a key's value"""
        with self.__lock:
            return super().append(key, more)

    def lcreate(self, name: str) -> Literal[True]:
        """Create a list, name must be str"""
        with self.__lock:
            return super().lcreate(name)

    def ladd(self, name: str, value: Any) -> Literal[True]:
        """Add a value to a list"""
        with self.__lock:
            return super().ladd(name, value)

    def lextend(self, name: str, seq: Iterable) -> bool:
        """Extend a list with a sequence"""
        with self.__lock:
            return super().lexists(name, seq)

    def lgetall(self, name: str) -> Any:
        """Return all values in a list"""
        with self.__lock:
            return super().lgetall(name)

    def lget(self, name: str, pos: int) -> Any:
        """Return one value in a list"""
        with self.__lock:
            return super().lget(name, pos)

    def lremlist(self, name: str) -> int:
        """Remove a list and all of its values"""
        with self.__lock:
            return super().lremlist(name)

    def lremvalue(self, name: str, value: Any) -> Literal[True]:
        """Remove a value from a certain list"""
        with self.__lock:
            return super().lremvalue(name, value)

    def lpop(self, name: str, pos: int) -> Any:
        """Remove one value in a list"""
        with self.__lock:
            return super().lpop(name, pos)

    def llen(self, name: str) -> int:
        """Returns the length of the list"""
        with self.__lock:
            return super().llen(name)

    def lappend(self, name: str, pos: int, more: Any) -> Literal[True]:
        """Add more to a value in a list"""
        with self.__lock:
            return super().lappend(name, pos, more)

    def lexists(self, name: str, value: Any) -> bool:
        """Determine if a value  exists in a list"""
        with self.__lock:
            return super().lexists(name, value)

    def dcreate(self, name: str) -> Union[Literal[True], TypeError]:
        """Create a dict, name must be str"""
        with self.__lock:
            return super().dcreate(name)

    def dadd(self, name: str, pair: tuple) -> Literal[True]:
        """Add a key-value pair to a dict, "pair" is a tuple"""
        with self.__lock:
            return super().dadd(name, pair)

    def dget(self, name: str, key: Any) -> Any:
        """Return the value for a key in a dict"""
        with self.__lock:
            return super().dget(name, key)

    def dgetall(self, name: str) -> Any:
        """Return all key-value pairs from a dict"""
        with self.__lock:
            return super().dgetall(name)

    def drem(self, name: str) -> Literal[True]:
        """Remove a dict and all of its pairs"""
        with self.__lock:
            return super().drem(name)

    def dpop(self, name: str, key: Any) -> Any:
        """Remove one key-value pair in a dict"""
        with self.__lock:
            return super().dpop(name, key)

    def dkeys(self, name: str) -> Union[KeysView, Any]:
        """Return all the keys for a dict"""
        with self.__lock:
            return super().dkeys(name)

    def dvals(self, name: str) -> Any:
        """Return all the values for a dict"""
        with self.__lock:
            return super().dvals(name)

    def dexists(self, name: str, key: Any) -> bool:
        """Determine if a key exists or not in a dict"""
        with self.__lock:
            return super().dexists(name, key)

    def dmerge(self, name1: str, name2: str) -> Literal[True]:
        """Merge two dicts together into name1"""
        with self.__lock:
            return super().dmerge(name1, name2)

    def deldb(self) -> bool:
        """Delete everything from the database"""
        try:
            with self.__lock:
                return super().deldb()
        finally:
            self.__scheduler.stop()

    def _autodumpdb(self) -> None:
        """Write/save the json dump into the file if auto_dump is enabled"""
        if self.__must_auto_dump:
            self.__scheduler.schedule_dump_job()


class _DumpingScheduler:
    def __init__(self, db: PuckDB) -> None:
        """Creates a scheduler for the puckDB

        Args:
            db (PuckDB): The database to dump regularly.
        """
        super().__init__()
        self.__db: PuckDB = db
        self.__queue: queue.Queue = queue.Queue(2)
        self.__run_jobs: bool = True
        self.__lock: threading.RLock = threading.RLock()
        self.__worker: threading.Thread = threading.Thread(
            target=self.__dump_job, daemon=True
        ).start()

    def stop(self) -> None:
        """Stops the scheduler by cancelling all events."""
        with self.__lock:
            self.__run_jobs = False
        self.__queue.join()
        self.__worker.join()

    def schedule_dump_job(self) -> None:
        """Enforces to dump the underlying DB, if no job is hanging."""
        if self.__queue.empty():
            self.__queue.put(time.time())

    def __dump_job(self) -> None:
        """Dumps the database."""
        timeout: float = 0.5  # Wait 500 ms before next try
        run_loop = True
        while run_loop:
            with self.__lock:
                run_loop = self.__run_jobs
            try:
                _ = self.__queue.get(timeout=timeout)
                self.__db.dump()
            except queue.Empty:
                pass  # it is ok to pass here. The queue might be full in next run
