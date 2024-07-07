from dataclasses import dataclass
from enum import StrEnum, auto


class ConfigNames(StrEnum):
    KILO = auto()
    DECI = auto()
    MILL = auto()
    PERCENT = auto()
    TENTH = auto()
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
    ConfigNames.DECI: TestFileConfig(10_000, 100, TEMP_RANGE, ConfigNames.DECI),
    ConfigNames.MILL: TestFileConfig(1_000_000, 500, TEMP_RANGE, ConfigNames.MILL),
    ConfigNames.PERCENT: TestFileConfig(
        10_000_000, 10_00, TEMP_RANGE, ConfigNames.PERCENT
    ),
    ConfigNames.TENTH: TestFileConfig(
        100_000_000, 5_000, TEMP_RANGE, ConfigNames.TENTH
    ),
    ConfigNames.FULL: TestFileConfig(
        1_000_000_000, 10_000, TEMP_RANGE, ConfigNames.FULL
    ),
}

TEST_FILE_DIR = "./.test_resources"

def generateFilename(config: TestFileConfig):
    return f"{TEST_FILE_DIR}/test_data_{config.configName}.txt"