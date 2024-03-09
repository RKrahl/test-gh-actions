"""Test repository for GitHub actions

This repository does not provide anything useful.  It is used to try
out and play around with GitHub actions.
"""

import setuptools
from setuptools import setup
import setuptools.command.build_py
import distutils.command.sdist
from distutils import log
from glob import glob
from pathlib import Path
import string
try:
    import distutils_pytest
    cmdclass = distutils_pytest.cmdclass
except (ImportError, AttributeError):
    cmdclass = dict()
try:
    import setuptools_scm
    version = setuptools_scm.get_version()
except (ImportError, LookupError):
    try:
        import _meta
        version = _meta.version
    except ImportError:
        log.warn("warning: cannot determine version number")
        version = "UNKNOWN"

docstring = __doc__


class meta(setuptools.Command):

    description = "generate meta files"
    user_options = []
    meta_template = '''
version = "%(version)s"
'''

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        version = self.distribution.get_version()
        log.info("version: %s", version)
        values = {
            'version': version,
        }
        with Path("_meta.py").open("wt") as f:
            print(self.meta_template % values, file=f)


# Note: Do not use setuptools for making the source distribution,
# rather use the good old distutils instead.
# Rationale: https://rhodesmill.org/brandon/2009/eby-magic/
class sdist(distutils.command.sdist.sdist):
    def run(self):
        self.run_command('meta')
        super().run()
        subst = {
            "version": self.distribution.get_version(),
            "url": self.distribution.get_url(),
            "description": docstring.split("\n")[0],
            "long_description": docstring.split("\n", maxsplit=2)[2].strip(),
        }
        for spec in glob("*.spec"):
            with Path(spec).open('rt') as inf:
                with Path(self.dist_dir, spec).open('wt') as outf:
                    outf.write(string.Template(inf.read()).substitute(subst))


class build_py(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('meta')
        super().run()
        package = self.distribution.packages[0].split('.')
        outfile = self.get_module_outfile(self.build_lib, package, "_meta")
        self.copy_file("_meta.py", outfile, preserve_mode=0)


with Path("README.rst").open("rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name = "test-gh-actions",
    version = version,
    description = docstring.split("\n")[0],
    long_description = readme,
    long_description_content_type = "text/x-rst",
    url = "https://github.com/RKrahl/test-gh-actions",
    author = "Rolf Krahl",
    author_email = "rolf@rotkraut.de",
    license = "Apache-2.0",
    classifiers = [
        "Development Status :: 1 - Planning",
        # "Intended Audience :: ?",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        # "Topic :: ?",
    ],
    project_urls = dict(
        Source="https://github.com/RKrahl/test-gh-actions",
        Download="https://github.com/RKrahl/test-gh-actions/releases/latest",
    ),
    packages = ["test_gha"],
    package_dir = {"": "src"},
    python_requires = ">=3.6",
    install_requires = [],
    cmdclass = dict(cmdclass, build_py=build_py, sdist=sdist, meta=meta),
)
