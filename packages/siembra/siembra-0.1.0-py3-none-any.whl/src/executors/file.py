import os
import shutil
from typing import Tuple
from collections.abc import Callable
from pathlib import Path

from .safe_path import safe_path


class InvalidPackagePath(Exception):
    def __init__(self, package: Path, path: Path):
        self.package = package
        self.path = path

        super().__init__(f'Path "{path}" is not a child of "{package}"')


class InvalidOutputPath(Exception):
    def __init__(self, output: Path, path: Path):
        self.output = output
        self.path = path

        super().__init__(f'Path "{path}" is not a child of "{output}"')


class DirectoriesConfig:
    def __init__(self, package: Path, output: Path):
        self.package = package.resolve()
        self.output = output.resolve()


class FileExecutorConfig:
    def __init__(self,
                 dest: Path,
                 from_package: Path = None,
                 from_output: Path = None):
        if from_package is not None and from_output is not None:
            # FIXME: Raise a proper exception for this
            raise Exception('ERROR')

        self.from_package = from_package if from_package else None
        self.from_output = from_output if from_output else None
        self.dest = dest

    @classmethod
    def from_yml(cls, yml):
        from_pkg = yml.get('from-pkg')
        from_output = yml.get('from')

        return cls(
            dest=Path(yml['to']),
            from_package=Path(from_pkg) if from_pkg else None,
            from_output=Path(from_output) if from_output else None,
        )


class FileExecutor:
    def __init__(self, config: DirectoriesConfig):
        self.config = config

    def mkdir(self, path):
        if not path.is_dir():
            path = path.parent
        path.mkdir(parents=True, exist_ok=True)

    def get_paths(self, runtime: FileExecutorConfig) -> Tuple[Path, Path]:
        if runtime.from_package:
            try:
                src = safe_path(self.config.package,
                                runtime.from_package)
            except ValueError:
                raise InvalidPackagePath(package=self.config.package,
                                         path=runtime.from_package)

        if runtime.from_output:
            try:
                src = safe_path(self.config.output,
                                runtime.from_output)
            except ValueError:
                raise InvalidOutputPath(output=self.config.output,
                                        path=runtime.from_output)

        try:
            dst = safe_path(self.config.output,
                            runtime.dest)
        except ValueError:
            raise InvalidOutputPath(output=self.config.output,
                                    path=runtime.dest)

        return (src, dst)

    def run(self,
            runtime: FileExecutorConfig,
            apply_fn) -> None:
        # import pdb
        # pdb.set_trace()

        src, dst = self.get_paths(runtime=runtime)
        self.mkdir(dst)
        apply_fn(src, dst)


class CopyExecutor:
    def __init__(self, config: DirectoriesConfig):
        self.config = config

    def run(self, runtime: FileExecutorConfig) -> None:
        def copy(src, dst):
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

        FileExecutor(config=self.config).run(runtime=runtime,
                                             apply_fn=copy)


class MoveExecutor:
    def __init__(self, config: DirectoriesConfig):
        self.config = config

    def run(self, runtime: FileExecutorConfig) -> None:
        FileExecutor(config=self.config).run(
            runtime=runtime,
            apply_fn=lambda src, dst: src.replace(dst)
        )


class DeleteExecutor:
    def __init__(self, config: DirectoriesConfig):
        self.config = config

    def run(self, path: Path) -> None:
        path = safe_path(self.config.output, path)
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)
