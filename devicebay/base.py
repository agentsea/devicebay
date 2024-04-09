from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Type

from pydantic import BaseModel
from toolfuse import Tool, action, observation, Action, Observation

D = TypeVar("D", bound="Device")
C = TypeVar("C", bound="BaseModel")


class ReactComponent:
    """A react component for a device"""

    source: str
    server_uri: str
    token: Optional[str] = None


class Device(Tool, ABC):
    """An agent device"""

    @classmethod
    @abstractmethod
    def envs(cls) -> dict:
        pass

    @abstractmethod
    def to_env(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_env(cls, config: BaseModel) -> D:
        pass

    @classmethod
    @abstractmethod
    def ensure(cls) -> D:
        pass

    @classmethod
    @abstractmethod
    def react_component(cls) -> ReactComponent:
        pass

    @abstractmethod
    def view(self, background: bool = False) -> None:
        pass

    @classmethod
    @abstractmethod
    def config(cls) -> Type[BaseModel]:
        pass

    @classmethod
    def serve(cls) -> None:
        pass


class MultiDevice(Device):
    pass
