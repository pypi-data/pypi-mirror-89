from dataclasses import dataclass
from logging import getLogger
from pathlib import Path

from injector import inject
from vunit import VUnit

from core_get.actions.action import Action
from core_get.actions.test.test_options import TestOptions
from core_get.configuration.environment_settings import EnvironmentSettings
from core_get.configuration.installed_packages_accessor import InstalledPackagesAccessor
from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.package.package_manifest_accessor import PackageManifestAccessor

logger = getLogger(__name__)


@inject
@dataclass
class Test(Action):
    package_manifest_accessor: PackageManifestAccessor
    environment_settings: EnvironmentSettings
    project_directory_manager: ProjectDirectoryManager
    installed_packages_accessor: InstalledPackagesAccessor

    def exec(self, options: TestOptions):
        manifest = self.package_manifest_accessor.read()
        vu = VUnit.from_argv(options.vunit_arguments)
        work_library = vu.add_library(manifest.library)

        project_path = self.project_directory_manager.get_project_directory()
        if project_path is None:
            logger.error('No package directory found')
            return
        path = Path(project_path)

        # Hack: Take the first variant
        variant_manifest = next(iter(manifest.variant_manifests.values()))
        all_files = [file.relative_to(project_path)
                     for pattern in variant_manifest.include
                     for file in path.glob(pattern)]

        for file in all_files:
            work_library.add_source_file(file)

        installed_packages = self.installed_packages_accessor.read()
        for installed_package in installed_packages.installed_packages:
            external_library = vu.add_library(installed_package.manifest.library, allow_duplicate=True)
            for installed_file in installed_package.installed_files:
                external_library.add_source_file(installed_file.path)

        vu.main()
