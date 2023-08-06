"""Setup configuration and dependencies for pystonkslib."""

from setuptools import find_packages, setup

with open("requirements.txt") as req_file:
    REQUIREMENTS = req_file.readlines()

COMMANDS = [
    "example_command=pystonkslib.example:main",
    "update_tickers=pystonkslib.tools.update_tickers:main",
]

setup(
    name="pystonkslib",
    version="0.0.1",
    author="Micheal Taylor",
    author_email="bubthegreat@gmail.com",
    url="https://gitlab.com/bubthegreat/pystonkslib",
    include_package_data=True,
    description="This is a stonks data pulling library",
    packages=find_packages("src"),
    package_dir={"": "src",},
    python_requires=">=3.6.6",
    entry_points={"console_scripts": COMMANDS},
    install_requires=REQUIREMENTS,
)
