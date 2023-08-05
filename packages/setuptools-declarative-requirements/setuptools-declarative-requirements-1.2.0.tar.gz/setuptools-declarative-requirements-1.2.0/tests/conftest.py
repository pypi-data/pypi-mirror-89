import json
import logging
import os
import pathlib
import random
import shutil
import string
import subprocess
import sys
import textwrap
import traceback
from contextlib import contextmanager

import attr
import pytest

from declarative_requirements import __version__

CODE_ROOT = pathlib.Path(__file__).resolve().parent.parent

log = logging.getLogger(__name__)


def random_string(prefix, size=6, uppercase=False, lowercase=True, digits=True):
    """
    Generates a random string.

    Args:
        prefix(str): The prefix for the random string
        size(int): The size of the random string
        uppercase(bool): If true, include upper-cased ascii chars in choice sample
        lowercase(bool): If true, include lower-cased ascii chars in choice sample
        digits(bool): If true, include digits in choice sample
    Returns:
        str: The random string
    """
    if not any([uppercase, lowercase, digits]):  # pragma: no cover
        raise RuntimeError(
            "At least one of 'uppercase', 'lowercase' or 'digits' needs to be true"
        )
    choices = []
    if uppercase:
        choices.extend(string.ascii_uppercase)
    if lowercase:
        choices.extend(string.ascii_lowercase)
    if digits:
        choices.extend(string.digits)

    return prefix + "".join(random.choice(choices) for _ in range(size))


@attr.s
class VirtualEnv:

    venv_dir = attr.ib()
    venv_python = attr.ib(init=False)

    @venv_dir.validator
    def _venv_dir(self, _, value):
        return value / random_string("venv-")

    @venv_python.default
    def _venv_python(self):
        if sys.platform.startswith("win"):
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"

    @property
    def venv_bin_dir(self):
        return self.venv_python.parent

    def __enter__(self):
        try:
            self._create_virtualenv()
        except subprocess.CalledProcessError:
            raise AssertionError("Failed to create virtualenv")
        return self

    def __exit__(self, *args):
        shutil.rmtree(str(self.venv_dir))

    def install(self, *args, **kwargs):
        return self.run(str(self.venv_python), "-m", "pip", "install", *args, **kwargs)

    def run(self, *args, **kwargs):
        check = kwargs.pop("check", True)
        kwargs.setdefault("cwd", str(self.venv_dir))
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.PIPE)
        kwargs.setdefault("universal_newlines", True),
        proc = subprocess.run(args, check=False, **kwargs)
        ret = CommandResult(
            exitcode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            cmdline=proc.args,
        )
        log.debug(ret)
        if check is True:  # pragma: no cover
            try:
                proc.check_returncode()
            except subprocess.CalledProcessError:
                raise CommandFailure(
                    "Command failed return code check",
                    cmdline=proc.args,
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    exitcode=proc.returncode,
                )
        return ret

    def get_installed_packages(self):
        ret = self.run(str(self.venv_python), "-m", "pip", "list", "--format", "json")
        pkgs = {}
        for entry in json.loads(ret.stdout):
            pkgs[entry["name"].lower()] = entry
        return pkgs

    def _get_real_python(self):
        """
        The reason why the virtualenv creation is proxied by this function is mostly
        because under windows, we can't seem to properly create a virtualenv off of
        another virtualenv(we can on linux) and also because, we really don't want to
        test virtualenv creation off of another virtualenv, we want a virtualenv created
        from the original python.
        Also, on windows, we must also point to the virtualenv binary outside the
        existing virtualenv because it will fail otherwise
        """
        try:
            if sys.platform.startswith("win"):
                return os.path.join(sys.real_prefix, os.path.basename(sys.executable))
            else:
                python_binary_names = [
                    "python{}.{}".format(*sys.version_info),
                    "python{}".format(*sys.version_info),
                    "python",
                ]
                for binary_name in python_binary_names:
                    python = os.path.join(sys.real_prefix, "bin", binary_name)
                    if os.path.exists(python):
                        break
                else:
                    bin_dir = os.path.join(sys.real_prefix, "bin")
                    raise AssertionError(
                        "Couldn't find a python binary name under '{bin_dir}' "
                        "matching: {python_binary_names}".format(
                            bin_dir=bin_dir, python_binary_names=python_binary_names
                        )
                    )
                return python
        except AttributeError:
            return sys.executable

    def _create_virtualenv(self):
        self.run("virtualenv", "--python", self._get_real_python(), str(self.venv_dir))


@attr.s(frozen=True)
class CommandResult:
    """
    This class serves the purpose of having a common result class which will hold the
    resulting data from a subprocess command.
    """

    exitcode = attr.ib()
    stdout = attr.ib()
    stderr = attr.ib()
    cmdline = attr.ib(default=None, kw_only=True)

    @exitcode.validator
    def _validate_exitcode(self, _, value):  # pragma: no cover
        if not isinstance(value, int):
            raise ValueError(
                "'exitcode' needs to be an integer, not '{}'".format(type(value))
            )

    def __str__(self):
        message = self.__class__.__name__
        if self.cmdline:
            message += "\n Command Line: {}".format(self.cmdline)
        if self.exitcode is not None:
            message += "\n Exitcode: {}".format(self.exitcode)
        if self.stdout or self.stderr:
            message += "\n Process Output:"
        if self.stdout:
            message += "\n   >>>>> STDOUT >>>>>\n{}\n   <<<<< STDOUT <<<<<".format(
                self.stdout
            )
        if self.stderr:
            message += "\n   >>>>> STDERR >>>>>\n{}\n   <<<<< STDERR <<<<<".format(
                self.stderr
            )
        return message + "\n"


class CommandFailure(Exception):  # pragma: no cover
    """
    Exception raised when a sub-process fails
    """

    def __init__(
        self, message, cmdline=None, stdout=None, stderr=None, exitcode=None, exc=None
    ):
        super().__init__()
        self.message = message
        self.cmdline = cmdline
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode
        self.exc = exc

    def __str__(self):
        message = self.message
        append_new_line = False
        if self.cmdline:
            message += "\n Command Line: {}".format(self.cmdline)
            append_new_line = True
        if self.exitcode is not None:
            append_new_line = True
            message += "\n Exitcode: {}".format(self.exitcode)
        if self.stdout or self.stderr:
            append_new_line = True
            message += "\n Process Output:"
        if self.stdout:
            message += "\n   >>>>> STDOUT >>>>>\n{}\n   <<<<< STDOUT <<<<<".format(
                self.stdout
            )
        if self.stderr:
            message += "\n   >>>>> STDERR >>>>>\n{}\n   <<<<< STDERR <<<<<".format(
                self.stderr
            )
        if self.exc:
            append_new_line = True
            message += "\n{}".format(
                "".join(traceback.format_exception(*self.exc)).rstrip()
            )
        if append_new_line:
            message += "\n"
        return message


@attr.s(frozen=True)
class Project:

    cwd = attr.ib()

    def run(self, *cmdline, check=False):
        proc = subprocess.run(
            cmdline,
            cwd=str(self.cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=False,
            # env={"DISTUTILS_DEBUG": "1"},
        )
        result = CommandResult(
            cmdline=cmdline,
            stdout=proc.stdout,
            stderr=proc.stderr,
            exitcode=proc.returncode,
        )
        log.debug(result)
        if check is True:
            proc.check_returncode()
        return result

    def sys_exec_run(self, *cmdline, check=False):
        return self.run(sys.executable, *cmdline, check=check)

    def write_file(self, path, contents=None, strip_first_newline=True):
        file_path = self.cwd.joinpath(path)
        file_directory = file_path.parent
        if not file_directory.is_dir():
            file_directory.mkdir(parents=True)
        file_path.touch(exist_ok=True)

        if contents is not None:
            if contents:
                if contents.startswith("\n") and strip_first_newline:
                    contents = contents[1:]
                file_contents = textwrap.dedent(contents)
            else:
                file_contents = contents

            file_path.write_text(file_contents)

    def write_setup(
        self,
        setup_requires=None,
        install_requires=None,
        extras_require=None,
        tests_require=None,
    ):
        if install_requires is None:
            install_requires = ""
        else:
            install_requires = "\n        install_requires = {}".format(
                install_requires
            )
        if setup_requires is None:
            setup_requires = ""
        else:
            setup_requires = "\n        setup_requires = {}".format(setup_requires)
        if tests_require is None:
            tests_require = ""
        else:
            tests_require = "\n        tests_require = {}".format(tests_require)
        if extras_require is None:
            extras_require = ""
        else:
            _extras_require = ""
            for key, value in extras_require.items():
                _extras_require += """          {} = {}\n""".format(key, value)
            if _extras_require:
                _extras_require = """\n        extras_require =\n{}\n""".format(
                    _extras_require
                )
            extras_require = _extras_require
        setup_cfg = """
        [metadata]
        name = test-project
        description = Test project for file support for setuptools declarative setup.cfg
        author = Pedro Algarvio
        author_email = pedro@algarvio.me
        url = https://github.com/s0undt3ch/setuptools-declarative-requirements
        project_urls =
            Source=https://gitlab.com/s0undt3ch/setuptools-declarative-requirements
            Tracker=https://gitlab.com/s0undt3ch/setuptools-declarative-requirements/issues
        license = Apache Software License 2.0
        classifiers =
            Programming Language :: Python
            Programming Language :: Cython
            Programming Language :: Python :: 3
            Programming Language :: Python :: 3 :: Only
            Programming Language :: Python :: 3.5
            Programming Language :: Python :: 3.6
            Programming Language :: Python :: 3.7
            Programming Language :: Python :: 3.8
            Programming Language :: Python :: 3.9
            Development Status :: 4 - Beta
            Intended Audience :: Developers
            License :: OSI Approved :: Apache Software License
        platforms = unix, linux, osx, cygwin, win32

        [options]
        zip_safe = False
        include_package_data = True
        packages = find:
        python_requires = >= 3.5
        install_requires =
          setuptools
          setuptools_declarative_requirements

        [requirements-files]{setup_requires}{install_requires}{tests_require}{extras_require}
        """.format(
            setup_requires=setup_requires,
            install_requires=install_requires,
            tests_require=tests_require,
            extras_require=extras_require,
        )
        self.write_file("setup.cfg", contents=setup_cfg)
        setup = """
        import setuptools
        if __name__ == "__main__":
            setuptools.setup()
        """
        self.write_file("setup.py", contents=setup)
        pyproject = """
        [build-system]
        requires = [
            "setuptools>=42",
            "wheel",
            "setuptools_declarative_requirements=={__version__}"
        ]
        build-backend = "setuptools.build_meta"
        """.format(
            __version__=__version__
        )
        self.write_file("pyproject.toml", contents=pyproject)
        manifest = """
        include requirements/*.txt
        """
        self.write_file("MANIFEST.in", contents=manifest)

    def create_pkg_tree(
        self,
        setup_requires=None,
        install_requires=None,
        extras_require=None,
        tests_require=None,
    ):
        self.write_setup(
            setup_requires=setup_requires,
            install_requires=install_requires,
            extras_require=extras_require,
            tests_require=tests_require,
        )
        self.write_file("tpkg/__init__.py")

        # if os.path.exists("/tmp/proj"):
        #     shutil.rmtree("/tmp/proj")
        # shutil.copytree(self.cwd, "/tmp/proj")

    def get_generated_dist(self):
        dist_dir = self.cwd / "dist"
        dist = next(dist_dir.glob("*.*"))
        return dist.relative_to(self.cwd)

    @contextmanager
    def virtualenv(self):
        with VirtualEnv(self.cwd) as venv:
            yield venv


@pytest.fixture(scope="session")
def local_pypi_repo_path(tmp_path_factory):
    yield tmp_path_factory.mktemp("pypi-pkgs")


@pytest.fixture(scope="session")
def build_test_pkgs(tmp_path_factory, local_pypi_repo_path):
    # Build this project's whell
    subprocess.run([sys.executable, "setup.py", "bdist_wheel"], cwd=str(CODE_ROOT))
    for pkg in CODE_ROOT.joinpath("dist").glob("*.*"):
        shutil.copyfile(str(pkg), str(local_pypi_repo_path.joinpath(pkg.name)))

    # Build the test project's wheel's
    setup_py = textwrap.dedent(
        """\
        import setuptools
        if __name__ == "__main__":
            setuptools.setup()
        """
    )
    pyproject_toml = textwrap.dedent(
        """\
        [build-system]
        requires = ["setuptools>=42", "wheel"]
        build-backend = "setuptools.build_meta"
        """
    )
    setup_cfg_tpl = textwrap.dedent(
        """\
        [metadata]
        name = {name}
        version = 1.0.0
        description = Test project for file support for setuptools declarative setup.cfg
        author = Pedro Algarvio
        author_email = pedro@algarvio.me
        license = Apache Software License 2.0

        [options]
        zip_safe = False
        include_package_data = True
        packages = find:
        """
    )
    for name in (
        "setup-requires",
        "install-requires",
        "docs-extras-require",
        "cli-extras-require",
        "tests-require",
    ):
        src = tmp_path_factory.mktemp("{}-pkg".format(name))
        src.joinpath("setup.py").write_text(setup_py)
        src.joinpath("pyproject.toml").write_text(pyproject_toml)
        src.joinpath("setup.cfg").write_text(
            setup_cfg_tpl.format(name="{}-pkg".format(name))
        )
        pkg = src / "{}_pkg".format(name.replace("-", "_"))
        pkg.mkdir()
        pkg.joinpath("__init__.py").touch()
        subprocess.run(
            [sys.executable, "setup.py", "bdist_wheel"], cwd=str(src), check=True
        )
        for pkg in src.joinpath("dist").glob("*.*"):
            shutil.copyfile(str(pkg), str(local_pypi_repo_path.joinpath(pkg.name)))


@pytest.fixture(scope="session")
def pypi_server(local_pypi_repo_path, build_test_pkgs):
    proc = subprocess.Popen(["pypi-server", "-p", "8080", str(local_pypi_repo_path)])
    os.environ["PIP_EXTRA_INDEX_URL"] = "http://localhost:8080"
    try:
        yield
    finally:
        os.environ.pop("PIP_EXTRA_INDEX_URL")
        with proc:
            proc.terminate()


@pytest.fixture
def project(tmp_path, pypi_server):
    _cwd = tmp_path / "cwd"
    _cwd.mkdir()
    return Project(_cwd)
