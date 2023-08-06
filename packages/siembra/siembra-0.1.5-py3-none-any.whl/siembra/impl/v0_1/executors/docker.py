import subprocess


class DockerExecutor:
    def __init__(self, spec, package, output, working_files):
        self.spec = spec
        self.package = package
        self.output = output
        self.working_files = working_files

    def run(self):
        # FIXME: This should be implemented using Docker's
        #        python sdk

        image = self.spec['image']
        commands = self.spec['commands']

        script_path = self.create_bash_script(commands)

        subprocess.run([
            'docker', 'run', '--rm', '-ti',
            '-v', f'{self.output}:/app',
            '-v', f'{script_path}:/tmp/run.sh',
            '-w', '/app',
            '--entrypoint',
            'bash',
            f'{image}',
            '/tmp/run.sh'
        ])

    def create_bash_script(self, commands):
        tmp_filename = self.working_files.create()

        script = '\n'.join([
            '#!/bin/bash',
            'set -x',
            *commands,
        ])

        with open(tmp_filename, 'w', newline='\n') as f:
            f.write(script)

        return tmp_filename
