#!/usr/bin/env python

"""siembra

Usage:
  siembra new <package> <output-directory>

Options:
  -h --help     Show this screen.
"""

from pathlib import Path

import yaml
import docker  # type: ignore
from docopt import docopt  # type: ignore

from executors.docker import DockerConfig, DockerExecutor
from executors.file import (
    DirectoriesConfig,
    FileExecutorConfig,
    CopyExecutor,
    MoveExecutor,
    DeleteExecutor,
)
from executors.template import TemplateExecutor
from parameters import parse_parameters_dictionary

class Siembra:
    def __init__(self, spec):
        pass 

    def run(self, package):



def new(package:  Path, output_directory: Path) -> None:
    spec = yaml.load(open(package / 'siembra.yml'), Loader=yaml.Loader)

    parameters = parse_parameters_dictionary(spec.get('parameters', {}))

    directories_config = DirectoriesConfig(
        package=package,
        output=output_directory,
    )

    for step in spec['steps']:
        if step.get('docker'):
            config = DockerConfig.from_yml(step.get('docker'))

            DockerExecutor(config=config).run(volume=directories_config.output)
        elif step.get('copy'):
            CopyExecutor(config=directories_config).run(
                runtime=FileExecutorConfig.from_yml(step['copy'])
            )
        elif step.get('move'):
            MoveExecutor(config=directories_config).run(
                runtime=FileExecutorConfig.from_yml(step['move'])
            )
        elif step.get('delete'):
            DeleteExecutor(config=directories_config).run(step.get('delete'))
        elif step.get('template'):
            TemplateExecutor(config=parameters).run(
                directories_config.output / step.get('template', {}).get('file'))


def main() -> None:
    args = docopt(__doc__, version='0.1')

    if args.get('new'):
        new(package=Path(args['<package>']),
            output_directory=Path(args['<output-directory>']))


if __name__ == '__main__':
    main()
