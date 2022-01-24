from __future__ import print_function

import pipes
import shutil
import subprocess
import sys
import traceback
from distutils import log
from distutils.command.build import build  # type: ignore
from distutils.command.sdist import sdist  # type: ignore
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.develop import develop

from bokeh.ext import build as build_bokeh_extension


if sys.platform == "win32":
    from subprocess import list2cmdline
else:

    def list2cmdline(cmd_list):
        return " ".join(map(pipes.quote, cmd_list))


# the name of the project
NAME = "idom_bokeh"

# basic paths used to gather files
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
PKG_DIR = SRC_DIR / NAME

# -----------------------------------------------------------------------------
# Package Definition
# -----------------------------------------------------------------------------


package = {
    "name": NAME,
    "python_requires": ">=3.7",
    "packages": find_packages(str(SRC_DIR)),
    "package_dir": {"": "src"},
    "description": "It's React, but in Python",
    "author": "Ryan Morshead",
    "author_email": "ryan.morshead@gmail.com",
    "url": "https://github.com/rmorshea/idom-bokeh",
    "license": "MIT",
    "platforms": "Linux, Mac OS X, Windows",
    "keywords": ["interactive", "widgets", "DOM", "React"],
    "include_package_data": True,
    "zip_safe": False,
    "classifiers": [
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Widget Sets",
        "Typing :: Typed",
    ],
}


# -----------------------------------------------------------------------------
# Library Version
# -----------------------------------------------------------------------------

pkg_root_init_file = PKG_DIR / "__init__.py"
for line in pkg_root_init_file.read_text().split("\n"):
    if line.startswith('__version__ = "') and line.endswith('"  # DO NOT MODIFY'):
        package["version"] = (
            line
            # get assignment value
            .split("=", 1)[1]
            # remove "DO NOT MODIFY" comment
            .split("#", 1)[0]
            # clean up leading/trailing space
            .strip()
            # remove the quotes
            [1:-1]
        )
        break
else:
    print(f"No version found in {pkg_root_init_file}")
    sys.exit(1)


# -----------------------------------------------------------------------------
# Requirements
# -----------------------------------------------------------------------------


requirements = []
with (ROOT_DIR / "requirements" / "pkg-deps.txt").open() as f:
    for line in map(str.strip, f):
        if not line.startswith("#"):
            requirements.append(line)
package["install_requires"] = requirements


# -----------------------------------------------------------------------------
# Library Description
# -----------------------------------------------------------------------------


with (ROOT_DIR / "README.md").open() as f:
    long_description = f.read()

package["long_description"] = long_description
package["long_description_content_type"] = "text/markdown"


# ----------------------------------------------------------------------------
# Build Javascript
# ----------------------------------------------------------------------------


def build_javascript_first(cls, rebuild=False):
    class Command(cls):
        def run(self):
            build_bokeh_extension(PKG_DIR, rebuild=rebuild)
            super().run()

    return Command


package["cmdclass"] = {
    "sdist": build_javascript_first(sdist),
    "build": build_javascript_first(build),
    "develop": build_javascript_first(develop, rebuild=True),
}


# -----------------------------------------------------------------------------
# Install It
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    setup(**package)
