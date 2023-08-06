import shutil
from uuid import uuid4
from pathlib import Path


class TempFiles:
    def __init__(self, output):
        tmp_dir = (output / '__siembra_delete_me__').resolve()
        if tmp_dir.exists() and not tmp_dir.is_dir():
            tmp_dir.unlink()
        tmp_dir.mkdir(parents=True, exist_ok=True)

        self.tmp_dir = tmp_dir

    def destroy(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def create(self):
        max_retries = 3
        for try_count in range(max_retries):
            try:
                path = self.tmp_dir / str(uuid4())
                with open(path, 'x'):
                    pass
                return path
            except FileExistsError as e:
                if try_count != max_retries - 1:
                    continue
                raise e
