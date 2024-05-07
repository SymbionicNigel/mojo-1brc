from dataclasses import dataclass
from typing import Dict
from pytablewriter import MarkdownTableWriter


@dataclass(kw_only=True)
class AttemptData:
    commit_id: str
    run_time: float


class TableUpdater[T: AttemptData, I: str | float | int]:
    attempt_data: list[T] = []
    current_attempt: T

    def __init__(self, attempt_data: Dict[str, I]) -> None:
        self._validate(attempt_data)
        self._check_workspace_clean()
        self._read_attempt_data()
        self._upsert_current_data()
        self._save_data()

    def _validate(self, raw_data: Dict[str, I]):
        # self.current_attempt = T(**raw_data)
        # TODO: validate data being passed
        pass

    def _check_workspace_clean(self) -> bool:
        # TODO: validate we have a clean workspace without changes
        pass

    def _read_attempt_data(self):
        self.attempt_data = []
        # TODO: Read current data from .json file
        pass

    def _upsert_current_data(self):
        # TODO: pull current git commit id
        commit_id = ""

        def find_attempt_by_commit(item: AttemptData):
            return bool(commit_id) and (item.commit_id == commit_id)

        current_data = next(filter(find_attempt_by_commit, iter(self.attempt_data)))

        if not current_data:
            self.attempt_data.append(self.current_attempt)
            return

        current_index = self.attempt_data.index(self.current_attempt)
        self.attempt_data[current_index] = self.current_attempt

    def _save_data(self):
        # TODO: Create table and save to file
        # TODO: Save to .json file
        MarkdownTableWriter()
