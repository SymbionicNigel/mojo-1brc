from dataclasses import dataclass
import json
import pathlib
import subprocess
from typing import List, Tuple

from pytablewriter import MarkdownTableWriter

FILEPATHS = {
    "README_TEMPLATE": pathlib.Path.cwd().joinpath("data_files/template_readme.md"),
    "README": pathlib.Path.cwd().joinpath("readme.md"),
    "ATTEMPTS_JSON": pathlib.Path.cwd().joinpath("data_files/attempt_data.json"),
}


@dataclass(kw_only=True)
class AttemptData:
    short_commit_id: str
    commit_id: str
    run_time: float
    note: str = ""
    row_count: int
    # TODO: add timestamp
    # date: datetime = datetime.fromtimestamp(0, UTC)


class TableUpdater:
    attempt_data: List[AttemptData]
    current_attempt: AttemptData

    def __init__(self, current_attempt: AttemptData) -> None:
        self.current_attempt = current_attempt
        self._is_workspace_clean()
        self._read_attempt_data()
        self._upsert_current_data()
        self._save_data()

    @staticmethod
    def _is_workspace_clean(error_on_dirty: bool = False) -> bool:
        unstaged = subprocess.run(["git", "diff", "--exit-code", "--no-patch"])
        staged = subprocess.run(
            ["git", "diff", "--cached", "--exit-code", "--no-patch"]
        )
        if error_on_dirty:
            assert not unstaged.returncode
            assert not staged.returncode
        return bool(staged.returncode + unstaged.returncode)

    def _read_attempt_data(self):
        with open(file=FILEPATHS["ATTEMPTS_JSON"], mode="r") as stream:
            attempt_data = json.load(stream)
            assert "attempts" in attempt_data
            self.attempt_data = [AttemptData(**x) for x in attempt_data["attempts"]]

    @staticmethod
    def get_current_commit_data() -> Tuple[str, str]:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode("ascii")
            .strip(),
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip(),
        )

    def _upsert_current_data(self):
        def find_attempt_by_commit(item: AttemptData):
            return bool(self.current_attempt.commit_id) and (
                item.commit_id == self.current_attempt.commit_id
            )

        if not TableUpdater._is_workspace_clean():
            assert (
                self.current_attempt.note
            ), "A note is required when the workspace has uncommitted changes"
            self.current_attempt.commit_id += "*"
            self.current_attempt.short_commit_id += "*"
            # TODO: insert after last instance of the commit
            pass
        try:
            current_data = next(filter(find_attempt_by_commit, iter(self.attempt_data)))
            current_index = self.attempt_data.index(current_data)
            self.attempt_data[current_index] = self.current_attempt
        except StopIteration:
            self.attempt_data.append(self.current_attempt)
            pass

    def _save_data(self):
        readme_template = ""
        with open(file=FILEPATHS["README_TEMPLATE"], mode="r") as stream:
            readme_template = stream.read()
        assert readme_template, "Readme template expected to be non-empty"

        # TODO: Create markdown table
        markdown_table_string = MarkdownTableWriter(kwargs={})

        with open(file=FILEPATHS["README"], mode="w") as stream:
            stream.write(readme_template.format(attempts_table=markdown_table_string))

        with open(file=FILEPATHS["ATTEMPTS_JSON"], mode="w") as stream:
            json.dump(
                {
                    "attempts": [x.__dict__ for x in self.attempt_data],
                },
                fp=stream,
                indent=2,
            )


if __name__ == "__main__":
    current_commit = TableUpdater.get_current_commit_data()
    TableUpdater(
        AttemptData(
            commit_id=current_commit[0],
            short_commit_id=current_commit[1],
            run_time=10.11,
            row_count=350,
            # date=datetime.now(UTC),
        )
    )
