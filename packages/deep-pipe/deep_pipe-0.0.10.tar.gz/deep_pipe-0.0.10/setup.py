from setuptools import setup, find_packages

from dpipe import __version__

classifiers = '''Development Status :: 4 - Beta
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8'''

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

with open('requirements.txt', encoding='utf-8') as file:
    requirements = file.read().splitlines()

setup(
    name='deep_pipe',
    packages=find_packages(include=('dpipe',)),
    include_package_data=True,
    version=__version__,
    description='A collection of tools for deep learning experiments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/neuro-ml/deep_pipe',
    download_url='https://github.com/neuro-ml/deep_pipe/v%s.tar.gz' % __version__,
    keywords=[],
    classifiers=classifiers.splitlines(),
    install_requires=requirements,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dpipe-run = dpipe.layout.scripts:run',
            'dpipe-build = dpipe.layout.scripts:build',
        ],
    },
)
