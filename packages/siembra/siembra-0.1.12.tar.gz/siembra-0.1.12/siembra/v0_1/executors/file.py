import shutil
from pathlib import Path


def is_relative_to(first, second):
    try:
        first.relative_to(second)
        return True
    except ValueError:
        return False


class FileExecutor:
    def __init__(self, spec, package, output):
        self.spec = spec
        self.package = package
        self.output = output

    def copy(self):
        _, from_path = self.compute_path(self.spec['from'])
        to_type, to_path = self.compute_path(self.spec['to'])

        if to_type != 'out':
            raise Exception('FIXME')

        if from_path.is_dir():
            shutil.copytree(
                src=from_path,
                dst=to_path,
                dirs_exist_ok=True,
            )
        else:
            shutil.copy2(
                src=from_path,
                dst=to_path,
            )

    def compute_path(self, path):
        pkg_prefix = 'pkg/'
        out_prefix = 'out/'

        if path.startswith(pkg_prefix):
            path = self.package / Path(path[len(pkg_prefix):])
            if is_relative_to(path, self.package):
                return ('pkg', path)
            else:
                raise Exception('FIXME')
        elif path.startswith(out_prefix):
            path = self.output / Path(path[len(out_prefix):])
            if is_relative_to(path, self.output):
                return ('out', path)
            else:
                raise Exception('FIXME')
        else:
            raise Exception('FIXME')
