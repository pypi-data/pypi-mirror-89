
from schema import Schema, And, Regex


class SiembraValidator:
    def __init__(self, spec):
        self.spec = spec

    def validate(self):
        schema = Schema({
            'version': 'v0.1',
            'install': [
                {
                    'copy': {
                        'from': And(str, Regex(r'^pkg/?|^out/?')),
                        'to': And(str, Regex(r'^out/?')),
                    }
                },
                {
                    'docker': {
                        'image': str,
                        'commands': [str],
                    }
                },
            ]
        })

        schema.validate(self.spec)
