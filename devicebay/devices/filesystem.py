from typing import Optional, Type, List

from pydantic import BaseModel

from devicebay import Device, action, observation, ReactComponent


class FSConnectConfig(BaseModel):
    """Connect configuration for a filesystem"""

    path: str


class FSProvisionConig(BaseModel):
    """Provision configuration for a filesystem"""

    path: str


class FileInfo(BaseModel):
    """File information"""

    name: str
    type: int
    created: float
    updated: float
    size: int


class FileSystem(Device[FSConnectConfig, "FileSystem", FSProvisionConig]):
    """A filesystem device"""

    def __init__(self, root_path: str) -> None:
        super().__init__()
        self._root_path = root_path
        self._config: FSConnectConfig = FSConnectConfig(path=root_path)

    @classmethod
    def connect(cls, config: FSConnectConfig) -> "FileSystem":
        """Connect to a device from a configuration

        Args:
            config (C): Config

        Returns:
            D: The device
        """
        return cls(config.path)

    def disconnect(self) -> None:
        """Disconnect from the device"""
        pass

    @classmethod
    def ensure(cls, name: str, config: FSProvisionConig) -> "FileSystem":
        """Ensure device infrastructure exists

        Args:
            name (str): Name of the device
            config (P): Provisioner configuration

        Returns:
            D: the device
        """
        return cls(config.path)

    @classmethod
    def create(cls, name: str, config: FSProvisionConig) -> "FileSystem":
        """Create device infrastructure

        Args:
            name (str): Name of the device
            config (P): Provisioner configuration

        Returns:
            D: The device
        """
        return cls(config.path)

    @classmethod
    def react_component(cls) -> Optional[ReactComponent]:
        """React component for the device

        Returns:
            ReactComponent: React component
        """
        return None

    def view(self, background: bool = False) -> None:
        """View the device in the browser

        Args:
            background (bool, optional): Whether to run in the background. Defaults to False.
        """
        pass

    def connect_config(self) -> FSConnectConfig:
        """Connect configuration

        Returns:
            FSConnectConfg: Connect configuration for this device
        """
        return FSConnectConfig(path=self._config.path)

    @classmethod
    def connect_config_type(cls) -> Type[FSConnectConfig]:
        """Type of connect configuration

        Returns:
            Type[FSConnectConfig]: Type of connect configuration
        """
        return FSConnectConfig

    @classmethod
    def provision_config_type(cls) -> Type[FSProvisionConig]:
        """Type of provision configuration

        Returns:
            Type[P]: Type of provisioner configuration
        """
        return FSProvisionConig

    @action
    def create_file(self, path: str, content: str) -> None:
        """Create a file

        Args:
            path (str): Path relative to root path
            content (str): Content of the file
        """
        with open(f"{self._root_path}/{path}", "w") as f:
            f.write(content)

    @observation
    def read_file(self, path: str) -> str:
        """Read a file

        Args:
            path (str): Path relative to root path

        Returns:
            str: The file
        """
        with open(f"{self._root_path}/{path}", "r") as f:
            return f.read()

    @action
    def create_dir(self, path: str) -> None:
        """Create a directory

        Args:
            path (str): Path relative to root path
        """
        import os

        os.makedirs(f"{self._root_path}/{path}")

    @observation
    def list_dir(self, path: str) -> List[FileInfo]:
        """List a directory

        Args:
            path (str): Path relative to root path

        Returns:
            List[FileInfo]: The file info
        """
        import os
        import stat
        from datetime import datetime

        files = []
        for f in os.listdir(f"{self._root_path}/{path}"):
            f_path = f"{self._root_path}/{path}/{f}"
            st = os.stat(f_path)
            files.append(
                FileInfo(
                    name=f,
                    type=stat.S_IFMT(st.st_mode),
                    created=datetime.fromtimestamp(st.st_ctime).timestamp(),
                    updated=datetime.fromtimestamp(st.st_mtime).timestamp(),
                    size=st.st_size,
                )
            )
        return files

    @action
    def delete_file(self, path: str) -> None:
        """Delete a file

        Args:
            path (str): Path relative to root path
        """
        import os

        os.remove(f"{self._root_path}/{path}")

    @action
    def delete_dir(self, path: str) -> None:
        """Delete a directory

        Args:
            path (str): Path relative to root path
        """
        import os

        os.rmdir(f"{self._root_path}/{path}")

    @action
    def append_file(self, path: str, content: str) -> None:
        """Append to a file

        Args:
            path (str): Path relative to root path
            content (str): Content to append
        """
        with open(f"{self._root_path}/{path}", "a") as f:
            f.write(content)

    @action
    def get_diff(self, path: str, content: str) -> str:
        """Get diff of a file

        Args:
            path (str): Path relative to root path
            content (str): Content to diff against

        Returns:
            str: The diff in unified diff format
        """
        import difflib

        # Correcting the splitlines usage by explicitly using `keepends=True`
        with open(f"{self._root_path}/{path}", "r") as f:
            old = f.read()
            # Splitting lines and keeping line breaks
            diff = difflib.unified_diff(
                old.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=path,
                tofile=path,
            )
        return "\n".join(diff)

    @action
    def overwrite_file(self, path: str, content: str) -> None:
        """Overwrite a file

        Args:
            path (str): Path relative to root path
            content (str): Content to overwrite with
        """
        with open(f"{self._root_path}/{path}", "w") as f:
            f.write(content)
