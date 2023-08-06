from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from ingots.utils.packages_versions import build_package_full_version
from ingots.utils.packages_versions import create_package_version_file
from ingots.utils.packages_versions import read_package_version_file

__all__ = (
    "BuildPackageFullVersionTestCase",
    "CreatePackageVersionFileTestCase",
    "ReadPackageVersionFileTestCase",
)


class BuildPackageFullVersionTestCase(TestCase):
    """Checks the build_package_full_version function."""

    tst_base_package_version = "1.2.3"
    tst_version_suffix_env_name = "TST_ENV_PACKAGE_SUFFIX"

    def test_call_default(self):
        """Checks for default case."""
        tst_res = build_package_full_version(
            base_package_version=self.tst_base_package_version,
            version_suffix_env_name=self.tst_version_suffix_env_name,
        )
        self.assertEqual(tst_res, "1.2.3")

    def test_call_environ(self):
        """Checks for default call."""
        mock_environ = {self.tst_version_suffix_env_name: "rc4.dev5"}
        with patch("ingots.utils.packages_versions.os.environ", mock_environ):
            tst_res = build_package_full_version(
                base_package_version=self.tst_base_package_version,
                version_suffix_env_name=self.tst_version_suffix_env_name,
            )
        self.assertEqual(tst_res, "1.2.3rc4.dev5")


class CreatePackageVersionFileTestCase(TestCase):
    """Checks the create_package_version_file function."""

    tst_full_package_version = "1.2.3rc4.dev5"
    tst_version_file_name = "TST_VERSION"

    def test_call_default(self):
        """Checks the default call."""
        mock_file = Mock()
        mock_file.write = Mock()
        mock_open_cm = Mock()
        mock_open_cm.__enter__ = Mock(return_value=mock_file)
        mock_open_cm.__exit__ = Mock()
        with patch("builtins.open") as mock_open:
            mock_open.return_value = mock_open_cm
            create_package_version_file(
                full_package_version=self.tst_full_package_version,
            )
            mock_open.assert_called_once_with("VERSION", "w+")
        mock_file.write.assert_called_once_with(self.tst_full_package_version)

    def test_call_override_version_file_name(self):
        """Checks a call with override version file name."""
        mock_file = Mock()
        mock_file.write = Mock()
        mock_open_cm = Mock()
        mock_open_cm.__enter__ = Mock(return_value=mock_file)
        mock_open_cm.__exit__ = Mock()
        with patch("builtins.open") as mock_open:
            mock_open.return_value = mock_open_cm
            create_package_version_file(
                full_package_version=self.tst_full_package_version,
                version_file_name=self.tst_version_file_name,
            )
            mock_open.assert_called_once_with(self.tst_version_file_name, "w+")
        mock_file.write.assert_called_once_with(self.tst_full_package_version)


class ReadPackageVersionFileTestCase(TestCase):
    """Checks the read_package_version_file function."""

    tst_full_package_version = "1.2.3rc4.dev5"
    tst_version_file_name = "TST_VERSION"

    def test_call_default(self):
        """Checks the default call."""
        mock_file = Mock()
        mock_file.readline = Mock(return_value=self.tst_full_package_version)
        mock_open_cm = Mock()
        mock_open_cm.__enter__ = Mock(return_value=mock_file)
        mock_open_cm.__exit__ = Mock()
        with patch("builtins.open") as mock_open:
            mock_open.return_value = mock_open_cm
            tst_res = read_package_version_file()
            mock_open.assert_called_once_with("VERSION")
        self.assertEqual(tst_res, self.tst_full_package_version)
        mock_file.readline.assert_called_once_with()

    def test_call_override_version_file_name(self):
        """Checks a call with override version file name."""
        mock_file = Mock()
        mock_file.readline = Mock(return_value=self.tst_full_package_version)
        mock_open_cm = Mock()
        mock_open_cm.__enter__ = Mock(return_value=mock_file)
        mock_open_cm.__exit__ = Mock()
        with patch("builtins.open") as mock_open:
            mock_open.return_value = mock_open_cm
            tst_res = read_package_version_file(
                version_file_name=self.tst_version_file_name,
            )
            mock_open.assert_called_once_with(self.tst_version_file_name)
        self.assertEqual(tst_res, self.tst_full_package_version)
        mock_file.readline.assert_called_once_with()
