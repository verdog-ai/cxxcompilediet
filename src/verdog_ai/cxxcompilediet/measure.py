"""Per-TU compile cost: a compiler launcher and the build's summary.

CMake runs every compile and link through this module (its
``CMAKE_CXX_COMPILER_LAUNCHER`` and ``CMAKE_CXX_LINKER_LAUNCHER`` are
``<python> -m verdog_ai.cxxcompilediet.measure``). The
wrapper appends one JSON line per command to ``$CXXCOMPILEDIET_LOG``: the output
file, start and end time and the maximum RSS of the compiler's processes
(``cc1plus``, or the LTO link's ``lto1``), as ``wait4`` reports it.
"""

import json
import os
import subprocess
import sys
import time
from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict, cast


class Record(TypedDict):
    """One compile or link command."""

    out: str
    start: float
    end: float
    rss_mb: float


class Summary(TypedDict):
    """The metrics of one build; lower is better for all of them."""

    peak_rss_mb: float
    max_tu_rss_mb: float
    sum_tu_seconds: float
    build_seconds: float


METRICS = tuple(Summary.__annotations__)


def _output(argv: list[str]) -> str:
    if "-o" in argv[:-1]:
        return argv[argv.index("-o") + 1]
    return " ".join(argv[-1:])


def wrap() -> None:
    """Run the command in ``sys.argv[1:]`` and log its cost."""
    argv = sys.argv[1:]
    start = time.time()
    proc = subprocess.Popen(argv)
    _, status, usage = os.wait4(proc.pid, 0)
    log = os.environ.get("CXXCOMPILEDIET_LOG")
    if log:
        record = Record(
            out=_output(argv),
            start=start,
            end=time.time(),
            rss_mb=usage.ru_maxrss / 1024,
        )
        # One short O_APPEND write per line: parallel wrappers do not mix.
        with open(log, "a") as f:
            f.write(json.dumps(record) + "\n")
    sys.exit(os.waitstatus_to_exitcode(status))


def read(log: Path) -> list[Record]:
    """The records of a build log."""
    lines = log.read_text().splitlines() if log.exists() else []
    return [Record(**json.loads(line)) for line in lines]


def peak(records: Iterable[Record]) -> float:
    """Peak of the summed RSS of the commands that run at the same time.

    Each command counts with its maximum RSS for its whole run, so this is
    an upper bound of the build's peak memory at its parallelism.
    """
    events = sorted(
        ev
        for r in records
        for ev in ((r["start"], 1, r["rss_mb"]), (r["end"], 0, -r["rss_mb"]))
    )
    # Ends sort before starts at the same instant.
    current = best = 0.0
    for _, _, delta in events:
        current += delta
        best = max(best, current)
    return best


def summarize(records: list[Record], build_seconds: float) -> Summary:
    """The build's metrics from its records."""
    return Summary(
        peak_rss_mb=peak(records),
        max_tu_rss_mb=max((r["rss_mb"] for r in records), default=0.0),
        sum_tu_seconds=sum(r["end"] - r["start"] for r in records),
        build_seconds=build_seconds,
    )


def heaviest(records: list[Record], n: int) -> str:
    """A table of the ``n`` heaviest commands by RSS, with their time."""
    rows = sorted(records, key=lambda r: -r["rss_mb"])[:n]
    return "\n".join(
        f"{r['rss_mb']:8.0f} MB {r['end'] - r['start']:7.1f} s  {r['out']}"
        for r in rows
    )


def value(summary: Summary, metric: str) -> float:
    """The metric named ``metric`` of ``summary``."""
    return cast(dict[str, float], summary)[metric]


if __name__ == "__main__":
    wrap()
