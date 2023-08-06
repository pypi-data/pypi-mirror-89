from pathlib import Path
import yaml

import impl.v0_1


class Siembra:
    @staticmethod
    def get_module(version):
        version_map = {
            'v0.1': impl.v0_1,
        }

        module = version_map.get(version)
        return module

    @staticmethod
    def installer(spec, package, output, working_files):
        version = spec.get('version')
        module = Siembra.get_module(version)

        if module:
            module.SiembraValidator(spec).validate()
            return module.SiembraInstaller(
                spec=spec,
                package=package,
                output=output,
                working_files=working_files,
            )
        else:
            raise Exception('FIXME')
