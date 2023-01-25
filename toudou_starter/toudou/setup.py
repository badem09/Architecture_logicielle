from setuptools import setup, find_packages

setup(
    name='Toudou',
    version='0.1',
    packages=['toudou'],
    package_dir={
        '': 'src',
    },
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': ['toudou=toudou:cli']
    }
)
