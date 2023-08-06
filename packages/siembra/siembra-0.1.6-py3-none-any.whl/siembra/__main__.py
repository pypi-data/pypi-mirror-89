"""siembra

Usage:
  siembra install <package> <output-directory>

Options:
  -h --help     Show this screen.
"""

from docopt import docopt
from pathlib import Path
import yaml

from siembra import (
    __version__ as SIEMBRA_VERSION,
    TempFiles,
    Siembra,
)


def main():
    args = docopt(__doc__, version=SIEMBRA_VERSION)

    if args['install']:
        package = Path(args['<package>']).resolve()
        output_directory = Path(args['<output-directory>']).resolve()

        spec = yaml.load(open(package / 'siembra.yml'), Loader=yaml.Loader)

        temp_files = TempFiles(output=output_directory)
        try:
            installer = Siembra.installer(
                spec=spec,
                package=package,
                output=output_directory,
                temp_files=temp_files,
            )

            installer.run()
        finally:
            temp_files.destroy()


if __name__ == '__main__':
    main()
