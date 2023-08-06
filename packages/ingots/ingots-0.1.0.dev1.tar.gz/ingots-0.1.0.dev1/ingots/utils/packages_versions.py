"""
Packages versions
=================

The module contains utilities for working with packages versions in the ingots package
and different derived from packages.
"""
import os

__all__ = (
    "build_package_full_version",
    "create_package_version_file",
    "read_package_version_file",
)


def build_package_full_version(
    base_package_version: str, version_suffix_env_name: str
) -> str:
    """
    Builds full package version from project base part and version suffix from
    environment.
    """
    version_suffix = os.environ.get(version_suffix_env_name, "")
    return f"{base_package_version}{version_suffix}"


def create_package_version_file(
    full_package_version: str, version_file_name: str = "VERSION"
):
    """
    Writes package version to file.
    """
    with open(version_file_name, "w+") as version_file:
        version_file.write(full_package_version)


def read_package_version_file(version_file_name: str = "VERSION") -> str:
    """
    Reads package version from file.
    """
    with open(version_file_name) as version_file:
        return version_file.readline()
