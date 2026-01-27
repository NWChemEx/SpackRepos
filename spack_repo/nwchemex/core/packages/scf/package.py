# Copyright 2026 NWChemEx-Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from spack import package as pkg

from spack_repo.nwchemex.common.mixins import NWChemExBasePybindings


class Scf(NWChemExBasePybindings):
    """Provides SCF driver for the NWChemEx project."""

    project = "SCF"

    homepage = f"https://github.com/NWChemEx/{project}"
    url = f"https://github.com/NWChemEx/{project}/archive/refs/tags/v0.0.23.tar.gz"
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
        "0.0.23",
        sha256="b175c15e8c814cd288817c970f4e049c7eab248975ff7c891d8927d7555d0cd8",
    )

    # For building GauXC, I think
    pkg.depends_on("c", type="build")

    # TODO: Create this package
    # pkg.depends_on("gauxc")
    pkg.depends_on("eigen")
    pkg.depends_on("mpi")
    pkg.depends_on("py-numpy")
    # Uncomment when GauXC/Libxc interactions are sorted out
    # pkg.depends_on("libxc")

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
