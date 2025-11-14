# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-qcelemental
#
# You can edit this file again by typing:
#
#     spack edit py-qcelemental
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.python import PythonPackage

from spack import package as pkg


class PyQcelemental(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/MolSSI/QCElemental"
    url = "https://github.com/MolSSI/QCElemental/archive/refs/tags/v0.29.0.tar.gz"
    git = "https://github.com/MolSSI/QCElemental.git"
    # pypi = "qcelemental/qcelemental-0.29.0.tar.gz"

    pkg.maintainers("ryanmrichard", "jwaldrop107", "zachcran")

    pkg.license("BSD-3-Clause")

    pkg.version(
        "0.29.0",
        sha256="3571b9bc6c67faba8ea9d988948fd8efc593bf3b5d533486f84ee2e423d60c1e",
    )
    pkg.version(
        "0.28.0",
        sha256="59f2104095b2d5bd78b02149c50c06fa884cde9fc2f49272edd0ec2e7f5fdd3d",
    )
    pkg.version(
        "0.27.1",
        sha256="10686a022e7e85259d6ee1730c29cedff1b67c8a21d753b336fb4c42529922b1",
    )
    pkg.version(
        "0.27.0",
        sha256="bf9ce6d6e134e905a5818c5907a3b8fa9fd8754eeb6b7519bd58c1a6a8177f1a",
    )
    pkg.version(
        "0.26.0",
        sha256="fe198b92298c2a922b5e780757c055a522b31e46178851594185924df82bc00a",
    )
    pkg.version(
        "0.25.1",
        sha256="87decd18ff6fffbbded4c77fe974c332a12573b9075247f461d57ec88301ac8b",
    )
    pkg.version(
        "0.25.0",
        sha256="aad969fb10ac803a659f400a8ffd452f8bfa98409c092a136761dc99eb8374a8",
    )
    pkg.version(
        "0.24.0",
        sha256="154367a7afa0a532325972caa16fd55b27c711fc4520a371eb9db56f4c2c62d1",
    )
    pkg.version(
        "0.23.0",
        sha256="a6c9b77e66241b0862bcad8507aa94c40d5f54d299f46484363e3413caa93185",
    )
    pkg.version(
        "0.22.0",
        sha256="e8d5e2cb00e5d8cd996157150e7270b304760c8a2bb569c68ad8ce279d5702d0",
    )

    pkg.depends_on("python@3.7:", type=("build", "run"))

    pkg.depends_on("py-poetry-core", type="build")

    pkg.depends_on("py-numpy@1.26:", type=("build", "run"))
    pkg.depends_on("py-packaging@24.1:", type=("build", "run"))
    pkg.depends_on("py-pint@0.24:", type=("build", "run"))
    pkg.depends_on("py-pydantic@1.8.2:", type=("build", "run"))
    pkg.depends_on("py-importlib-metadata@4.8:", type=("build", "run"))
    pkg.depends_on("py-networkx~default", type=("build", "run"))
    pkg.depends_on("py-scipy@1.9.0:", type=("build", "run"))
    pkg.depends_on("py-setuptools@68.0.0:", type=("build", "run"))
    pkg.depends_on("py-pytest@7.2.2:", type=("build", "run"))
