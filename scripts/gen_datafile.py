import math, random, string, os, time, sys
from multiprocessing import Pool
from typing import Iterator
from argparse import ArgumentParser
from scripts.test_file_configs import CONFIGS, TEST_FILE_DIR, ConfigNames, TestFileConfig, generateFilename


class TestFileGen:
    config: TestFileConfig
    keys: list[str] = []
    pageSize: int = 16_000
    rowsProcessed = 0
    iterations: Iterator[int]
    filename: str

    def __init__(self, config: TestFileConfig) -> None:
        t0 = time.time()
        self.config = config
        self.filename = generateFilename(self.config)
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
            f"{self.rowsProcessed:12} rows generated over {(t1 - t0):8.4f} seconds with a pagesize of {self.pageSize}"
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
        if not os.path.exists(TEST_FILE_DIR):
            os.mkdir(TEST_FILE_DIR)
        assert os.path.exists(TEST_FILE_DIR)
        if os.path.exists(self.filename):
            os.remove(self.filename)
        assert not os.path.exists(self.filename)
        with open(self.filename, "w"):
            pass
        assert os.path.exists(self.filename)

    def writeToFile(self, linesToWrite: list[str], lastRun: bool):
        assert os.path.exists(TEST_FILE_DIR), f"Directory Not Found: {TEST_FILE_DIR}"
        assert os.path.exists(self.filename), f"File Not Found, filename {self.filename}"
        with open(self.filename, "a") as file_obj:
            file_obj.write("\n".join(linesToWrite) + ("" if lastRun else "\n"))


if __name__ == "__main__":
    argParser = ArgumentParser(prog="Billion Row Challenge File Generator")
    argParser.add_argument("config", type=ConfigNames, choices=ConfigNames.__members__.values())
    parsedArgs = argParser.parse_args(sys.argv[1:2] if len(sys.argv) > 1 else [ConfigNames.FULL])
    print(f"Generating file with config: {CONFIGS[vars(parsedArgs)["config"]]}")
    TestFileGen(config=CONFIGS[vars(parsedArgs)["config"]])
