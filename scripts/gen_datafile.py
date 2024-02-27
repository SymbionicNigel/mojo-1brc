from dataclasses import dataclass
from enum import auto, StrEnum
import random, string


@dataclass
class TestFileConfiguration:
    total_rows: int
    unique_locaions: int
    range: tuple[float, float]


class TestGenerator:
    config: TestFileConfiguration
    keys: set[str] = set()
    rows: list[str] = []

    def __init__(self, config: TestFileConfiguration) -> None:
        self.config = config

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
        pass

    def shuffleRows(self):
        pass

    def writeToFile(self, filepath: str):
        with open(filepath, "w") as file_obj:
            file_obj.writelines(self.rows)


class ConfigNames(StrEnum):
    KILO = auto()
    TENTH = auto()
    FULL = auto()


TEMP_RANGE = (-100, 100)

CONFIGS: dict[ConfigNames, TestFileConfiguration] = {
    ConfigNames.KILO: TestFileConfiguration(1_000, 50, TEMP_RANGE),
    ConfigNames.TENTH: TestFileConfiguration(1_000_000, 10_00, TEMP_RANGE),
    ConfigNames.FULL: TestFileConfiguration(1_000_000_000, 10_000, TEMP_RANGE),
}


def main():
    config = CONFIGS[ConfigNames.KILO]

    generator = TestGenerator(config=config)
    generator.generateKeys()


if __name__ == "__main__":
    main()
