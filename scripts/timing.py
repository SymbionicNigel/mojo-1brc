from cProfile import Profile
import os, pstats, pathlib
from pstats import SortKey
import time
from typing import IO, Any, Callable
from functools import wraps


def timingTool(
    profile: bool = False,
    storeInRecords: Callable[[list[float]], None] | None = None,
    saveStats: bool = False,
    runs: int = 1,
):
    def timingTool(
        func: Callable[[], bool],
    ):
        @wraps(func)
        def wrapper():

            def profileFunc(statsFilePath: str | None):
                with Profile() as profiler:

                    if not profile:
                        profiler.disable()

                    times: list[float] = []

                    for i in range(runs):
                        t0 = time.time()

                        func()
                        t1 = time.time()
                        print(
                            f"{func.__name__} call #{i} ran in {(t1-t0):10.4f} seconds"
                        )
                        times.append(t1 - t0)

                    if profile:
                        profiler.disable()

                        def printFinalStats(stream: IO[Any] | None):
                            printStats = pstats.Stats(
                                profiler, stream=stream
                            ).sort_stats(SortKey.TIME)
                            printStats.print_stats()

                        assert (not statsFilePath) or os.path.exists(statsFilePath)
                        if statsFilePath:
                            with open(statsFilePath, "w") as stream:
                                printFinalStats(stream=stream)
                                printFinalStats(stream=None)
                        else:
                            printFinalStats(None)

                        _ = storeInRecords and storeInRecords(times)

            saveStatsFilepath = None
            if saveStats or storeInRecords:
                statsDirectory = pathlib.Path.cwd().joinpath("./profilerData/")
                if not os.path.exists(statsDirectory):
                    os.mkdir(statsDirectory)
                assert os.path.exists(statsDirectory)
                saveStatsFilepath = f"{statsDirectory}/{int(time.time())}.txt"
                with open(saveStatsFilepath, "w") as _stats:
                    pass
            profileFunc(saveStatsFilepath)

            return

        return wrapper

    return timingTool
