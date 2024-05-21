from typing import Optional, Type

from pydantic import BaseModel
from playwright.sync_api import sync_playwright, Browser, Page

from devicebay import Device, action, observation, ReactComponent


class PlaywrightConnectConfig(BaseModel):
    """Connect configuration for Playwright"""

    browser_type: str = "chromium"
    headless: bool = True


class PlaywrightProvisionConfig(BaseModel):
    """Provision configuration for Playwright"""

    pass


class Playwright(
    Device[PlaywrightConnectConfig, "Playwright", PlaywrightProvisionConfig]
):
    """A Playwright device"""

    def __init__(
        self,
        config: PlaywrightConnectConfig,
    ) -> None:
        super().__init__()
        self._config = config
        self._playwright = sync_playwright().start()
        self._browser: Browser = getattr(self._playwright, config.browser_type).launch(
            headless=config.headless
        )
        self._page: Page = self._browser.new_page()

    @classmethod
    def connect(cls, config: PlaywrightConnectConfig) -> "Playwright":
        """Connect to a device from a configuration

        Args:
            config (PlaywrightConnectConfig): Config

        Returns:
            Playwright: The device
        """
        return cls(config)

    def disconnect(self) -> None:
        """Disconnect from the device"""
        self._browser.close()
        self._playwright.stop()

    @classmethod
    def ensure(cls, name: str, config: PlaywrightProvisionConfig) -> "Playwright":
        """Ensure device infrastructure exists

        Args:
            name (str): Name of the device
            config (PlaywrightProvisionConfig): Provisioner configuration

        Returns:
            Playwright: The device
        """
        return cls(PlaywrightConnectConfig())

    @classmethod
    def create(cls, name: str, config: PlaywrightProvisionConfig) -> "Playwright":
        """Create device infrastructure

        Args:
            name (str): Name of the device
            config (PlaywrightProvisionConfig): Provisioner configuration

        Returns:
            Playwright: The device
        """
        return cls(PlaywrightConnectConfig())

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

    def connect_config(self) -> PlaywrightConnectConfig:
        """Connect configuration

        Returns:
            PlaywrightConnectConfig: Connect configuration for this device
        """
        return self._config

    @classmethod
    def connect_config_type(cls) -> Type[PlaywrightConnectConfig]:
        """Type of connect configuration

        Returns:
            Type[PlaywrightConnectConfig]: Type of connect configuration
        """
        return PlaywrightConnectConfig

    @classmethod
    def provision_config_type(cls) -> Type[PlaywrightProvisionConfig]:
        """Type of provision configuration

        Returns:
            Type[PlaywrightProvisionConfig]: Type of provisioner configuration
        """
        return PlaywrightProvisionConfig

    @action
    def navigate(self, url: str) -> None:
        """Navigate to a URL

        Args:
            url (str): URL to navigate to
        """
        self._page.goto(url)

    @observation
    def get_url(self) -> str:
        """Get the current URL

        Returns:
            str: The current URL
        """
        return self._page.url

    @action
    def click(self, selector: str) -> None:
        """Click on an element

        Args:
            selector (str): CSS selector of the element to click
        """
        self._page.click(selector)

    @action
    def type(self, selector: str, text: str) -> None:
        """Type text into an element

        Args:
            selector (str): CSS selector of the element to type into
            text (str): Text to type
        """
        self._page.fill(selector, text)

    @observation
    def get_text(self, selector: str) -> str:
        """Get the text of an element

        Args:
            selector (str): CSS selector of the element

        Returns:
            str: The text of the element
        """
        return self._page.inner_text(selector)

    @observation
    def get_page_source(self) -> str:
        """Get the page source

        Returns:
            str: The page source
        """
        return self._page.content()

    @action
    def press_key(self, selector: str, key: str) -> None:
        """Press a key on an element

        Args:
            selector (str): CSS selector of the element
            key (str): Key to press
        """
        self._page.press(selector, key)

    @action
    def hover(self, selector: str) -> None:
        """Hover over an element

        Args:
            selector (str): CSS selector of the element to hover over
        """
        self._page.hover(selector)

    @observation
    def get_attribute(self, selector: str, name: str) -> Optional[str]:
        """Get an attribute of an element

        Args:
            selector (str): CSS selector of the element
            name (str): Name of the attribute

        Returns:
            str: The attribute value
        """
        return self._page.get_attribute(selector, name)
