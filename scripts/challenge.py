from argparse import ArgumentParser
from cProfile import Profile
from fileinput import filename
import os, pstats, pathlib
from pstats import SortKey
from sre_constants import ANY
import time
from typing import IO, Any, Callable
from functools import wraps


def timingTool(
    profile: bool = False,
    storeInRecords: bool = False,
    saveStats: bool = False,
):
    def timingTool(
        func: Callable[[], Any],
    ):
        @wraps(func)
        def wrapper():

            def profileFunc(statsFilePath: str | None):
                with Profile() as profiler:

                    if not profile:
                        profiler.disable()

                    t0 = time.time()
                    func()
                    t1 = time.time()
                    print(f"{func.__name__} ran in {(t1-t0):10.4f} seconds")

                    if profile:
                        profiler.disable()

                        def printFinalStats(stream: IO[Any] | None):
                            printStats = pstats.Stats(
                                profiler, stream=stream
                            ).sort_stats(SortKey.CUMULATIVE)
                            printStats.print_stats()

                        assert (not statsFilePath) or os.path.exists(statsFilePath)
                        if statsFilePath:
                            with open(statsFilePath, "w") as stream:
                                printFinalStats(stream=stream)
                        else:
                            printFinalStats(None)

                        if storeInRecords:
                            recordsPath = pathlib.Path.cwd().joinpath("./records.csv")
                            with open(recordsPath, mode="t+a") as recordFile:
                                recordFile.write(f"{time.time()},{(t1-t0):10.4f}\n")

                        # TODO: give the option to flush the profile results to a file in a structured format to be displayed in the readme. Consider using https://pypi.org/project/pytablewriter/

            saveStatsFilepath = None
            if saveStats:
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


@timingTool(profile=True, storeInRecords=True, saveStats=True)
def runChallenge():
    time.sleep(1)
    return


if __name__ == "__main__":
    argParser = ArgumentParser(prog="Billion Row Challenge Python attempt")
    runChallenge()
