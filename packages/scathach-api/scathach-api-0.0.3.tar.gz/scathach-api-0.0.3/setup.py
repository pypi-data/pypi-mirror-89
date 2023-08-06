import re

from setuptools import setup


version = ''
with open('scathach/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


if not version:
    raise RuntimeError('version is not set')


setup(
    name='scathach-api',
    author='sinkaroid',
    author_email='anakmancasan@gmail.com',
    version='0.0.3',
    url='https://github.com/sinkaroid/scathach-api',
    packages=['scathach'],
    license='MIT',
    description='An advanced NSFW wrapper, complete rewrite and overhaul of the original Fate/Lewd Order API.',
    include_package_data=True,
    install_requires=requirements
)
