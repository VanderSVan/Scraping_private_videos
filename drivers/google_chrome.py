from packaging.version import parse as parse_ver

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from drivers.tools import mode_type, version_type, user_agent, set_background_mode


def create_google_chrome_driver(headers: str = user_agent.chrome,
                                mode: mode_type = 'dev',
                                version: version_type = 'new'
                                ) -> webdriver.Chrome:
    """
    Creates Google Chrome driver.
    Sets the Google Chrome driver options and sets background mode if you select;
    Dev mode and a new version of Google Chrome are set by default;
    :param headers: Google Chrome headers such as 'User agent';
    :param mode: dev - show via browser, prod - without browser;
    :param version: Google Chrome version;
    :return: instance of webdriver.Chrome.
    """
    options = disable_webdriver_mode(google_version=version)
    options.add_argument(f"user-agent={headers}")

    if mode == "prod":
        set_background_mode(way=1, options=options)

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=options)


def disable_webdriver_mode(google_version: version_type) -> webdriver.ChromeOptions:
    """
    Disables the web driver mode, probably this func will stop working in the future.
    The websites to test this func:
    "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html",
    "https://bot.sannysoft.com/";
    :param google_version: 0.0.0.0 (optionally);
    :return: instance of webdriver.ChromeOptions;
    """
    options = webdriver.ChromeOptions()
    if google_version == 'new' or parse_ver(google_version) >= parse_ver('79.0.3945.16'):
        # for ChromDriver version 79.0.3945.16 or over
        options.add_argument("--disable-blink-features=AutomationControlled")
    else:
        # for older ChromeDriver under version 79.0.3945.16
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
    return options
