from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Type, Generic

from pydantic import BaseModel
from toolfuse import Tool, action, observation, Action, Observation

from .models import DeviceModel

D = TypeVar("D", bound="Device")
C = TypeVar("C", bound="BaseModel")
P = TypeVar("P", bound="BaseModel")


class ReactComponent:
    """A react component for a device"""

    source: str
    server_uri: str
    token: Optional[str] = None


class Device(Generic[C, D, P], Tool, ABC):
    """An agent device"""

    @classmethod
    @abstractmethod
    def connect(cls, config: C) -> D:
        """Connect to a device from a configuration

        Args:
            config (C): Config

        Returns:
            D: The device
        """
        pass

    @classmethod
    @abstractmethod
    def ensure(cls, name: str, config: P) -> D:
        """Ensure device infrastructure exists

        Args:
            name (str): Name of the device
            config (P): Provisioner configuration

        Returns:
            D: the device
        """
        pass

    @classmethod
    @abstractmethod
    def create(cls, name: str, config: P) -> D:
        """Create device infrastructure

        Args:
            name (str): Name of the device
            config (P): Provisioner configuration

        Returns:
            D: The device
        """
        pass

    @classmethod
    @abstractmethod
    def react_component(cls) -> ReactComponent:
        """React component for the device

        Returns:
            ReactComponent: React component
        """
        pass

    @abstractmethod
    def view(self, background: bool = False) -> None:
        """View the device in the browser

        Args:
            background (bool, optional): Whether to run in the background. Defaults to False.
        """
        pass

    @abstractmethod
    def connect_config(self) -> C:
        """Connect configuration

        Returns:
            C: Connect configuration for this device
        """
        pass

    @classmethod
    @abstractmethod
    def connect_config_type(cls) -> Type[C]:
        """Type of connect configuration

        Returns:
            Type[C]: Type of connect configuration
        """
        pass

    @classmethod
    @abstractmethod
    def provision_config_type(cls) -> Type[P]:
        """Type of provision configuration

        Returns:
            Type[P]: Type of provisioner configuration
        """
        pass

    def to_schema(self) -> DeviceModel:
        """Convert the device to server transport schema

        Returns:
            DeviceModel: Device schema
        """
        config_type = self.connect_config_type()
        config_instance = self.connect_config()
        if not isinstance(config_instance, config_type):
            raise TypeError(
                f"Expected config instance of type {config_type.__name__}, but got {type(config_instance).__name__}"
            )
        parametrized_device_model = DeviceModel[config_type](
            name=self.name(), config=config_instance
        )
        return parametrized_device_model

    @classmethod
    def serve(cls) -> None:
        pass


class MultiDevice(Device):
    """A device of multiple devices"""

    pass
