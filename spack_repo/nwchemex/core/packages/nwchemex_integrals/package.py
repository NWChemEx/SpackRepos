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


class NwchemexIntegrals(NWChemExBasePybindings):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    project = "Integrals"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.0.30.tar.gz"
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
        "0.0.30",
        sha256="894bec1a6be2ec28302fde9f26f9b2961b43cfe4d15c037005fd266295dd7f3b",
    )

    pkg.variant(
        "sigma",
        default=False,
        description="Enable Sigma for uncertainty tracking",
        sticky=True,
    )

    # The "tune" variant is not available prior to v2.6
    # TODO: A value of "tune=none" or any of the molgw-* options likely break
    # the unit tests, but I don't know how to add them as conflicts yet.
    pkg.depends_on("libint@2.6:")
    # Although we have a variant, technically it is not a direct dependency
    # of this package
    # pkg.depends_on("sigma+eigen", when="+sigma")

    # First-party
    pkg.depends_on(
        "nwchemex-simde+python",
        type=("build", "link", "run"),
        when="+python",
    )
    pkg.depends_on(
        "nwchemex-simde~python",
        type=("build", "link", "run"),
        when="~python",
    )

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
                self.define_from_variant("ENABLE_SIGMA", "sigma"),
            ]
        )

        return args
