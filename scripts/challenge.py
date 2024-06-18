from argparse import ArgumentParser
from multiprocessing import Pool
import statistics
import traceback
from typing import Any, Generator, Self
from functools import reduce
from scripts.tables import AttemptData, TableUpdater
from timing import timingTool

FILEPATH = "./.test_resources/test_data_full.txt"
RUNS = 3


class LocationData:
    __slots__ = "min_temp", "max_temp", "count", "sum_temp", "loc_str"
    min_temp: float
    max_temp: float
    count: int
    sum_temp: float
    loc_str: str

    def __init__(self, loc_str: str, temp: float) -> None:
        self.loc_str = loc_str
        self.max_temp = temp
        self.min_temp = temp
        self.sum_temp = temp
        self.count = 1

    def merge(self, temperature: float):
        if self.max_temp < temperature:
            self.max_temp = temperature
        if self.min_temp > temperature:
            self.min_temp = temperature
        self.count += 1
        self.sum_temp += temperature

    def mergeComplex(self, mergedData: Self):
        if self.max_temp < mergedData.max_temp:
            self.max_temp = mergedData.max_temp
        if self.min_temp > mergedData.min_temp:
            self.min_temp = mergedData.min_temp
        self.count += mergedData.count
        self.sum_temp += mergedData.sum_temp


fileDone = False


class Challenge:

    def __init__(self) -> None:
        self.data: dict[str, LocationData] = {}

    def readFile(self):

        global fileDone

        def fileIterator() -> Generator[list[str], Any, None]:
            with open(FILEPATH) as dataFile:
                while lineGroup := dataFile.readlines(4096):
                    yield lineGroup

        fileIter = fileIterator()

        def filePortionIterator(filePortion: int) -> Generator[list[str], Any, None]:
            iters = 0
            while True:
                if iters == 90_000:
                    # TODO: Need to look into how this will affect the memory of the program over the runtime of the script did not make it all the way through the full script
                    break
                iters += 1
                try:
                    yield next(fileIter)
                except StopIteration:
                    global fileDone
                    fileDone = True
                    break
            print(f"Portion {filePortion}, final iters {iters}")

        with Pool() as p:
            i = 1
            while not fileDone:

                reduce(
                    self.mergeData,
                    p.imap(
                        self.readFileIter,
                        filePortionIterator(i),
                        chunksize=12500,
                    ),
                    self.data,
                )
                i += 1
        return self

    def readFileIter(self, lineGroups: list[str]):
        workingData: dict[str, LocationData] = {}
        for line in lineGroups:
            location, temp_str = line.removesuffix("\n").split(";")
            self.upsert_row(location.capitalize(), float(temp_str), workingData)
        return workingData

    def mergeData(
        self,
        fullData: dict[str, LocationData],
        itemToMerge: dict[str, LocationData],
    ):
        for location, partial in itemToMerge.items():
            if location not in fullData:
                fullData[location] = partial
            else:
                fullData[location].mergeComplex(partial)
        return fullData

    def upsert_row(
        self, location: str, temperature: float, workingData: dict[str, LocationData]
    ):
        if location not in workingData:
            workingData[location] = LocationData(location, temperature)
        else:
            workingData[location].merge(temperature)

    def sort_and_print(self):
        for location in sorted(self.data.values(), key=lambda x: x.loc_str):
            self.print_row(loc_data=location)

    def print_row(self, loc_data: LocationData):
        print(
            f"{loc_data.loc_str},{loc_data.min_temp},{loc_data.max_temp},{(loc_data.sum_temp / loc_data.count):3.1f}"
        )


def storeInRecords(
    runtimes: list[float],
):
    current_commit = TableUpdater.get_current_commit_data()
    TableUpdater(
        AttemptData(
            commit_id=current_commit[0],
            short_commit_id=current_commit[1],
            runs=len(runtimes),
            average_run_time=statistics.mean(runtimes),
            note=input("Add notes on this run please: "),
            row_count=0,
        )
    )


@timingTool(profile=False, storeInRecords=storeInRecords, saveStats=False, runs=RUNS)
def runChallenge():
    success = False
    try:
        Challenge().readFile().sort_and_print()
        success = True
    except Exception:
        traceback.print_exc()
    finally:
        return success


if __name__ == "__main__":
    argParser = ArgumentParser(prog="Billion Row Challenge Python attempt")
    runChallenge()
