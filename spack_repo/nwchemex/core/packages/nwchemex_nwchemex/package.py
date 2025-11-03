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

from spack_repo.nwchemex.common.mixins import NWChemExBasePython


class NwchemexNwchemex(NWChemExBasePython):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    project = "NWChemEx"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.0.27.tar.gz"
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
        "0.0.27",
        sha256="1bd22792ca0fbe74f95b2065f2f2d674f2c62d186a340150e8ed1e0f27c2d334",
    )

    # TODO: Should this still be here for SimDE propagation?
    # pkg.variant(
    #     "sigma",
    #     default=False,
    #     description="Enable Sigma for uncertainty tracking",
    #     sticky=True,
    # )
    # TODO: Handle this turned on
    pkg.variant(
        "tamm",
        default=False,
        description="Build modules that rely on TAMM/Exachem",
    )
    # TODO: This is not used anywhere
    pkg.variant(
        "full-chemcache",
        default=False,
        description="If ChemCache isn't found, build the full version",
        sticky=False,
    )
    pkg.variant(
        "friends",
        values=pkg.any_combination_of("nwchem", "ase"),
        # pkg.any_combination_of() automatically adds a "none" option and sets
        # the following two options
        # default="none",
        # multi=True,
        description=(
            "Which friends to include. For multiple friends, use a "
            "comma-separated list "
            "(e.g. `spack install friendzone friends=nwchem,ase`)"
        ),
    )

    # TODO: Many of these may be able to be switched to ("build", "run")
    # instead of ("build", "link", "run")
    pkg.depends_on("python@3.10:", type=("build", "run"))

    # First-party
    # TODO: Figure out how to ensure that the correct value for the "friends"
    # variant can be propagated, or switch each friend to a separate variant
    pkg.depends_on(
        "nwchemex-friendzone",
        type=("build", "link", "run"),
    )
    pkg.depends_on(
        "nwchemex-scf+python",
        type=("build", "link", "run"),
    )
    pkg.depends_on(
        "nwchemex-nux+python",
        type=("build", "link", "run"),
    )
    pkg.depends_on(
        "nwchemex-chemcache+python",
        type=("build", "link", "run"),
    )
    pkg.depends_on(
        "nwchemex-integrals+python",
        type=("build", "link", "run"),
    )

    # TODO: Add sanity checks
    # Start with CMaize sanity check locations
    # sanity_check_is_dir = NWChemExBasePybindings.cmaize_sanity_check_dirs(
    #     project.lower()
    # )
    # sanity_check_is_file = NWChemExBasePybindings.cmaize_sanity_check_files(
    #     project.lower()
    # )
    # Append more sanity checks as needed
