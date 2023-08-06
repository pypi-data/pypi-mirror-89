from setuptools import setup

requirements = [
    'requests',
    'enum'
]

setup(
    name="rayyan_store",
    version="0.1.0",
    description="Python client interface for RayyanStore",
    author="Fadhil Abubaker",
    packages=['rayyan_store'],
    install_requires=requirements
)
