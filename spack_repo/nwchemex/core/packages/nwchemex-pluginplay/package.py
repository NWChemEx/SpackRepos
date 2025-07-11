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
#     spack install nwchemex-pluginplay
#
# You can edit this file again by typing:
#
#     spack edit nwchemex-pluginplay
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class NwchemexPluginplay(CMakePackage):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    homepage = "https://github.com/NWChemEx/PluginPlay"
    url = "https://github.com/NWChemEx/PluginPlay/archive/refs/tags/v1.0.43.tar.gz"
    git = "https://github.com/NWChemEx/PluginPlay.git"  # For the latest commit

    # Versions are hosted under GitHub tags right now
    list_url = "https://github.com/NWChemEx/PluginPlay/tags"
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
        "1.0.46",
        sha256="22303b38ac6e2459b50a9074697a59fbd01422cdb7db98599f81255f43176597",
    )

    variant(
        "rocksdb",
        default=False,
        description="Enable RocksDB backend of the cache",
    )
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
    depends_on("boost")
    depends_on("libfort enable_testing=false")
    depends_on("rocksdb", when="+rocksdb")
    depends_on("py-pybind11", when="+pybindings")
    # First-party
    depends_on("nwchemex-utilities")
    depends_on("nwchemex-parallelzone")

    # Test dependencies
    depends_on("catch2", when="+tests")

    # Sanity check tests during installation
    sanity_check_is_file = [
        join_path("include", "pluginplay", "pluginplay.hpp"),
        join_path("lib", "pluginplay", "cmake", "pluginplayConfig.cmake"),
        join_path(
            "lib", "pluginplay", "cmake", "pluginplayConfigVersion.cmake"
        ),
        join_path("lib", "pluginplay", "cmake", "pluginplay-target.cmake"),
        # TODO: Conditionally check these once there is a "shared" variant
        # join_path("lib", "pluginplay", "libpluginplay.a"),
        # join_path("lib", "pluginplay", "libpluginplay.so"),
    ]

    sanity_check_is_dir = [
        join_path("include", "pluginplay"),
        join_path("lib", "pluginplay"),
        join_path("lib", "pluginplay", "cmake"),
    ]

    def cmake_args(self):
        args = [
            self.define_from_variant(
                "CMAKE_POSITION_INDEPENDENT_CODE", "shared"
            ),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("BUILD_DOCS", "docs"),
            self.define_from_variant("BUILD_ROCKSDB", "rocksdb"),
            self.define_from_variant(
                "BUILD_PYBIND11_PYBINDINGS", "pybindings"
            ),
            self.define_from_variant("PYBIND11_FINDPYTHON", "pybindings"),
        ]

        if self.spec.satisfies("+pybindings"):
            # TODO: Allow the user to configure this
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
