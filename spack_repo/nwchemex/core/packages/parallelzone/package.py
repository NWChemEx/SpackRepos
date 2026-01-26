from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings

# TODO: Use from spack import package as pkg like other packages


class Parallelzone(NWChemExBasePybindings):
    """You're travelling through another dimension, a dimension not only of
    CPUs and threads but of GPUs; a journey into a wondrous land whose
    boundaries are bandwidth limited. That's the signpost up ahead - your next
    stop, the ParallelZone!
    """

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

    pkg.maintainers("ryanmrichard", "jwaldrop107", "zachcran")
    pkg.license("Apache-2.0", checked_by="zachcran")

    pkg.version("develop", branch="find_package_wrapper")

    # Versions from git tags
    pkg.version(
        "0.1.34",
        sha256="ca47108832ddefc600c9b4782bbe0faf89da403a4cdac5b379f508be39ece934",
    )

    pkg.variant(
        "papi",
        default=False,
        description="Enable PAPI bindings",
    )
    # pkg.variant(
    #     "cuda",
    #     default=False,
    #     description="Enable CUDA bindings",
    # )
    # pkg.variant(
    #     "hip",
    #     default=False,
    #     description="Enable HIP bindings",
    # )
    # pkg.variant(
    #     "sycl",
    #     default=False,
    #     description="Enable SYCL bindings",
    # )

    # Runtime dependencies
    pkg.depends_on("mpi")
    pkg.depends_on("spdlog")
    pkg.depends_on(
        "cereal@1.3.1:", when="@0.1.41:"
    )  # v1.3.1 changed the installed target from "cereal" to "cereal::cereal"
    pkg.depends_on("cereal@:1.3.0", when="@:0.1.40")
    pkg.depends_on("papi", when="+papi")

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
                self.define_from_pkg.variant("BUILD_PAPI_BINDINGS ", "papi"),
            ]
        )

        return args
