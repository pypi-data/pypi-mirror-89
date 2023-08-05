from setuptools import setup, find_packages

entrypoints = {}

console_scripts = entrypoints['console_scripts'] = [
    'update-version = main:main',
]

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
    name='version_updater',
    version='0.0.1',
    description="Updates semantic versions, either of the artifact itself, or its dependencies",
    author="Jeremy Vickery",
    author_email="jeremyvickery@gmail.com",
    platforms=['any'],
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'semver==2.13.0',
        'jsonpath-ng==1.5.2',
        'ruamel.yaml==0.16.12'
    ],
    include_package_data=True,
    entry_points=entrypoints,
    long_description=long_description
)
