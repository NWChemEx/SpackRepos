from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings


class Tensorwrapper(NWChemExBasePybindings):
    """A type-erased wrapper around various tensor backends."""

    project = "TensorWrapper"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.0.55.tar.gz"
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
        "0.0.62",
        sha256="a526418836e0fff1362d4ff2c9131ae9eb2d509ae53148ac597f8de8444af9ca",
    )

    pkg.variant(
        "sigma",
        default=False,
        description="Enable Sigma for uncertainty tracking",
        sticky=True,
    )

    # Runtime dependencies
    pkg.depends_on("boost")
    pkg.depends_on("eigen", type=("build", "link", "run"))
    pkg.depends_on("py-numpy", when="+python", type=("build", "run"))

    # First-party
    pkg.depends_on("utilities")
    pkg.depends_on(
        "parallelzone~python",
        type=("build", "link", "run"),
        when="~python",
    )
    pkg.depends_on(
        "parallelzone+python",
        type=("build", "link", "run"),
        when="+python",
    )
    pkg.depends_on(
        "py-numpy",
        type=("build", "link", "run"),
        when="+python",
    )

    pkg.depends_on("sigma+eigen", when="+sigma")

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
