import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Tuple, TypeVar, Optional

T = TypeVar('T')


@dataclass
class AbsRelTime:
    """Container for absolute, relative and time."""

    time: timedelta
    """The time this unit takes."""
    absolute: int
    """The number of elements in this unit."""
    percentage: float
    """The percentage of absolute through total."""


class ETA:
    __iterable: Any
    """The source of items inspected by this ETA instance."""
    __total: int
    """Number of total items that will be yielded by __iterator."""
    __done: int
    """Number of already yielded items."""
    __start_time: datetime
    """Time when this ETA started."""
    __auto_print: bool
    """Automatically print stats after each __next() call"""
    __overwrite: bool
    """Overwrite old stats line."""
    __file: bool
    """File for outputting stats."""

    @dataclass(frozen=True)
    class Stats:
        """Statistics about the current status of ETA."""

        total: AbsRelTime
        """Stats for completing all the task."""
        remaining: AbsRelTime
        """Stats for the remaining operations to complete the task."""
        done: AbsRelTime
        """Stats for operations that are already done."""
        eta: datetime
        """The guessed time when the task is completed."""

        def print_refresh(self, file: Optional[Any]):
            """Deletes the old line, prints this stats to file and flushes the stream."""
            print(f'\r{self}', end='', file=file, flush=True)

        def print(self, file: Optional[Any]):
            """Prints this stats to file and flushes the stream."""
            print(self, file=file, flush=True)

        def dict(self) -> dict:
            """"""
            return dataclasses.asdict(self)

        def json(self, **kwargs):
            return json.dumps(self.dict(), default=lambda x: str(x), **kwargs)

        def __str__(self):
            return (
                f'{self.done.absolute}/{self.total.absolute} = {self.done.percentage:.1f}%, '
                f'remaining {self.remaining.time}'
            )

    def __init__(
            self, iterable: Any, *,
            total: Optional[int] = None,
            auto_print: bool = True,
            overwrite: bool = True,
            file: Optional[Any] = None,
    ):
        """Creates a new ETA instance.

        Arguments:
            * iterable: An iterable object. If it has a __len__ property, you don't need to provide a value for total.
            * total: The total number of items in iterable. Pass a value for total if iterable does not have a
            __len__ property.
            * auto_print: If true, the stats of ETA will be printed after each loop run. i.e. after each __next()
            call. Set auto_print to false to disable automatic printing the stats.
            * overwrite: If true, overwrites the old stats with new stats instead of printing each stats in a
            separate line.
            * file: The file to print the output to. None means stdout. If you want to disable the automatic printing
            of stats, set auto_print to false.

        Examples:
            >>> data = list(range(3))
            >>> for num, _ in ETA(data, auto_print=False): print(num, end=' ')
            >>> 0 1 2
        """
        if total:
            self.__total = total
        elif hasattr(iterable, '__len__'):
            self.__total = len(iterable)
        else:
            raise TypeError('Expected iterable with __len__ property or total not None')
        self.__iterable = iter(iterable)
        self.__done = 0
        self.__start_time = datetime.now()
        self.__auto_print = auto_print
        self.__overwrite = overwrite
        self.__file = file

    def __iter__(self):
        # ETA is already an iterator, so return self
        return self

    def __next__(self) -> Tuple[T, Stats]:
        self.__done += 1
        # Get next item from inner iterable
        iterable_next_item = next(self.__iterable)
        # Calculate new stats
        stats = self.stats()
        # Prints stats if desired
        if self.__auto_print and self.__overwrite:
            stats.print_refresh(self.__file)
        elif self.__auto_print and not self.__overwrite:
            stats.print(self.__file)
        return iterable_next_item, stats

    def stats(self) -> Stats:
        """Returns statistics about the current status of ETA."""
        elapsed_since_start = datetime.now() - self.__start_time
        duration_per_operation = elapsed_since_start / self.__done
        remaining_absolute = self.__total - self.__done
        remaining_time = duration_per_operation * remaining_absolute

        return self.Stats(
            total=AbsRelTime(
                time=duration_per_operation * self.__total,
                absolute=self.__total,
                percentage=100
            ),
            remaining=AbsRelTime(
                time=remaining_time,
                absolute=remaining_absolute,
                percentage=(remaining_absolute / self.__total) * 100
            ),
            done=AbsRelTime(
                time=duration_per_operation * self.__done,
                absolute=self.__done,
                percentage=(self.__done / self.__total) * 100
            ),
            eta=datetime.now() + remaining_time
        )
