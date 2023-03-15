""" Usual setup file for package """
# read the contents of your README file
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
install_requires = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="Oil-Storage-Tanks",
    version="0.0.3",
    license="MIT",
    description="Dissertation regarding Oil Storage Tanks",
    author="Raj Modi",
    author_email="vardhan609@gmail.com",
    company="Gaia Research Ltd",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),    
)
