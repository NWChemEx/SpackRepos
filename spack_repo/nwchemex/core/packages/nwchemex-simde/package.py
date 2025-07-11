# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
#     spack install nwchemex-simde
#
# You can edit this file again by typing:
#
#     spack edit nwchemex-simde
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class NwchemexSimde(CMakePackage):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    homepage = "https://github.com/NWChemEx/SimDE"
    url = "https://github.com/NWChemEx/SimDE/archive/refs/tags/v0.0.53.tar.gz"
    git = "https://github.com/NWChemEx/SimDE.git"  # For the latest commit

    # Versions are hosted under GitHub tags right now
    list_url = "https://github.com/NWChemEx/SimDE/tags"
    # To get older versions, uncomment 'list_depth' below and set it to a
    # value >0 to get list_depth + 1 pages of versions.
    # WARNING: This increases the number of links that the search spider will
    # follow, meaning even 'list_depth = 1' may increase the search time
    # significantly!
    # list_depth = 1

    maintainers("ryanmrichard", "jwaldrop107", "zachcran")
    license("Apache-2.0", checked_by="zachcran")

    # Latest commit from GitHub
    # "This download method is untrusted, and is not recommended. Branches are
    # moving targets, so the commit you get when you install the package likely
    # won’t be the same commit that was used when the package was first written."
    #                                          ~~~~ From the Spack docs
    # Is there a way to warn the user about this while still providing
    # the option?
    version("master", branch="master", preferred=True)

    # Versions from git tags
    version(
        "0.0.53",
        sha256="c95b818c0151a38190eebdaf41cc19fe04227ec827aef30293f959751a4b0bed",
    )

    variant(
        "pybindings",
        default=False,
        description="Build the Python bindings with Pybind11",
        sticky=True,
    )
    variant("docs", default=False, description="Build documentation")
    variant(
        "sigma",
        default=False,
        description="Enable Sigma for uncertainty tracking",
        sticky=True,
    )
    variant(
        "shared",
        default=True,
        description="Build shared libraries",
        sticky=True,
    )
    variant(
        "tests",
        default=False,
        description="Build unit tests",
    )

    # Runtime dependencies
    depends_on("cxx", type="build")
    depends_on("py-pybind11", when="+pybindings")
    # First-party
    depends_on("nwchemex-chemist")
    depends_on("nwchemex-pluginplay")

    # Test dependencies
    depends_on("catch2", when="+tests")

    # Sanity check tests during installation
    sanity_check_is_file = [
        join_path("include", "simde", "simde.hpp"),
        join_path("lib", "simde", "cmake", "simdeConfig.cmake"),
        join_path("lib", "simde", "cmake", "simdeConfigVersion.cmake"),
        join_path("lib", "simde", "cmake", "simde-target.cmake"),
        # TODO: Conditionally check these once there is a "shared" variant
        # join_path("lib", "simde", "libsimde.a"),
        # join_path("lib", "simde", "libsimde.so"),
    ]

    sanity_check_is_dir = [
        join_path("include", "simde"),
        join_path("lib", "simde"),
        join_path("lib", "simde", "cmake"),
    ]

    def cmake_args(self):
        args = [
            self.define_from_variant(
                "CMAKE_POSITION_INDEPENDENT_CODE", "shared"
            ),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("BUILD_DOCS", "docs"),
            self.define_from_variant("ENABLE_SIGMA", "sigma"),
            self.define_from_variant(
                "BUILD_PYBIND11_PYBINDINGS", "pybindings"
            ),
            self.define_from_variant("PYBIND11_FINDPYTHON", "pybindings"),
        ]

        if self.spec.satisfies("+pybindings"):
            # TODO: Allow the user to configure this
            args.append(
                "-DNWX_MODULE_DIRECTORY={}".format(
                    join_path(self.prefix.lib, "simde", "python")
                )
            )

        if "CMAKE_TOOLCHAIN_FILE" in os.environ:
            args.append(
                f"-DCMAKE_TOOLCHAIN_FILE={os.environ["CMAKE_TOOLCHAIN_FILE"]}"
            )
        args.append("-DCMAKE_MESSAGE_LOG_LEVEL=DEBUG")
        args.append("-DCMAKE_POLICY_DEFAULT_CMP0152=NEW")
        args.append("-Wno-dev")

        return args
