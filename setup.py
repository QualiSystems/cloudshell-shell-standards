import os

from setuptools import find_packages, setup

with open(os.path.join("version.txt")) as version_file:
    version_from_file = version_file.read().strip()

with open("requirements.txt") as f_required:
    required = f_required.read().splitlines()

with open("test_requirements.txt") as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="cloudshell-shell-standards",
    url="http://www.qualisystems.com/",
    author="Quali",
    author_email="info@quali.com",
    packages=find_packages(),
    install_requires=required,
    tests_require=required_for_tests,
    version=version_from_file,
    description="QualiSystems Shells Standards Package",
    long_description="QualiSystems Shells Standards Package",
    include_package_data=True,
    python_requires="~=3.7",
)
