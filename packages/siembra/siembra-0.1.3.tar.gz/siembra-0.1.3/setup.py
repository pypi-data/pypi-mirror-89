import setuptools
from src.metadata import SIEMBRA_VERSION

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='siembra',
    version=SIEMBRA_VERSION,
    author='Juan Cabrera',
    author_email='juan@jjcp.dev',
    description='Description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mulitadev/siembra',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>= 3.8',
    scripts=['src/siembra'],
)
