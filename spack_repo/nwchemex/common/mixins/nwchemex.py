import os

from spack import package as pkg
from spack.package_base import PackageBase
from spack_repo.builtin.build_systems.python import PythonPackage

from .cmaize import CMaizePackage


class NWChemExBaseGit(PackageBase):

    # Latest commit from GitHub
    # "This download method is untrusted, and is not recommended. Branches are
    # moving targets, so the commit you get when you install the package likely
    # won’t be the same commit that was used when the package was first
    # written."
    #                                          ~~~~ From the Spack docs
    # Is there a way to warn the user about this while still providing
    # the option?
    pkg.version("master", branch="master", preferred=True)


class NWChemExBaseCXX(NWChemExBaseGit, CMaizePackage):

    pkg.variant("docs", default=False, description="Build documentation")
    pkg.variant(
        "shared",
        default=True,
        description="Build shared libraries",
        sticky=True,
    )

    pkg.depends_on("cxx", type="build")

    # Test dependencies
    pkg.depends_on("catch2", type=("build", "test"))

    def cmake_args(self):
        args = super().cmake_args()

        args.extend(
            [
                self.define_from_variant(
                    "CMAKE_POSITION_INDEPENDENT_CODE", "shared"
                ),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("BUILD_DOCS", "docs"),
                self.define("BUILD_TESTING", self.run_tests),
            ]
        )

        if "CMAKE_TOOLCHAIN_FILE" in os.environ:
            args.append(
                f"-DCMAKE_TOOLCHAIN_FILE={os.environ["CMAKE_TOOLCHAIN_FILE"]}"
            )
        # TODO: +debug flag? +verbose flag?
        args.append(self.define("CMAKE_MESSAGE_LOG_LEVEL", "DEBUG"))
        # Silence FetchContent by default
        args.append(self.define("FETCHCONTENT_QUIET", True))
        args.append("-Wno-dev")
        # https://cmake.org/cmake/help/latest/policy/CMP0152.html
        # Added in 3.28; OLD is deprecated now
        args.append(self.define("CMAKE_POLICY_DEFAULT_CMP0152", "NEW"))

        # DEBUG REMOVE ME
        args.append(
            self.define(
                "CMAKE_VERBOSE_MAKEFILE",
                True,
            )
        )

        return args


class NWChemExBasePybindings(NWChemExBaseCXX):

    pkg.variant(
        "python",
        default=True,
        description="Build the Python bindings",
        # sticky=True,
    )

    # https://spack.readthedocs.io/en/latest/build_systems/pythonpackage.html#extends-vs-depends-on
    pkg.extends("python", when="+python")
    pkg.depends_on(
        "py-pybind11@3:",
        type=("build", "link", "run", "test"),
        when="+python",
    )
    pkg.depends_on(
        "python@3:",
        type=("build", "link", "run", "test"),
        when="+python",
    )

    def cmake_args(self):
        args = super().cmake_args()

        args.extend(
            [
                self.define_from_variant(
                    "BUILD_PYBIND11_PYBINDINGS", "python"
                ),
                self.define_from_variant("PYBIND11_FINDPYTHON", "python"),
            ]
        )

        if self.spec.satisfies("+python"):
            args.append(
                self.define(
                    "NWX_MODULE_DIRECTORY",
                    # lib64 is used for platlib from Python package
                    self.prefix.lib.join(
                        "python{}".format(self.spec["python"].version[:-1])
                    ).join("site-packages"),
                )
            )

        return args


class NWChemExBasePython(NWChemExBaseGit, PythonPackage):
    pass
