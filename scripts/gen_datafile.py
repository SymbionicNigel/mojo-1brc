from dataclasses import dataclass
from enum import auto, StrEnum
import random, string, os


class ConfigNames(StrEnum):
    KILO = auto()
    TENTH = auto()
    FULL = auto()


@dataclass
class TestFileConfiguration:
    total_rows: int
    unique_locaions: int
    range: tuple[float, float]
    configName: ConfigNames


TEMP_RANGE = (-99.9, 99.9)

CONFIGS: dict[ConfigNames, TestFileConfiguration] = {
    ConfigNames.KILO: TestFileConfiguration(1_000, 50, TEMP_RANGE, ConfigNames.KILO),
    ConfigNames.TENTH: TestFileConfiguration(
        1_000_000, 10_00, TEMP_RANGE, ConfigNames.TENTH
    ),
    ConfigNames.FULL: TestFileConfiguration(
        1_000_000_000, 10_000, TEMP_RANGE, ConfigNames.FULL
    ),
}


class TestGenerator:
    config: TestFileConfiguration
    keys: set[str] = set()
    rows: list[str] = []

    def __init__(self, config: TestFileConfiguration) -> None:
        self.config = config
        self.generateKeys()
        self.generateAllRows()
        self.shuffleRows()
        self.writeToFile("test_data")

    def _generateLocationName(self, stringLength: int):
        return "".join(random.choices(string.ascii_letters, k=stringLength))

    def _generateManyLocationNames(self, count: int):
        return [
            self._generateLocationName(random.randrange(1, 100)) for _ in range(count)
        ]

    def generateKeys(self):
        self.keys.clear()
        while len(self.keys) < self.config.unique_locaions:
            self.keys.update(
                self._generateManyLocationNames(
                    self.config.unique_locaions - len(self.keys)
                )
            )
        assert len(self.keys) == self.config.unique_locaions

    def generateRow(self):
        return f"{random.choice(list(self.keys))};{round(random.uniform(self.config.range[0], self.config.range[1]), 1)}\n"

    def generateAllRows(self):
        self.rows = [self.generateRow() for _ in range(self.config.total_rows)]
        assert len(self.rows) == self.config.total_rows

    def shuffleRows(self):
        random.shuffle(self.rows)

    def writeToFile(self, filepath: str):
        parent_filepath = "./.test_resources"
        if not os.path.exists(parent_filepath):
            os.mkdir(parent_filepath)
        assert os.path.exists(parent_filepath)
        with open(
            f"{parent_filepath}/{filepath}_{self.config.configName}.txt", "w+"
        ) as file_obj:
            file_obj.writelines(self.rows)


def main():
    [TestGenerator(config=config) for _, config in CONFIGS.items()]


if __name__ == "__main__":
    main()
