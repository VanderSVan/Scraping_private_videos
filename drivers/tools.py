from typing import Literal
from selenium import webdriver
from fake_useragent import UserAgent


# Type hinting
mode_type = Literal['prod'] | Literal['dev']  # for driver start mode
version_type = Literal['new'] | str  # for Google Chrome version

user_agent = UserAgent()


def set_background_mode(way: Literal[1] | Literal[2], options: webdriver):
    """
    This func exists for demonstration purpose:
    it shows that there are 2 ways to set the background mode.
    """
    if way == 1:
        options.add_argument("--headless")
    else:
        options.headless = True
