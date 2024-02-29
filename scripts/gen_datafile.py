import math, random, string, os, time
from dataclasses import dataclass
from enum import auto, StrEnum
from multiprocessing import Pool
from typing import Iterator


class ConfigNames(StrEnum):
    KILO = auto()
    PERCENT = auto()
    FULL = auto()


@dataclass
class TestFileConfig:
    total_rows: int
    unique_locations: int
    range: tuple[float, float]
    configName: ConfigNames


TEMP_RANGE = (-99.9, 99.9)

CONFIGS: dict[ConfigNames, TestFileConfig] = {
    ConfigNames.KILO: TestFileConfig(1_000, 50, TEMP_RANGE, ConfigNames.KILO),
    ConfigNames.PERCENT: TestFileConfig(
        10_000_000, 10_00, TEMP_RANGE, ConfigNames.PERCENT
    ),
    ConfigNames.FULL: TestFileConfig(
        1_000_000_000, 10_000, TEMP_RANGE, ConfigNames.FULL
    ),
}


class TestFileGen:
    config: TestFileConfig
    keys: list[str] = []
    rows: list[str] = []
    pageSize: int = 16_000
    directory = "./.test_resources"
    filenamePrefix = "test_data"
    rowsProcessed = 0
    iterations: Iterator[int]

    def __init__(self, config: TestFileConfig) -> None:
        t0 = time.time()
        self.config = config
        self.generateKeys()
        self.cleanFiles()
        self.iterations = iter(
            range(math.ceil(self.config.total_rows / self.pageSize) - 1)
        )

        with Pool() as p:
            self.rowsProcessed = sum(p.map(self.runIteration, self.iterations))

        self.rowsProcessed += self.runIteration(
            math.ceil(self.config.total_rows / self.pageSize), True
        )
        assert self.rowsProcessed == self.config.total_rows
        t1 = time.time()
        print(
            f"{self.rowsProcessed} generated in {t1 - t0} seconds pagesize {self.pageSize}"
        )

    def runIteration(self, _: int, lastRun: bool = False):
        newRows = self.generateRows()
        self.writeToFile(newRows, lastRun)
        return len(newRows)

    def _generateLocationName(self, stringLength: int):
        return "".join(random.choices(string.ascii_letters, k=stringLength))

    def _generateManyLocationNames(self, count: int):
        return [
            self._generateLocationName(random.randrange(1, 100)) for _ in range(count)
        ]

    def generateKeys(self):
        self.keys.clear()
        workingKeys: set[str] = set()
        while len(workingKeys) < self.config.unique_locations:
            workingKeys.update(
                self._generateManyLocationNames(
                    self.config.unique_locations - len(workingKeys)
                )
            )

        assert len(workingKeys) == self.config.unique_locations
        self.keys = list(workingKeys)

    def generateFilename(self):
        return f"{self.directory}/{self.filenamePrefix}_{self.config.configName}.txt"

    def generateRow(self, keyList: list[str]):
        randIndex = random.randint(0, self.config.unique_locations)
        return f"{keyList[randIndex - 1]};{round(random.uniform(self.config.range[0], self.config.range[1]), 1)}"

    def generateRows(self):
        currentPagesSize = (
            self.pageSize
            if self.pageSize < self.config.total_rows - self.rowsProcessed
            else self.config.total_rows - self.rowsProcessed
        )
        return [self.generateRow(self.keys) for _ in range(currentPagesSize)]

    def cleanFiles(self):
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        assert os.path.exists(self.directory)
        if os.path.exists(self.generateFilename()):
            os.remove(self.generateFilename())
        assert not os.path.exists(self.generateFilename())
        with open(self.generateFilename(), "w"):
            pass
        assert os.path.exists(self.generateFilename())

    def writeToFile(self, linesToWrite: list[str], lastRun: bool):
        assert os.path.exists(self.directory), f"Directory Not Found: {self.directory}"
        assert os.path.exists(
            self.generateFilename()
        ), f"File Not Found, filename {self.generateFilename()}"
        with open(self.generateFilename(), "a") as file_obj:
            file_obj.write(
                "\n".join(linesToWrite) + ("" if lastRun else "\n"),
            )


def main():
    [TestFileGen(config=config) for config in CONFIGS.values()]


if __name__ == "__main__":
    main()
