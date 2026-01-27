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


class Friendzone(NWChemExBasePybindings):
    """Provides SimDE-compatible APIs so that NWChemEx can play nicely with its
    friends.
    """

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
        "1.0.9",
        sha256="fbf3b4a8f392e88e675696976d4d4927af1f158a2602f761796d415c1fbaeab1",
    )

    # TODO: Should this still be here for SimDE propagation?
    # pkg.variant(
    #     "sigma",
    #     default=False,
    #     description="Enable Sigma for uncertainty tracking",
    #     sticky=True,
    # )

    pkg.depends_on("py-pip", when="+python", type=("build", "link"))
    pkg.depends_on(
        "py-pydantic", when="+python", type=("build", "link", "run")
    )
    pkg.depends_on(
        "py-networkx~default", when="+python", type=("build", "link", "run")
    )
    pkg.depends_on(
        "py-qcelemental", when="+python", type=("build", "link", "run")
    )
    pkg.depends_on(
        "py-qcengine", when="+python", type=("build", "link", "run")
    )
    # pkg.depends_on("py-ase", when="+python", type=("build", "link", "run"))
    pkg.depends_on("nwchem", when="+python", type=("build", "link", "run"))

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
    # sanity_check_is_dir = NWChemExBasePybindings.cmaize_sanity_check_dirs(
    #     project.lower()
    # )
    # sanity_check_is_file = NWChemExBasePybindings.cmaize_sanity_check_files(
    #     project.lower()
    # )
    # Append more sanity checks as needed

    def cmake_args(self):
        args = super().cmake_args()

        args.extend(
            [
                self.define("ENABLE_ASE", "OFF"),
            ]
        )

        return args
