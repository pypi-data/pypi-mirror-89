from pathlib import Path
from .executors.file import FileExecutor
from .executors.docker import DockerExecutor
from ..safepaths import is_relative_to


class SiembraInstaller:
    def __init__(self, package, output, spec, working_files):
        self.spec = spec
        self.package = Path(package).resolve()
        self.output = Path(output).resolve()
        self.working_files = working_files

        assert is_relative_to(self.package, self.output) is False
        assert is_relative_to(self.output, self.package) is False

    def run(self):
        install_steps = self.spec.get('install')

        for step in install_steps:
            if step.get('copy'):
                executor = FileExecutor(
                    spec=step['copy'],
                    package=self.package,
                    output=self.output,
                )
                executor.copy()
            elif step.get('docker'):
                executor = DockerExecutor(
                    spec=step['docker'],
                    package=self.package,
                    output=self.output,
                    working_files=self.working_files,
                )
                executor.run()
