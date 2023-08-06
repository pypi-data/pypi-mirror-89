from string import Template
from pathlib import Path


class TemplateExecutor:
    def __init__(self, config: dict):
        self.config = config

    def run(self, path: Path) -> None:
        template = Template(open(path).read())
        open(path, 'w').write(
            template.substitute(self.config)
        )
