from abc import ABC, abstractmethod
from typing import TypeVar

from toolfuse import Tool

D = TypeVar("D", bound="Device")


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
    def from_env(cls) -> D:
        pass

    @classmethod
    @abstractmethod
    def react_component(cls) -> str:
        pass

    @abstractmethod
    def view(self, background: bool = False) -> None:
        pass

    @classmethod
    def serve(cls) -> None:
        pass
