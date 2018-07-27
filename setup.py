from setuptools import setup, find_packages
import versioneer
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('ltm/ltm/')
extra_files += package_files('config/')

setup(
    name='ltm_pipeline',
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='LTM Pipeline',
    author='',
    author_email='',
    entry_points={'console_scripts': ['ltm = ltm.run:main']},
    package_data={'': extra_files},
)
