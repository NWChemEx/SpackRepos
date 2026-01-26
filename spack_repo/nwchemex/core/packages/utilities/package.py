from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBaseCXX


class Utilities(NWChemExBaseCXX):
    """Generic, helpful C++ classes used by the NWChemEx project."""

    project = "Utilities"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.1.26.tar.gz"
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
        "0.1.26",
        sha256="508a14609cb6cdbaaa604ada512224ed1bfa3c378d0232c69429a2134c1d1180",
    )

    # Start with CMaize sanity check locations
    sanity_check_is_dir = NWChemExBaseCXX.cmaize_sanity_check_dirs(
        project.lower()
    )
    sanity_check_is_file = NWChemExBaseCXX.cmaize_sanity_check_files(
        project.lower()
    )
    # Append more sanity checks as needed
