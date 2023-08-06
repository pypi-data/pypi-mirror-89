import setuptools
import os
import re


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


def get_version():
    VERSIONFILE = os.path.join('siembra', '__init__.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))


setuptools.setup(
    name='siembra',
    version=get_version(),
    author='Juan Cabrera',
    author_email='juan@jjcp.dev',
    description='Description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mulitadev/siembra',
    packages=setuptools.find_packages(),
    install_requires=[
        'docopt==0.6.2',
        'PyYAML==5.3.1',
        'schema==0.7.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>= 3.8',
    entry_points={
        'console_scripts': [
            'siembra=siembra.__main__:main',
        ],
    },
)
