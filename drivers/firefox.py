from dotenv import load_dotenv

from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from drivers.tools import mode_type, user_agent, set_background_mode

# It is needed for GH_TOKEN, because Firefox driver is located in GitHub
# GH_TOKEN is stored in .env
load_dotenv()


def create_firefox_driver(headers: str = user_agent.firefox,
                          mode: mode_type = 'dev',
                          ) -> webdriver.Firefox:
    """
    Creates Firefox driver.
    Sets the Firefox driver options and sets background mode if you select;
    Dev mode and a new version of Firefox are set by default;
    :param headers: Firefox headers such as 'User agent';
    :param mode: dev - show via browser, prod - without browser;
    :return: instance of webdriver.Firefox.
    """
    options = disable_webdriver_mode()
    options.add_argument(f"user-agent={headers}")  # set user agent for firefox

    if mode == "prod":
        set_background_mode(way=1, options=options)

    return webdriver.Firefox(service=Service(GeckoDriverManager().install()),
                             options=options)


def disable_webdriver_mode() -> webdriver.FirefoxOptions:
    """
    Disables the web driver mode, probably this func will stop working in the future.
    The websites to test this func:
    "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html",
    "https://bot.sannysoft.com/";
    :return: instance of webdriver.FirefoxOptions;
    """
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    return options
