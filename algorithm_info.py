"""
algorithm.py

Pure algorithm implementations for disk scheduling.
Provides:
 - DiskScheduler class with methods: fcfs, sstf, scan, cscan, look, clook
 - Each method returns a tuple: (order, total_movement, average_movement, per_step_movements)
 - Helper functions available for standalone use.

This module is written to match and improve the behavior in the provided `disk_scheduler.py`.
"""
from typing import List, Tuple, Optional


def _compute_metrics(start: int, order: List[int]) -> Tuple[int, float, List[int]]:
    """Compute total movement, average movement, and a list of per-step movements.

    Args:
        start: starting head position
        order: ordered list of visited track positions (each element is an int)

    Returns:
        (total_movement, average_movement, per_step_movements)
    """
    if not order:
        return 0, 0.0, []
    pos = start
    moves = []
    for p in order:
        moves.append(abs(p - pos))
        pos = p
    total = sum(moves)
    avg = total / len(moves)
    return total, avg, moves


class DiskScheduler:
    """
    DiskScheduler holds a request list and a starting head position and exposes
    methods implementing classic disk scheduling algorithms.

    Each algorithm returns:
        (service_order, total_movement, average_movement, per_step_movements)

    Notes:
     - If disk_size is provided, SCAN/C-SCAN behave using disk ends (0 and disk_size-1).
     - For C-SCAN and C-LOOK the 'jump' is treated as literal movement in metrics
       if disk_size is provided (C-SCAN jump moves across entire disk; C-LOOK
       jump moves between last and first request).
     - Methods do not modify the original request list.
    """

    def __init__(self, requests: List[int], head: int, disk_size: Optional[int] = None):
        self.requests = list(requests)
        self.head = int(head)
        self.disk_size = None if disk_size is None else int(disk_size)

    # -------------------------
    # Basic algorithms
    # -------------------------
    def fcfs(self) -> Tuple[List[int], int, float, List[int]]:
        """First-Come First-Served: service in the given request order."""
        order = list(self.requests)
        total, avg, moves = _compute_metrics(self.head, order)
        return order, total, avg, moves

    def sstf(self) -> Tuple[List[int], int, float, List[int]]:
        """Shortest Seek Time First: always pick closest pending request."""
        pending = set(self.requests)
        pos = self.head
        order = []
        while pending:
            # choose the pending request with minimum absolute distance to current head
            closest = min(pending, key=lambda x: abs(x - pos))
            order.append(closest)
            pending.remove(closest)
            pos = closest
        total, avg, moves = _compute_metrics(self.head, order)
        return order, total, avg, moves

    # -------------------------
    # SCAN / C-SCAN / LOOK / C-LOOK
    # -------------------------
    def scan(self, direction: str = "up") -> Tuple[List[int], int, float, List[int]]:
        """
        SCAN (elevator): head moves in `direction` (up => increasing track numbers)
        servicing requests along the way, goes to disk end (0 or disk_size-1) then reverses.
        If disk_size is None, the effective end is the max/min of requests (so reverse at end of requests).
        """
        if not self.requests:
            return [], 0, 0.0, []

        if direction not in ("up", "down"):
            raise ValueError("direction must be 'up' or 'down'")

        size = self.disk_size
        left = sorted([r for r in self.requests if r < self.head])
        right = sorted([r for r in self.requests if r >= self.head])

        order: List[int] = []

        if direction == "up":
            # service right side first (including any requests at head)
            order.extend(right)
            # go to disk end if disk_size provided (to simulate full scan)
            if size is not None:
                order.append(size - 1)
            # then service left side in descending order
            order.extend(reversed(left))
        else:
            order.extend(reversed(left))
            if size is not None:
                order.append(0)
            order.extend(right)

        total, avg, moves = _compute_metrics(self.head, order)
        return order, total, avg, moves

    def cscan(self, direction: str = "up") -> Tuple[List[int], int, float, List[int]]:
        """
        C-SCAN (circular SCAN): head moves in one direction to the end, then jumps
        to the other end and continues in the same direction.
        If disk_size is provided, the jump is represented in the order as traveling to the end
        and then to the start so metrics reflect that traversal. If disk_size is None,
        the jump movement is simulated between the last request on the traveled side to
        the first request on the opposite side.
        """
        if not self.requests:
            return [], 0, 0.0, []

        if direction not in ("up", "down"):
            raise ValueError("direction must be 'up' or 'down'")

        size = self.disk_size
        left = sorted([r for r in self.requests if r < self.head])
        right = sorted([r for r in self.requests if r >= self.head])

        order: List[int] = []

        if direction == "up":
            # service from head upward
            order.extend(right)
            if size is not None:
                # sweep to disk end, then jump to start (simulate by visiting end then start)
                order.append(size - 1)
                order.append(0)
                # after jump, service left side in ascending order
                order.extend(left)
            else:
                # no explicit disk ends: simulate jump from max(right) (or head if right empty)
                # to min(left)
                if left:
                    order.extend(left)
        else:
            # direction == down: service left side (descending)
            order.extend(reversed(left))
            if size is not None:
                order.append(0)
                order.append(size - 1)
                order.extend(reversed(right))
            else:
                if right:
                    order.extend(reversed(right))

        total, avg, moves = _compute_metrics(self.head, order)
        return order, total, avg, moves

    def look(self, direction: str = "up") -> Tuple[List[int], int, float, List[int]]:
        """
        LOOK: similar to SCAN but head reverses at the last request on that side,
        it does not go to the physical disk end unless requests exist there.
        """
        if not self.requests:
            return [], 0, 0.0, []

        if direction not in ("up", "down"):
            raise ValueError("direction must be 'up' or 'down'")

        left = sorted([r for r in self.requests if r < self.head])
        right = sorted([r for r in self.requests if r >= self.head])

        order: List[int] = []
        if direction == "up":
            order.extend(right)
            # reverse and service left (highest to lowest)
            order.extend(reversed(left))
        else:
            order.extend(reversed(left))
            order.extend(right)

        total, avg, moves = _compute_metrics(self.head, order)
        return order, total, avg, moves

    def clook(self, direction: str = "up") -> Tuple[List[int], int, float, List[int]]:
        """
        C-LOOK: like C-SCAN but instead of going to disk end, jumps from the last request
        on the traveled side to the first request on the other side.
        When disk_size is provided, the jump is represented as a direct move between
        those requests (metrics count that distance).
        """
        if not self.requests:
            return [], 0, 0.0, []

        if direction not in ("up", "down"):
            raise ValueError("direction must be 'up' or 'down'")

        left = sorted([r for r in self.requests if r < self.head])
        right = sorted([r for r in self.requests if r >= self.head])

        order: List[int] = []
        if direction == "up":
            # service right ascending
            order.extend(right)
            # if there are left-side requests, jump to smallest left and continue
            if left:
                # represent the post-jump servicing sequence starting at left[0]
                order.append(left[0])
                order.extend(left[1:])
        else:
            # direction down: service left descending
            order.extend(reversed(left))
            if right:
                # after finishing left, jump to the largest right and continue descending through right
                order.append(right[-1])
                order.extend(reversed(right[:-1])) if len(right) > 1 else None

        total, avg, moves = _compute_metrics(self.head, order)
        return order, total, avg, moves


# -------------------------
# Convenience standalone functions (optional)
# -------------------------
def fcfs(requests: List[int], head: int) -> Tuple[List[int], int, float, List[int]]:
    return DiskScheduler(requests, head).fcfs()


def sstf(requests: List[int], head: int) -> Tuple[List[int], int, float, List[int]]:
    return DiskScheduler(requests, head).sstf()


def scan(requests: List[int], head: int, disk_size: Optional[int] = None, direction: str = "up"):
    return DiskScheduler(requests, head, disk_size=disk_size).scan(direction=direction)


def cscan(requests: List[int], head: int, disk_size: Optional[int] = None, direction: str = "up"):
    return DiskScheduler(requests, head, disk_size=disk_size).cscan(direction=direction)


def look(requests: List[int], head: int, direction: str = "up"):
    return DiskScheduler(requests, head).look(direction=direction)


def clook(requests: List[int], head: int, direction: str = "up"):
    return DiskScheduler(requests, head).clook(direction=direction)


# -------------------------
# Module test (run only when executed directly)
# -------------------------
if __name__ == "__main__":
    # quick sanity check
    sample_requests = [95, 180, 34, 119, 11, 123, 62, 64]
    head_pos = 50
    disk_size = 200

    ds = DiskScheduler(sample_requests, head_pos, disk_size=disk_size)

    for name, func in [
        ("FCFS", ds.fcfs),
        ("SSTF", ds.sstf),
        ("SCAN (up)", lambda: ds.scan(direction="up")),
        ("C-SCAN (up)", lambda: ds.cscan(direction="up")),
        ("LOOK (up)", lambda: ds.look(direction="up")),
        ("C-LOOK (up)", lambda: ds.clook(direction="up")),
    ]:
        order, total, avg, moves = func()
        print(f"\n{name}:")
        print(" Service order:", order)
        print(" Total head movement:", total)
        print(" Average per request:", round(avg, 2))
        print(" Per-step moves:", moves)
