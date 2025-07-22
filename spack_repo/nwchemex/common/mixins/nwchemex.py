import os

from spack import package as pkg
from spack.package_base import PackageBase

from . import CMaizePackage


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

    pkg.variant(
        "cxxstd",
        default="17",
        # NOTE: Comma after "17" is necessary so Spack doesn't split it into
        #       individual characters
        values=("17",),
        multi=False,
        description="Use the specified C++ standard when building",
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
                self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
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

        return args


class NWChemExBasePybindings(NWChemExBaseCXX):

    pkg.variant(
        "pybindings",
        default=False,
        description="Build the Python bindings with Pybind11",
        sticky=True,
    )

    pkg.depends_on("py-pybind11", when="+pybindings")

    def cmake_args(self):
        args = super().cmake_args()

        args.extend(
            [
                self.define_from_variant(
                    "BUILD_PYBIND11_PYBINDINGS", "pybindings"
                ),
                self.define_from_variant("PYBIND11_FINDPYTHON", "pybindings"),
            ]
        )

        if self.spec.satisfies("+pybindings"):
            if "NWX_MODULE_DIRECTORY" in os.environ:
                args.append(
                    self.define(
                        "NWX_MODULE_DIRECTORY",
                        os.environ["NWX_MODULE_DIRECTORY"],
                    )
                )
            # TODO: Allow the user to configure this?
            # args.append(
            #     "-DNWX_MODULE_DIRECTORY={}".format(
            #         self.prefix.lib.join(self.project.lower()).join("python")
            #     )
            # )

        return args
