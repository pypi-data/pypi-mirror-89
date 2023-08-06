import os
import sys

sys.path.insert(0, os.path.abspath("."))  # noqa

from ingots import VERSION
from ingots.utils.packages_versions import build_package_full_version
from ingots.utils.packages_versions import create_package_version_file


if __name__ == "__main__":
    create_package_version_file(
        full_package_version=build_package_full_version(
            base_package_version=VERSION,
            version_suffix_env_name="INGOTS_VERSION_SUFFIX",
        )
    )
