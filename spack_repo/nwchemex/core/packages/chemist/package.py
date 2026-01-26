# Copyright 2025-2026 NWChemEx Developers.
#
# SPDX-License-Identifier: Apache-2.0

from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings


class Chemist(NWChemExBasePybindings):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    project = "Chemist"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v1.3.18.tar.gz"
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
        "1.3.19",
        sha256="dc1adf754ce9a532ee4b13461aaaf29488a2d6d5f34aaa416a33bd621abb8c29",
    )

    pkg.variant(
        "sigma",
        default=False,
        description="Enable Sigma for uncertainty tracking",
        sticky=True,
    )

    # Runtime dependencies
    pkg.depends_on("boost")

    # First-party
    pkg.depends_on("nwchemex-utilities")
    pkg.depends_on(
        "nwchemex-parallelzone+python",
        type=("build", "link", "run"),
        when="+python",
    )
    pkg.depends_on(
        "nwchemex-parallelzone~python",
        type=("build", "link", "run"),
        when="~python",
    )

    pkg.depends_on(
        "nwchemex-tensorwrapper+python",
        type=("build", "link", "run"),
        when="+python",
    )
    pkg.depends_on(
        "nwchemex-tensorwrapper~python",
        type=("build", "link", "run"),
        when="~python",
    )

    # Although we have a variant, technically it is not a direct dependency
    # of this package
    # pkg.depends_on("sigma+eigen", when="+sigma")

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
