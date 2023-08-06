from uuid import uuid4
from pathlib import Path


class WorkingFile:
    def __init__(self, package: Path, name: str = 'siembra-temporary'):
        # FIXME: Check that path is a direct descendant of `package`
        path = (package / name).resolve()
        if path.exists() and not path.is_dir():
            path.unlink()
        path.mkdir(parents=True, exist_ok=True)

        self.working_directory = path

    def create(self):
        max_retries = 3
        for try_count in range(max_retries):
            try:
                path = self.working_directory / str(uuid4())
                return open(path, 'x')
            except FileExistsError as e:
                if try_count != max_retries - 1:
                    continue
                raise e
