import os
import time
from pathlib import Path
from dotenv import load_dotenv

import pickle  # package for load/dump cookies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.errorhandler import ElementNotInteractableException

from exceptions import AuthIncorrect

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# [Enter_points]
auth_url = "https://happyhopeenglish.getcourse.ru/cms/system/login"

# [Paths]
project_dir = Path(__file__).parent.parent
cookies_dir = project_dir.joinpath("cookies")
cookies_file_path = cookies_dir.joinpath(f"{email}_cookies")


def _read_cookies_from_file(driver: webdriver, cookies_file: Path) -> None:
    """Reads cookies from binary file and add them to webdriver session"""
    try:
        with cookies_file.open(mode="rb") as cookies:
            for cookie in pickle.load(cookies):
                driver.add_cookie(cookie)
    except Exception as err:
        print(f"Got EXCEPTION: "
              f"{err}.\n")


def _write_cookies_to_file(driver, cookies_file) -> None:
    """Writes cookies to binary file from a webdriver session"""
    try:
        print("\tSaving cookies...")
        cookies_file.parent.mkdir(parents=True, exist_ok=True)
        with cookies_file.open(mode="wb") as cookies:
            pickle.dump(driver.get_cookies(), cookies)
        print("\tCookies successfully saved")
    except Exception as err:
        print(f"Got EXCEPTION: "
              f"{err}.\n")


def click_button(driver, xpath: str):
    """Clicks on the button on the website"""
    enter_button = driver.find_element(by=By.XPATH, value=xpath)
    enter_button.click()


def fill_in_field(driver, xpath: str, value: str):
    """"Fills in the field on the website"""
    field = driver.find_element(by=By.XPATH, value=xpath)
    field.clear()
    field.send_keys(value)


def _to_auth_via_cookies(driver):
    """Authentication through cookies"""
    print("\t\tExecuting authentication with cookies...")
    _read_cookies_from_file(driver, cookies_file_path)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    try:
        enter_button_xpath = ("//button [@class='xdget-block xdget-button btn btn-primary btn-enter']"
                              "[@id='xdget831024_1_1']")
        click_button(driver, enter_button_xpath)
    except ElementNotInteractableException:
        print("\t\tERROR: Incorrect cookies")
        raise AuthIncorrect


def _to_auth_via_login_password(driver):
    """Authentication through login and password"""
    print("\t\tExecuting authentication with login and password...")
    login_xpath = "(//input [@class='form-control form-field-email'][@placeholder='Введите ваш эл. адрес'])[1]"
    fill_in_field(driver, login_xpath, email)

    time.sleep(1)

    password_xpath = "//input [@class='form-control form-field-password'][@placeholder='Введите пароль']"
    fill_in_field(driver, password_xpath, password)

    time.sleep(1)

    enter_button_xpath = ("//button [@class='xdget-block xdget-button btn btn-success'"
                          " and normalize-space()='Войти']")
    click_button(driver, enter_button_xpath)

    if not _check_err_button(driver):
        _write_cookies_to_file(driver, cookies_file_path)


def _check_err_button(driver):
    """Checks for an error button"""
    try:
        WebDriverWait(driver, 3).until(ec.presence_of_element_located((
            By.XPATH,
            "//button [@class='xdget-block xdget-button btn btn-success btn-error'"
            " and (normalize-space()='Неверный пароль' or normalize-space()='Неверный формат e-mail')]"
        )))
        print("\t\tERROR: Incorrect login or password")
    except TimeoutException:
        return False
    else:
        raise AuthIncorrect


def to_auth_user(driver):
    """
    Authentication user on the website.
    For beginning tries to authentication through cookies if they not exist, then
    authentication through login and password.
    """

    print("[Opening the site:")

    driver.get(url=auth_url)

    print("\tPassing authentication:")
    try:
        if cookies_file_path.exists():
            _to_auth_via_cookies(driver)
        else:
            _to_auth_via_login_password(driver)
    except AuthIncorrect:
        print("\tAuthentication is not successful.")
    else:
        print("\tAuthentication successful.")

    time.sleep(3)
    print("Closing the site.]")


if __name__ == '__main__':
    from drivers.google_chrome import create_google_chrome_driver
    # from drivers.firefox import create_firefox_driver

    browser_driver = create_google_chrome_driver()
    try:
        to_auth_user(browser_driver)
        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        browser_driver.close()
        browser_driver.quit()
