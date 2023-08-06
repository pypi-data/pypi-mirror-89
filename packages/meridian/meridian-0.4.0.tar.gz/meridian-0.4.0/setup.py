#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from pathlib import Path
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
pypi_name = "meridian"
# Set "package_name" if the import name of the package is
# different than the name it should have on pypi
package_name = None
short_desc = "Easy geospatial data processing."
url = "https://github.com/tomplex/meridian"
author = "Tom Caruso"
email = "carusot42@gmail.com"
min_python_version = (3, 6, 0)

install_requires = ["Shapely>=1.7.0", "Rtree>=0.8.3", "Fiona>=1.8"]

package_license = "MIT"
classifiers = [
    # Trove classifiers
    # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython",
]


def get_version(root, package):
    about = {}
    version_file = (root / package) / "__version__.py"
    with open(version_file) as f:
        exec(f.read(), about)

    return about["__version__"]


def get_long_description(root, default=None):
    try:
        with io.open(os.path.join(root, "README.md"), encoding="utf-8") as f:
            return "\n" + f.read()
    except FileNotFoundError:
        return default


here = Path(__file__).parent
package_name = package_name or pypi_name
required_python_dot_version = '.'.join([str(v) for v in min_python_version])
package_version = get_version(here, package_name)


if sys.version_info < min_python_version:
    print("Sorry, {} is only supported on Python{}+.".format(pypi_name, required_python_dot_version))
    sys.exit(1)


_setup = {
    "name": pypi_name,
    "version": get_version(here, pypi_name),
    "description": short_desc,
    "long_description": get_long_description(here, default=short_desc),
    "long_description_content_type": "text/markdown",
    "author": author,
    "author_email": email,
    "python_requires": ">={}".format(required_python_dot_version),
    "url": url,
    "packages": find_packages(exclude=("tests", "test")),
    "install_requires": install_requires,
    "license": package_license,
    "classifiers": classifiers,
}


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(package_version))
        os.system("git push --tags")

        self.status("Cleaning up...")
        os.system("rm -rf *.egg-info dist build")
        sys.exit()


setup(
    **_setup,
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand, },
)
