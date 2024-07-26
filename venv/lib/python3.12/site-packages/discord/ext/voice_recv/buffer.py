# -*- coding: utf-8 -*-

from __future__ import annotations

import time
import heapq
import threading

from typing import (
    TYPE_CHECKING,
    overload,
    Protocol,
    Generic,
    TypeVar,
    Optional,
    List,
    Sequence,
    Tuple,
    Callable,
)

from .rtp import _PacketCmpMixin

if TYPE_CHECKING:
    from typing import Literal, Optional, List
    from .rtp import RTPPacket

__all__ = [
    'HeapJitterBuffer',
]


_T = TypeVar('_T')
PacketT = TypeVar('PacketT', bound=_PacketCmpMixin)


class Buffer(Protocol[_T]):
    """The base class representing a simple buffer with no extra features."""

    # fmt: off
    def __len__(self) -> int: ...
    def push(self, item: _T) -> None: ...
    def pop(self) -> Optional[_T]: ...
    def peek(self) -> Optional[_T]: ...
    def flush(self) -> List[_T]: ...
    def reset(self) -> None: ...
    # fmt: on


class RetainingBuffer(Buffer[_T], Protocol):
    """A buffer that retains an arbitrary number of items."""

    maxsize: int
    prefsize: int
    prefill: int


class SortedBuffer(Buffer[_T], Protocol):
    """A buffer that maintains a sorted internal state."""


class WindowedBuffer(Buffer[_T], Protocol):
    """A buffer with arbitrarily windowed output."""

    window_start: float
    window_end: float

    # fmt: off
    def pop(self) -> List[_T]: ...
    def peek(self) -> Optional[List[_T]]: ...
    def flush(self) -> List[List[_T]]: ...
    # fmt: on


class BaseBuffer(Buffer[PacketT]):
    """A basic buffer."""

    def __init__(self):
        self._buffer: List[PacketT] = []

    def __len__(self) -> int:
        return len(self._buffer)

    def push(self, item: PacketT) -> None:
        self._buffer.append(item)

    def pop(self) -> Optional[PacketT]:
        return self._buffer.pop()

    def peek(self) -> Optional[PacketT]:
        return self._buffer[-1] if self._buffer else None

    def flush(self) -> List[PacketT]:
        buf = self._buffer.copy()
        self._buffer.clear()
        return buf

    def reset(self) -> None:
        self._buffer.clear()


class RetensionBuffer(BaseBuffer[PacketT], RetainingBuffer):
    def __init__(self, maxsize: int = 10, *, prefsize: int = 1, prefill: int = 1):
        if maxsize < 1:
            raise ValueError(f'maxsize ({maxsize}) must be greater than 0')

        if not 0 <= prefsize <= maxsize:
            raise ValueError(f'prefsize must be between 0 and maxsize ({maxsize})')

        super().__init__()
        self.maxsize: int = maxsize
        self.prefsize: int = prefsize
        self.prefill: int = prefill


class HeapJitterBuffer(BaseBuffer[PacketT], RetainingBuffer):
    """Push item in, pop items out"""

    def __init__(self, maxsize: int = 10, *, prefsize: int = 1, prefill: int = 1):
        if maxsize < 1:
            raise ValueError(f'maxsize ({maxsize}) must be greater than 0')

        if not 0 <= prefsize <= maxsize:
            raise ValueError(f'prefsize must be between 0 and maxsize ({maxsize})')

        self.maxsize: int = maxsize
        self.prefsize: int = prefsize
        self.prefill: int = prefill
        self._prefill: int = prefill

        self._last_rx: int = 0
        self._last_tx: int = 0
        self._generation: int = 0
        self._generation_ts: int = 0

        self._has_item: threading.Event = threading.Event()
        # I sure hope I dont need to add a lock to this
        self._buffer: List[tuple[int, RTPPacket]] = []

    def __len__(self) -> int:
        return len(self._buffer)

    def _push(self, packet: RTPPacket, seq: int) -> None:
        heapq.heappush(self._buffer, (seq, packet))

    def _pop(self) -> RTPPacket:
        return heapq.heappop(self._buffer)[1]

    def _get_packet_if_ready(self) -> Optional[RTPPacket]:
        return self._buffer[0][1] if len(self._buffer) > self.prefsize else None

    def _pop_if_ready(self) -> Optional[RTPPacket]:
        return self._pop() if len(self._buffer) > self.prefsize else None

    def _update_has_item(self) -> None:
        prefilled = self._prefill == 0
        packet_ready = len(self._buffer) > self.prefsize

        if not prefilled or not packet_ready:
            self._has_item.clear()
            return

        sequential = self._last_tx + 1 == self._buffer[0][0]
        positive_seq = self._last_tx > 0 or self._generation > 0

        # We have the next packet ready
        # OR we havent sent a packet out yet
        # OR the buffer is full
        if (sequential and positive_seq) or not positive_seq or len(self._buffer) >= self.maxsize:
            self._has_item.set()
        else:
            self._has_item.clear()

    def _cleanup(self) -> None:
        while len(self._buffer) > self.maxsize:
            heapq.heappop(self._buffer)

        while self._buffer and self._buffer[0][0] <= self._last_tx:
            heapq.heappop(self._buffer)

    def _get_seq(self, packet: RTPPacket) -> int:
        return packet.sequence + 65536 * self._generation

    def push(self, packet: RTPPacket) -> bool:
        """
        Push a packet into the buffer.  If the packet would make the buffer
        exceed its maxsize, the oldest packet will be dropped.
        """

        seq = self._get_seq(packet)

        # if the seq has rolled over, it'll be ~65535 lower than the generation ts
        if seq + 32768 < self._last_rx and packet.timestamp > self._generation_ts:
            self._generation += 1
            self._generation_ts = packet.timestamp
            seq = self._get_seq(packet)

        # Ignore the packet if its too old
        if seq <= self._last_rx and self._last_rx > 0:
            return False

        self._push(packet, seq)

        if self._prefill > 0:
            self._prefill -= 1

        self._last_rx = seq

        self._cleanup()
        self._update_has_item()

        return True

    @overload
    def pop(self, *, timeout: float = 1.0) -> Optional[RTPPacket]:
        ...

    @overload
    def pop(self, *, timeout: Literal[0]) -> Optional[RTPPacket]:
        ...

    def pop(self, *, timeout=1.0):
        """
        If timeout is a positive number, wait as long as timeout for a packet
        to be ready and return that packet, otherwise return None.
        """

        ok = self._has_item.wait(timeout)
        if not ok:
            return None

        if self._prefill > 0:
            return None

        # This function should actually be redundant but i'll leave it for now
        packet = self._pop_if_ready()

        if packet is not None:
            self._last_tx = self._get_seq(packet)

        self._update_has_item()
        return packet

    def peek(self, *, all: bool = False) -> Optional[RTPPacket]:
        """
        Returns the next packet in the buffer only if it is ready, meaning it can
        be popped. When `all` is set to True, it returns the next packet, if any.
        """

        if not self._buffer:
            return None

        if all:
            return self._buffer[0][1]
        else:
            return self._get_packet_if_ready()

    def peek_next(self) -> Optional[RTPPacket]:
        """
        Returns the next packet in the buffer only if it is sequential.
        """

        packet = self.peek(all=True)

        if packet and self._get_seq(packet) == self._last_tx + 1:
            return packet

    def gap(self) -> int:
        """
        Returns the number of missing packets between the last packet to be
        popped and the currently held next packet.  Returns 0 otherwise.
        """

        if self._buffer and self._last_tx > 0:
            return self._buffer[0][0] - self._last_tx + 1

        return 0

    def flush(self) -> List[RTPPacket]:
        """
        Return all remaining packets.
        """

        packets = [p for (_, p) in sorted(self._buffer)]
        self._buffer.clear()

        if packets:
            self._last_tx = packets[-1].sequence

        self._generation = self._generation_ts = 0
        self._prefill = self.prefill
        self._has_item.clear()

        return packets

    def reset(self) -> None:
        """
        Clear buffer and reset internal counters.
        """

        self._buffer.clear()
        self._has_item.clear()
        self._prefill = self.prefill
        self._last_tx = self._last_rx = self._generation = self._generation_ts = 0


class WindowBuffer(Generic[PacketT]):
    def __init__(self, window_duration: float, *, time_func: Callable[[], float] = time.time):
        self.window_duration: float = window_duration
        self.time = time_func

        self._buffer: List[Tuple[PacketT, float]] = []
        self._start: float = 0
        self._current_window: int = 1
        self._lock = threading.Lock()

        self.add_item = self._add_once

    @property
    def window_start(self) -> float:
        return self._start + self._current_window * self.window_duration

    @property
    def window_end(self) -> float:
        return self.window_start + self.window_duration

    def _add_once(self, item: PacketT) -> None:
        self._start = self.time()
        self.add_item = self._add_item
        return self.add_item(item)

    def _add_item(self, item: PacketT) -> None:
        with self._lock:
            self._buffer.append((item, self.time()))

    # stub
    def add_item(self, item: PacketT) -> None:
        pass

    def reset(self) -> None:
        with self._lock:
            self._buffer.clear()
            self._start = 0
            self._current_window = 1
            self.add_item = self._add_once

    def get_last_window_number(self) -> int:
        return self._current_window - 1

    def get_window_number_at(self, when: Optional[float] = None) -> int:
        # TODO: check to see if this logic is sane
        return int(((when or self.time()) - self._start) / self.window_duration)

    def get_time_until_current_window_end(self) -> float:
        return self.window_end - self.time()

    def get_next_window(self, *, skip_empty: bool = False) -> Sequence[PacketT]:
        time.sleep(self.get_time_until_current_window_end())

        with self._lock:
            window = None
            while not window:
                window = self._generate_window()
                self._current_window += 1
                if not skip_empty:
                    break
        return window

    def _generate_window(self) -> List[PacketT]:
        window = []

        # I could just splice the list and not do this dumb copy but eh
        for pair in self._buffer.copy():
            item, when = pair
            if self.window_start <= when < self.window_end:
                window.append(item)
                self._buffer.remove(pair)

        return window

    @classmethod
    def sync(cls, *buffers: WindowBuffer, start_time: float) -> None:
        for buffer in buffers:
            buffer.reset()
            buffer.add_item = buffer._add_item
            buffer._start = start_time


# 1. Basic buffer with max size/retention capabilities
# 2. Sorted buffer?
# 3. Windowed buffer
# 4. Controller for grouping and syncing multiple buffers (for muxer etc)
