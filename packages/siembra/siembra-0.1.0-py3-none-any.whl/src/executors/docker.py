import sys
import subprocess
from typing import List
from pathlib import Path

from .working_file import WorkingFile


class DockerConfig:
    def __init__(self, image: str, commands: List[str]):
        self.image = image
        self.commands = commands

    @classmethod
    def from_yml(cls, yml: dict):
        return cls(
            image=yml['image'],
            commands=yml['commands'],
        )


class DockerExecutor:
    def __init__(self, config: DockerConfig):
        self.config = config

    def run(self, volume: Path) -> None:
        # FIXME: This should be implemented using Docker's
        #        python sdk

        wf = WorkingFile(package=Path('.'), name='siembra-temporary')

        for command in self.config.commands:
            sh_file = wf.create()
            sh_path = Path(sh_file.name).resolve()

            sh_file.write(f'{command}')
            sh_file.close()

            subprocess.run([
                'docker', 'run', '--rm', '-ti',
                '-v', f'{volume.resolve()}:/app',
                '-v', f'{sh_path}:/tmp/run.sh',
                '-w', '/app',
                '--entrypoint',
                'bash',
                f'{self.config.image}',
                '/tmp/run.sh'
            ])
