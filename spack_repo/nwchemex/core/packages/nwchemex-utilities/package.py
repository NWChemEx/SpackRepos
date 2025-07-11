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
#     spack install nwchemex-utilities
#
# You can edit this file again by typing:
#
#     spack edit nwchemex-utilities
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class NwchemexUtilities(CMakePackage):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    homepage = "https://github.com/NWChemEx/Utilities"
    url = "https://github.com/NWChemEx/Utilities/archive/refs/tags/v0.1.26.tar.gz"
    git = "https://github.com/NWChemEx/Utilities.git"  # For the latest commit

    # Versions are hosted under GitHub tags right now
    list_url = "https://github.com/NWChemEx/Utilities/tags"
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
        "0.1.26",
        sha256="508a14609cb6cdbaaa604ada512224ed1bfa3c378d0232c69429a2134c1d1180",
    )

    depends_on("cxx", type="build")

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

    # No runtime dependencies
    # depends_on("foo")

    # Test dependencies
    depends_on("catch2", type="test", when="+tests")

    # Sanity check tests during installation
    sanity_check_is_file = [
        join_path("lib", "utilities", "cmake", "utilitiesConfig.cmake"),
        join_path("lib", "utilities", "cmake", "utilitiesConfigVersion.cmake"),
        join_path("lib", "utilities", "cmake", "utilities-target.cmake"),
        # TODO: Conditionally check these once there is a "shared" variant
        # join_path("lib", "utilities", "libutilities.a"),
        # join_path("lib", "utilities", "libutilities.so"),
    ]
    sanity_check_is_dir = [
        join_path("include", "utilities"),
        join_path("lib", "utilities"),
        join_path("lib", "utilities", "cmake"),
        # ZDC: I don't think CMaize's "external/" should be a strict requirement
        # since it can be empty, especially with Spack managing most/all deps.
        # join_path("lib", "utilities", "external"),
    ]

    def cmake_args(self):
        args = [
            self.define_from_variant(
                "CMAKE_POSITION_INDEPENDENT_CODE", "shared"
            ),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("BUILD_DOCS", "docs"),
        ]

        if "CMAKE_TOOLCHAIN_FILE" in os.environ:
            args.append(
                f"-DCMAKE_TOOLCHAIN_FILE={os.environ["CMAKE_TOOLCHAIN_FILE"]}"
            )
        args.append("-DCMAKE_MESSAGE_LOG_LEVEL=DEBUG")
        args.append("-DCMAKE_POLICY_DEFAULT_CMP0152=NEW")
        args.append("-Wno-dev")

        return args
