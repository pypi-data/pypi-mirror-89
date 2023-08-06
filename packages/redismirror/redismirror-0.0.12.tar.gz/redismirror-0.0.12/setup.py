from setuptools import setup, find_packages
from redismirror.core.version import get_version

VERSION = get_version()

f = open("README.md", "r")
LONG_DESCRIPTION = f.read()
f.close()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name="redismirror",
    version=VERSION,
    description="Mirror Redis Traffic to another redis node",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    setup_requires=requirements,
    author="Ali Saleh Baker",
    author_email="alivxlive@gmail.com",
    url="https://github.com/alivx/redis-mirror",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "tests*"]),
    package_data={"redismirror": ["templates/*"]},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        redismirror = redismirror.main:main
    """,
)
