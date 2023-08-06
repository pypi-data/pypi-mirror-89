from setuptools import setup, find_packages

setup(
    name='justin',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pyvko',
        'Pillow',
        'lazy-object-proxy',
    ],
    url='',
    license='MIT',
    author='Harry Djachenko',
    author_email='i.s.djachenko@gmail.com',
    description='',
    entry_points={
        "console_scripts": [
            "justin = v3_0.runners.console_runner:run",
            "parts = parts.parts:run",
            "sf = subfolder.subfolder:run",
        ]
    }
)
