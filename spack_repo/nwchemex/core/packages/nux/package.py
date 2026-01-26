from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings


class Nux(NWChemExBasePybindings):
    """NWChemEx User Experience (NUX): Tools, functions, etc. to facilitate
    user workflows.
    """

    project = "NUX"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.0.5.tar.gz"
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
        "0.0.5",
        sha256="58cb55b4975baf3255208333fd4366293efe55b0aeaab3c269f7485f75f2061b",
    )

    # First-party
    pkg.depends_on(
        "simde+python",
        type=("build", "link", "run"),
        when="+python",
    )
    pkg.depends_on(
        "simde~python",
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
