"""siembra

Usage:
  siembra install <package> <output-directory>

Options:
  -h --help     Show this screen.
"""

import yaml
from pathlib import Path
from docopt import docopt

from metadata import SIEMBRA_VERSION
from siembra import Siembra
from working_files import WorkingFiles


def main():
    args = docopt(__doc__, version=SIEMBRA_VERSION)

    if args['install']:
        package = Path(args['<package>']).resolve()
        output_directory = Path(args['<output-directory>']).resolve()

        spec = yaml.load(open(package / 'siembra.yml'), Loader=yaml.Loader)

        working_files = WorkingFiles(output=output_directory)
        try:
            installer = Siembra.installer(
                spec=spec,
                package=package,
                output=output_directory,
                working_files=working_files,
            )

            installer.run()
        finally:
            working_files.destroy()


if __name__ == '__main__':
    main()
