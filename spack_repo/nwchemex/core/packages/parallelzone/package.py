# Copyright 2025-2026 NWChemEx Developers.
#
# SPDX-License-Identifier: Apache-2.0

from spack.package import depends_on, license, maintainers, variant, version

from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings

# TODO: Use from spack import package as pkg like other packages


class Parallelzone(NWChemExBasePybindings):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    project = "ParallelZone"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.1.34.tar.gz"
    git = f"https://github.com/NWChemEx/{project}.git"  # For the latest commit

    # Versions are hosted under GitHub tags right now
    list_url = f"https://github.com/NWChemEx/{project}/tags"
    # To get older versions, uncomment 'list_depth' below and set it to a
    # value >0 to get list_depth + 1 pages of versions.
    # WARNING: This increases the number of links that the search spider will
    # follow, meaning even 'list_depth = 1' may increase the search time
    # significantly!
    # list_depth = 1

    maintainers("ryanmrichard", "jwaldrop107", "zachcran")
    license("Apache-2.0", checked_by="zachcran")

    version("develop", branch="find_package_wrapper")

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

    # Runtime dependencies
    depends_on("mpi")
    depends_on("spdlog")
    depends_on(
        "cereal@1.3.1:", when="@0.1.41:"
    )  # v1.3.1 changed the installed target from "cereal" to "cereal::cereal"
    depends_on("cereal@:1.3.0", when="@:0.1.40")
    depends_on("papi", when="+papi")

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
                self.define_from_variant("BUILD_PAPI_BINDINGS ", "papi"),
            ]
        )

        return args
