class Siembra:
    @staticmethod
    def get_module(version):
        from . import v0_1

        version_map = {
            'v0.1': v0_1,
        }

        module = version_map.get(version)
        return module

    @staticmethod
    def installer(spec, package, output, temp_files):
        version = spec.get('version')
        module = Siembra.get_module(version)

        if module:
            module.SiembraValidator(spec).validate()
            return module.SiembraInstaller(
                spec=spec,
                package=package,
                output=output,
                temp_files=temp_files,
            )
        else:
            raise Exception('FIXME')
