import os.path
from setuptools import setup, find_packages

package_dir = os.path.abspath(os.path.dirname(__file__))
version_file = os.path.join(package_dir, "version")
with open(version_file) as version_file_handle:
    version = version_file_handle.read()

setup(
    name = "falcon-exceptions",
    version = version,
    description = "Falcon Exceptions",
    package_dir = {"":"src"},
    packages = find_packages("src"),
    install_requires=["falcon"],
    author = 'Andres Chavez',
    author_email = 'aschavezu@gmail.com',
    url = 'https://github.com/aschavez/falcon-exceptions',
    keywords = ['falcon', 'exceptions']
)
