from dataclasses import dataclass
import subprocess
from typing import Tuple
from pytablewriter import MarkdownTableWriter


@dataclass(kw_only=True)
class AttemptData:
    short_commit_id: str
    commit_id: str
    run_time: float


class TableUpdater[T: AttemptData, I: str | float | int]:
    attempt_data: list[T] = []
    current_attempt: T

    def __init__(self, current_attempt: T) -> None:
        self.current_attempt = current_attempt
        self._is_workspace_clean()
        self._read_attempt_data()
        self._upsert_current_data()
        self._save_data()

    def _is_workspace_clean(self, error_on_dirty: bool = True) -> bool:
        unstaged = subprocess.run(["git", "diff", "--exit-code", "--no-patch"])
        staged = subprocess.run(
            ["git", "diff", "--cached", "--exit-code", "--no-patch"]
        )
        if error_on_dirty:
            assert not unstaged.returncode
            assert not staged.returncode
        return bool(staged.returncode + unstaged.returncode)

    def _read_attempt_data(self):
        self.attempt_data = []
        # TODO: Read current data from .json file
        pass

    @classmethod
    def get_current_commit_data(cls) -> Tuple[str, str]:
        full = subprocess.run(["git", "rev-parse", "HEAD"])
        partial = subprocess.run(["git", "rev-parse", "--short", "HEAD"])
        return str(full.stdout), str(partial.stdout)

    def _upsert_current_data(self):
        def find_attempt_by_commit(item: AttemptData):
            return bool(self.current_attempt.commit_id) and (
                item.commit_id == self.current_attempt.commit_id
            )

        try:
            current_data = next(filter(find_attempt_by_commit, iter(self.attempt_data)))
            current_index = self.attempt_data.index(current_data)
            self.attempt_data[current_index] = self.current_attempt
        except StopIteration:
            self.attempt_data.append(self.current_attempt)
            pass

    def _save_data(self):
        # TODO: Create table and save to file
        # TODO: Save to .json file
        MarkdownTableWriter()


if __name__ == "__main__":
    current_commit = TableUpdater.get_current_commit_data()
    TableUpdater(
        AttemptData(
            commit_id=current_commit[0],
            short_commit_id=current_commit[1],
            run_time=10.1,
        )
    )
