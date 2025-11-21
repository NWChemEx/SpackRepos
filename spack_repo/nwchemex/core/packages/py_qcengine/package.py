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
#     spack install py-qcengine
#
# You can edit this file again by typing:
#
#     spack edit py-qcengine
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.python import PythonPackage

from spack import package as pkg


class PyQcengine(PythonPackage):
    """QCEngine provides a wrapper to ingest and produce QCSchema for a variety
    of quantum chemistry programs."""

    homepage = "https://github.com/MolSSI/QCEngine"
    url = "https://github.com/MolSSI/QCEngine/archive/refs/tags/v0.29.0.tar.gz"
    git = "https://github.com/MolSSI/QCEngine.git"
    # pypi = "qcengine/qcengine-0.33.0.tar.gz"

    pkg.maintainers("ryanmrichard", "jwaldrop107", "zachcran")

    pkg.license("BSD-3-Clause")

    pkg.version(
        "0.33.0",
        sha256="7d9317355294b2118b9e959e57394eb3f2205db004d9ebe7441cd5026a7fc6c4",
    )
    pkg.version(
        "0.32.0",
        sha256="666ae2eeec6758904548ac72199964c2141a1fcd2f14fed5dbe8bc324e43e4ac",
    )
    pkg.version(
        "0.31.0",
        sha256="1d220c32efa813191a95a5c6a7aa8035551e4126230b60dccea4af236eeff810",
    )
    pkg.version(
        "0.30.0",
        sha256="896c690fa82a5f65b6d702775ac61606dc54050f8642f0c04b6497c5f9bdca62",
    )
    pkg.version(
        "0.29.0",
        sha256="a790f733d9132675636216011286415872ce815e6a4e7f7029ccde8c90293bfc",
    )
    pkg.version(
        "0.28.1",
        sha256="11555cfc475fe6d048da6335fc1e2150a6c5f8082a415c45fe596e4fc96588ee",
    )
    pkg.version(
        "0.28.0",
        sha256="c4b27a7a2f06e02e0ddfabf9b9b95adcc4f92acdd9a55678ae603d79a8464e60",
    )
    pkg.version(
        "0.27.0",
        sha256="d339976c880c79cfe2da7cdb8458895a97322ca2abd134734b0b15031f5e3eeb",
    )
    pkg.version(
        "0.26.0",
        sha256="0659fc6e92d0b8bd2252e4d0290543fdbf6fd5361943b4a43d429fe3074ab2dc",
    )
    pkg.version(
        "0.25.0",
        sha256="2b651ed588c606cb9a734d4cfe04f8dfdee5ce7ccc64885c38f1a4e7798dadea",
    )

    pkg.depends_on("python@3.7:", type=("build", "run"))

    pkg.depends_on("py-setuptools", type="build")

    pkg.depends_on("py-pyyaml", type=("build", "run"))
    pkg.depends_on("py-py-cpuinfo", type=("build", "run"))
    pkg.depends_on("py-psutil", type=("build", "run"))
    pkg.depends_on("py-pydantic@1.8.2:", type=("build", "run"))
    pkg.depends_on("py-packaging", type=("build", "run"))
    pkg.depends_on("py-qcelemental", type=("build", "run"))
