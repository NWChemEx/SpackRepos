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
#     spack install nwchemex-parallelzone
#
# You can edit this file again by typing:
#
#     spack edit nwchemex-parallelzone
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class NwchemexParallelzone(CMakePackage):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    homepage = "https://github.com/NWChemEx/ParallelZone"
    url = "https://github.com/NWChemEx/ParallelZone/archive/refs/tags/v0.1.30.tar.gz"
    git = (
        "https://github.com/NWChemEx/ParallelZone.git"  # For the latest commit
    )

    # Versions are hosted under GitHub tags right now
    list_url = "https://github.com/NWChemEx/ParallelZone/tags"
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
        "0.1.34",
        sha256="ca47108832ddefc600c9b4782bbe0faf89da403a4cdac5b379f508be39ece934",
    )

    variant(
        "papi",
        default=False,
        description="Enable PAPI bindings",
    )
    # variant(
    #     "cuda",
    #     default=False,
    #     description="Enable CUDA bindings",
    # )
    # variant(
    #     "hip",
    #     default=False,
    #     description="Enable HIP bindings",
    # )
    # variant(
    #     "sycl",
    #     default=False,
    #     description="Enable SYCL bindings",
    # )
    variant(
        "pybindings",
        default=False,
        description="Build the Python bindings with Pybind11",
        sticky=True,
    )
    variant("docs", default=False, description="Build documentation")
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
    depends_on("mpi")
    depends_on("spdlog")
    depends_on("cereal@1.3.0")  # v1.3.1 changed the installed target...
    depends_on("papi", when="+papi")
    depends_on("py-pybind11", when="+pybindings")

    # Test dependencies
    depends_on("catch2", when="+tests")

    # Sanity check tests during installation
    sanity_check_is_file = [
        join_path("include", "parallelzone", "parallelzone.hpp"),
        join_path("lib", "parallelzone", "cmake", "parallelzoneConfig.cmake"),
        join_path(
            "lib", "parallelzone", "cmake", "parallelzoneConfigVersion.cmake"
        ),
        join_path("lib", "parallelzone", "cmake", "parallelzone-target.cmake"),
        # TODO: Conditionally check these once there is a "shared" variant
        # join_path("lib", "parallelzone", "libparallelzone.a"),
        # join_path("lib", "parallelzone", "libparallelzone.so"),
    ]

    sanity_check_is_dir = [
        join_path("include", "parallelzone"),
        join_path("lib", "parallelzone"),
        join_path("lib", "parallelzone", "cmake"),
    ]

    def cmake_args(self):
        args = [
            self.define_from_variant(
                "CMAKE_POSITION_INDEPENDENT_CODE", "shared"
            ),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("BUILD_DOCS", "docs"),
            self.define_from_variant(
                "BUILD_PYBIND11_PYBINDINGS", "pybindings"
            ),
            self.define_from_variant("PYBIND11_FINDPYTHON", "pybindings"),
        ]

        if self.spec.satisfies("+pybindings"):
            # TODO: Allow the user to configure this?
            args.append(
                "-DNWX_MODULE_DIRECTORY={}".format(
                    join_path(self.prefix.lib, "parallelzone", "python")
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
