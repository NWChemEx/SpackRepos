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

from spack import package as pkg
from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings


class NwchemexScf(NWChemExBasePybindings):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    project = "SCF"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.0.23.tar.gz"
    git = f"https://github.com/NWChemEx/{project}.git"  # For the latest commit

    # Versions are hosted under GitHub tags right now
    list_url = f"https://github.com/NWChemEx/{project}/tags"
    # To get older versions, uncomment 'list_depth' below and set it to a
    # value >0 to get list_depth + 1 pages of versions.
    # WARNING: This increases the number of links that the search spider will
    # follow, meaning even 'list_depth = 1' may increase the search time
    # significantly!
    # list_depth = 1

    pkg.maintainers("ryanmrichard", "jwaldrop107", "zachcran")
    pkg.license("Apache-2.0", checked_by="zachcran")

    # Versions from git tags
    pkg.version(
        "0.0.23",
        sha256="b175c15e8c814cd288817c970f4e049c7eab248975ff7c891d8927d7555d0cd8",
    )

    pkg.variant(
        "sigma",
        default=False,
        description="Enable Sigma for uncertainty tracking",
        sticky=True,
    )
    # TODO: Handle this turned on
    pkg.variant(
        "tamm",
        default=False,
        description="Build modules that rely on TAMM/Exachem",
    )
    pkg.variant(
        "experimental",
        default=False,
        description="Enable experimental features",
        sticky=False,
    )

    # For building GauXC, I think
    pkg.depends_on("c", type="build")

    # TODO: Create this package
    # pkg.depends_on("gauxc")
    pkg.depends_on("eigen")
    pkg.depends_on("libint@2.6:", when="+tamm")
    pkg.depends_on("mpi")
    # pkg.depends_on("tamm", when="+tamm")
    # pkg.depends_on("exachem", when="+tamm")

    # Although we have a variant, technically it is not a direct dependency
    # of this package
    # pkg.depends_on("sigma+eigen", when="+sigma")

    # First-party
    pkg.depends_on("nwchemex-simde")

    # Start with CMaize sanity check locations
    sanity_check_is_dir = NWChemExBasePybindings.cmaize_sanity_check_dirs(
        project.lower()
    )
    sanity_check_is_file = NWChemExBasePybindings.cmaize_sanity_check_files(
        project.lower()
    )
    # Append more sanity checks as needed

    def cmake_args(self):
        args = super().cmake_args()

        args.extend(
            [
                self.define_from_variant(
                    "ENABLE_EXPERIMENTAL_FEATURES", "experimental"
                ),
                self.define_from_variant("ENABLE_SIGMA", "sigma"),
            ]
        )

        return args
