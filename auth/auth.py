import time
from pathlib import Path

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
import pickle

from auth_data import email, password

# [Enter_points]
main_url = "https://happyhopeenglish.getcourse.ru/cms/system/login"

# [Paths]
project_dir = Path(__file__).parent.parent
cookies_dir = project_dir.joinpath("cookies")
cookies_file_path = cookies_dir.joinpath(f"{email}_cookies")


def set_driver_options(mode: str = "prod"):
    options = webdriver.ChromeOptions()

    # change user_agent
    user_agent = UserAgent()
    options.add_argument(f"user-agent={user_agent.chrome}")

    # disable webdriver mode:
    # # for older ChromeDriver under version 79.0.3945.16
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    # for ChromDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    if mode == "prod":
        # background mode:
        # first way:
        options.add_argument("--headless")
        # # second way:
        # options.headless = True
    return options


def _read_cookies_from_file(webdriver, cookies_file):
    try:
        with open(cookies_file, "rb") as cookies:
            for cookie in pickle.load(cookies):
                webdriver.add_cookie(cookie)
    except Exception as err:
        print(f"Got EXCEPTION:"
              f"{err}.\n")


def _add_cookies_to_file(webdriver, cookies_file):
    try:
        print("\tSaving cookies...")
        with open(cookies_file, "wb") as cookies:
            pickle.dump(webdriver.get_cookies(), cookies)
        print("\tCookies successfully saved")
    except Exception as err:
        print(f"Got EXCEPTION:"
              f"{err}.\n")


def click_button(driver, xpath: str):
    enter_button = driver.find_element(by=By.XPATH, value=xpath)
    enter_button.click()


def fill_in_field(driver, xpath: str, value: str):
    field = driver.find_element(by=By.XPATH, value=xpath)
    field.clear()
    field.send_keys(value)


def _to_auth_via_cookies(driver):
    print("\t\tExecuting authentication with cookies...")
    _read_cookies_from_file(driver, cookies_file_path)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    enter_button_xpath = ("//button [@class='xdget-block xdget-button btn btn-primary btn-enter']"
                          "[@id='xdget831024_1_1']")
    click_button(driver, enter_button_xpath)


def _to_auth_via_login_password(driver):
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
    err_enter_button = _handle_incorrect_auth(driver)

    time.sleep(5)

    if not err_enter_button:
        _add_cookies_to_file(driver, cookies_file_path)


def _handle_incorrect_auth(driver):
    try:
        err_password_button = WebDriverWait(driver, 2).until(ec.presence_of_element_located((
            By.XPATH,
            "//button [@class='xdget-block xdget-button btn btn-success btn-error'"
            " and (normalize-space()='Неверный пароль' or normalize-space()='Неверный формат e-mail')]"
        )))
        print("\t\tERROR: Incorrect login or password")
    except TimeoutException:
        err_password_button = False
    return err_password_button


def to_auth_user(driver):
    print("[Opening the site:")

    driver.get(url=main_url)
    time.sleep(1)

    print("\tPassing authentication:")

    if cookies_file_path.exists():
        _to_auth_via_cookies(driver)
    else:
        _to_auth_via_login_password(driver)

    print("Closing the site.]")


if __name__ == '__main__':
    # [Driver]
    dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=set_driver_options(mode="dev"))
    try:
        to_auth_user(dr)
    except Exception as ex:
        print(ex)
    finally:
        dr.close()
        dr.quit()
