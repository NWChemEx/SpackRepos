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
#     spack install nwchemex-friendzone
#
# You can edit this file again by typing:
#
#     spack edit nwchemex-friendzone
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBasePython


class NwchemexFriendzone(NWChemExBasePython):
    """Provides SimDE-compatible APIs so that NWChemEx can play nicely with its friends."""

    project = "FriendZone"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v1.0.9.tar.gz"
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
        "1.0.14",
        sha256="b504cb1f20ed5839a1fc926650b2f4114b8ff985f2295f81980e05281c74d652",
    )

    pkg.variant(
        "friends",
        values=pkg.any_combination_of("molssi", "ase", "nwchem"),
        # pkg.any_combination_of() automatically adds a "none" option and sets
        # the following two options
        # default="none",
        # multi=True,
        description=(
            "Which friends to include. For multiple friends, use a "
            "comma-separated list "
            "(e.g. `spack install friendzone friends=molssi,ase`)"
        ),
    )

    # TODO: Many of these may be able to be switched to ("build", "run")
    # instead of ("build", "link", "run")
    pkg.depends_on("python@3.10:", type=("build", "run"))
    pkg.depends_on("py-pip", type=("build", "link"))
    pkg.depends_on("py-setuptools", type="build")
    pkg.depends_on("py-pydantic", type=("build", "link", "run"))
    with pkg.when("friends=molssi"):
        pkg.depends_on("py-networkx~default", type=("build", "link", "run"))
        pkg.depends_on("py-qcelemental", type=("build", "link", "run"))
        pkg.depends_on("py-qcengine", type=("build", "link", "run"))
    with pkg.when("friends=nwchem"):
        pkg.depends_on("nwchem", type=("build", "link", "run"))
    with pkg.when("friends=ase"):
        pkg.depends_on("py-ase", type=("build", "link", "run"))

    # First-party
    pkg.depends_on(
        "nwchemex-simde+python",
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
