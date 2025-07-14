from spack.package import join_path
from spack.package_base import PackageBase
from spack_repo.builtin.build_systems.cmake import CMakePackage


class CMaizePackage(CMakePackage):

    @staticmethod
    def cmaize_sanity_check_dirs(project_name: str) -> list[str]:
        # Could also use cls.__name__.lower() if it should always match
        project_name_lowercase = project_name.lower()

        # Create NWChemEx project locations
        project_include_path = join_path("include", project_name_lowercase)
        project_lib_path = join_path("lib", project_name_lowercase)
        project_lib_cmake_path = join_path(
            project_lib_path,
            "cmake",
        )

        directories = [
            join_path(project_include_path),
            join_path(project_lib_path),
            join_path(project_lib_cmake_path),
            # CMaize's "external/" should not be a strict requirement since it
            # can be empty, especially with Spack managing most/all deps.
            # join_path(project_lib_path, "external"),
        ]

        return directories

    @staticmethod
    def cmaize_sanity_check_files(project_name: str) -> list[str]:
        project_name_lowercase = project_name.lower()

        # Create NWChemEx project locations
        project_lib_path = join_path("lib", project_name_lowercase)
        project_lib_cmake_path = join_path(
            project_lib_path,
            "cmake",
        )

        files = [
            join_path(
                project_lib_cmake_path,
                f"{project_name_lowercase}Config.cmake",
            ),
            join_path(
                project_lib_cmake_path,
                f"{project_name_lowercase}ConfigVersion.cmake",
            ),
            join_path(
                project_lib_cmake_path,
                f"{project_name_lowercase}-target.cmake",
            ),
            # TODO: Conditionally check these once there is a "shared" variant
            #       if even possible
            # join_path(
            #     project_lib_path, f"lib{project_name_lowercase}.a"
            # ),
            # join_path(
            #     project_lib_path,
            #     f"lib{project_name_lowercase}.so",
            # ),
        ]

        return files
