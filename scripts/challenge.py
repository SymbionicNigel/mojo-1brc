from argparse import ArgumentParser
from cProfile import Profile
from multiprocessing import Manager, Pool
import os, pstats, pathlib
from pstats import SortKey
import time
from typing import IO, Any, Callable
from functools import wraps

FILEPATH = "./.test_resources/test_data_kilo.txt"


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
                                printFinalStats(stream=None)
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


class LocationData:
    __slots__ = "min_temp", "max_temp", "count", "sum_temp", "loc_str"
    min_temp: float
    max_temp: float
    count: int
    sum_temp: float
    loc_str: str


class Challenge:
    manager = Manager()

    def __init__(self) -> None:
        self.data = self.manager.dict()

    def readFile(self):
        def callback(objs: Any):
            print("callback", len(objs))
            for idx, obj in enumerate(objs):
                try:
                    self.mergeData(obj)
                except Exception as e:
                    print(e)
            print(len(self.data.keys()))

        def error_callback(obj: BaseException):
            print("error_callback", obj)

        def fileIterator():
            with open(FILEPATH) as dataFile:
                while lineGroup := dataFile.readlines(4096):
                    yield lineGroup

        fileIter = fileIterator()
        x = None
        with Pool() as p:
            x = p.map_async(
                self.readFileIter,
                fileIter,
                chunksize=10,
                callback=callback,
                error_callback=error_callback,
            )

            x.wait()

    def readFileIter(self, lineGroups: list[str]):
        workingData = {}
        print(len(lineGroups))
        for line in lineGroups:
            location, temp_str = line.removesuffix("\n").split(";")
            self.upsert_row(location.capitalize(), float(temp_str), workingData)
        return workingData

    def mergeData(self, itemToMerge):
        print(sum(x["count"] for x in itemToMerge.values()))
        for location, partial in itemToMerge.items():
            if location not in self.data:
                self.data[location] = partial
            else:
                # print("else")
                if self.data[location]["max_temp"] < partial["max_temp"]:
                    self.data[location]["max_temp"] = partial["max_temp"]
                if self.data[location]["min_temp"] > partial["min_temp"]:
                    self.data[location]["min_temp"] = partial["min_temp"]
                # with workingData
                self.data[location]["count"] += partial["count"]
                self.data[location]["sum_temp"] += partial["sum_temp"]

    def upsert_row(self, location: str, temperature: float, workingData: Any):
        if location not in workingData:
            workingData[location] = {
                "loc_str": location,
                "max_temp": temperature,
                "min_temp": temperature,
                "sum_temp": temperature,
                "count": 1,
            }
        else:
            tempData = workingData[location]
            if workingData[location]["max_temp"] < temperature:
                tempData["max_temp"] = temperature
            if workingData[location]["min_temp"] > temperature:
                tempData["min_temp"] = temperature
            tempData["count"] += 1
            tempData["sum_temp"] += temperature
            workingData[location] = tempData

    def sort_and_print(self):
        for location in sorted(self.data.keys()):
            self.print_row(
                location=self.data[location]["loc_str"],
                min_temp=self.data[location]["min_temp"],
                max_temp=self.data[location]["max_temp"],
                average=(
                    self.data[location]["sum_temp"] / self.data[location]["count"]
                ),
                count=self.data[location]["count"],
            )
        print(sum(x["count"] for x in self.data.values()))

    def print_row(
        self,
        location: str,
        min_temp: float,
        max_temp: float,
        average: float,
        count: int,
    ):
        print(f"{location},{min_temp},{max_temp},{average},{count}")


@timingTool(profile=False, storeInRecords=False, saveStats=False)
def runChallenge():
    x = Challenge()
    x.readFile()
    x.sort_and_print()
    return


if __name__ == "__main__":
    argParser = ArgumentParser(prog="Billion Row Challenge Python attempt")
    runChallenge()
