# Copyright 2025-2026 NWChemEx Developers.
#
# SPDX-License-Identifier: Apache-2.0

from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings


class Pluginplay(NWChemExBasePybindings):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    project = "PluginPlay"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v1.0.43.tar.gz"
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

    pkg.version("develop", branch="find_package_wrapper")

    # Versions from git tags
    pkg.version(
        "1.0.46",
        sha256="22303b38ac6e2459b50a9074697a59fbd01422cdb7db98599f81255f43176597",
    )

    pkg.variant(
        "rocksdb",
        default=False,
        description="Enable RocksDB backend of the cache",
    )

    # Runtime dependencies
    pkg.depends_on("boost")
    pkg.depends_on("libfort enable_testing=false")
    pkg.depends_on("rocksdb", when="+rocksdb")
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
                self.define_from_variant("BUILD_ROCKSDB", "rocksdb"),
            ]
        )

        return args
