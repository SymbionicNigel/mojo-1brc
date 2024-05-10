from dataclasses import dataclass, fields
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
    # Field order matters
    short_commit_id: str
    row_count: int
    run_time: float
    note: str = ""
    commit_id: str
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
        return not bool(staged.returncode + unstaged.returncode)

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

        workspaceClean = TableUpdater._is_workspace_clean()

        try:
            if not workspaceClean:
                assert (
                    self.current_attempt.note
                ), "A note is required when the workspace has uncommitted changes"
                self.current_attempt.commit_id += "*"
                self.current_attempt.short_commit_id += "*"
                # When working with an unclean workspace, reverse the list since `.insert()` takes the index of the item you wish to place an item before
                # Remember to un-reverse the list before finishing
                self.attempt_data.reverse()

            current_data = next(
                filter(
                    find_attempt_by_commit,
                    iter(self.attempt_data),
                )
            )

            current_index = self.attempt_data.index(current_data)
            if workspaceClean:
                self.attempt_data[current_index] = self.current_attempt
            else:
                self.attempt_data.insert(current_index, self.current_attempt)
                self.attempt_data.reverse()
        except StopIteration:
            if not workspaceClean:
                self.attempt_data.reverse()
            self.attempt_data.append(self.current_attempt)

    def _save_data(self):
        readme_template = ""
        with open(file=FILEPATHS["README_TEMPLATE"], mode="r") as stream:
            readme_template = stream.read()
        assert readme_template, "Readme template expected to be non-empty"

        markdown_table_string = MarkdownTableWriter(
            headers=[field.name for field in fields(AttemptData)],
            value_matrix=[list(x.__dict__.values()) for x in self.attempt_data],
        )

        with open(file=FILEPATHS["README"], mode="w") as stream:
            stream.write(
                readme_template.format(attempts_table=str(markdown_table_string))
            )

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
            commit_id=f"test_{current_commit[0]}",
            short_commit_id=f"test_{current_commit[1]}",
            run_time=123456.78,
            row_count=9004,
            note="Test note",
        )
    )
