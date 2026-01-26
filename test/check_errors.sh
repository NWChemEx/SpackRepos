#!/usr/bin/env bash

# Performs import of all NWChemEx Spack package components to check for errors.
#
# With v2.0 of the Spack package API, Spack packages can be treated as normal
# Python-importable packages. This allows a first-pass error check by just
# importing the packages before even installing them, catching potential
# programming errors up the stack quickly.
#
# Usage: <this_script>.sh
#
# Environment:
#   SPACK_ROOT           Used to find the location of your Spack install.
#   SPACK_NWCHEMEX_ENV   Env to activate that has the NWChemEx repo set up.
#                        Does not activate an env if undefined or empty.

set -e

_main() {
    # Ensure that Spack is available for the script
    local _spack_root="${SPACK_ROOT:-}"
    if [[ "${_spack_root}" == "" ]]; then
        printf 'ERROR: SPACK_ROOT environment variable not found! Make sure that Spack is installed and sourced correctly in your shell.\n'
        exit 1
    fi
    . "${_spack_root}"/share/spack/setup-env.sh

    # Check if an environment should be activated
    local _nwchemex_env="${SPACK_NWCHEMEX_ENV:-}"
    if [[ "${_nwchemex_env}" != "" ]]; then
        spack env activate "${_nwchemex_env}"
    fi

    # These are the imports to be executed
    commands=(
        "from spack_repo.nwchemex.common.mixins import *"
        "from spack_repo.nwchemex.core.packages.utilities.package import Utilities"
        "from spack_repo.nwchemex.core.packages.parallelzone.package import Parallelzone"
        "from spack_repo.nwchemex.core.packages.pluginplay.package import Pluginplay"
        "from spack_repo.nwchemex.core.packages.tensorwrapper.package import Tensorwrapper"
        "from spack_repo.nwchemex.core.packages.chemist.package import Chemist"
        "from spack_repo.nwchemex.core.packages.simde.package import Simde"
        "from spack_repo.nwchemex.core.packages.integrals.package import Integrals"
        "from spack_repo.nwchemex.core.packages.nux.package import Nux"
        "from spack_repo.nwchemex.core.packages.chemcache.package import Chemcache"
        "from spack_repo.nwchemex.core.packages.friendzone.package import Friendzone"
        "from spack_repo.nwchemex.core.packages.scf.package import Scf"
        "from spack_repo.nwchemex.core.packages.nwchemex.package import Nwchemex"
    )

    # Perform each import; this currently exits on the first error, but could
    # continue if the python call was changed to avoid triggering 'set -e' with
    # the colon no-op operator on error, like this:
    #   spack python -c "$cmd" || :
    for cmd in "${commands[@]}"; do
        printf 'Testing %s\n' "$cmd"
        spack python -c "$cmd"
    done
}

_main "$@"
