import bs4
import psutil
from contextlib import suppress
import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Timer
from requests_futures import sessions
import model
import settings

timeout = 3
options = Options()
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-web-security")
options.add_argument("disable-gpu")
options.add_argument("headless")
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"
driver = undetected_chromedriver.Chrome(version_main=settings.chrome_version, options=options, desired_capabilities=caps)
wait = WebDriverWait(driver, timeout=60, poll_frequency=0.1, ignored_exceptions=[NoSuchElementException])


def terminate_chrome() -> None:
    for process in psutil.process_iter():
        with suppress(psutil.NoSuchProcess, ProcessLookupError):
            if process.name() == "chrome" and "--no-sandbox" in process.cmdline():
                process.terminate()


def parse_stat(divs: bs4.element.ResultSet, player: model.Player) -> None:
    if len(divs) != 0:
        player.set_stat(model.STAT.WINS, divs[0].select("li:nth-of-type(2)")[model.DATA.diff_number].text)
        player.set_stat(model.STAT.BATTLES, divs[0].select("li:nth-of-type(3)")[model.DATA.diff_number].text)
        player.set_stat(model.STAT.WINRATE, divs[0].select("li:nth-of-type(4)")[model.DATA.diff_number].text)
        player.set_stat(model.STAT.TIME_FIGHTER, divs[1].select("li:nth-of-type(6)")[model.DATA.diff_number].text)
        player.set_stat(model.STAT.TIME_ATTACKER, divs[1].select("li:nth-of-type(8)")[model.DATA.diff_number].text)


def findstat() -> None:
    if settings.lang == settings.Languages.RU:
        url_start: str = "https://warthunder.ru/ru/community/userinfo/?nick="
    else:
        url_start: str = "https://warthunder.com/en/community/userinfo/?nick="
    session = sessions.FuturesSession(max_workers=32)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-eundetected_chromedriveroding": "gzip, deflate, br",
        "accept-language": "ru,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "upgrade-insecure-requests": "1",
    }
    all_cookies = driver.get_cookies()
    cookies: str = ""
    for cookie in all_cookies:
        cookies += cookie["name"] + "=" + cookie["value"] + ';'
    user_agent = driver.execute_script("return navigator.userAgent;")
    headers["cookie"] = cookies
    headers["user-agent"] = user_agent
    session.headers.update(headers)
    # driver.quit()
    # Timer(timeout, terminate_chrome).start()
    futures = [(session.get(url_start + player.name), player) for player in model.DATA.get_players()]
    results = [(future.result(), player) for future, player in futures]
    retry: bool = True
    retry_list: list = []
    while retry:
        for i in range(len(results)):
            if results[i][0].status_code == 429:
                retry_list.append(i)
        new_futures = [(session.get(url_start + model.DATA.get_players()[i].name), model.DATA.get_players()[i]) for i in retry_list]
        new_results = [(future.result(), player) for future, player in new_futures]
        for i in range(len(new_results)):
            results[retry_list[i]] = new_results[i]
        if len(retry_list) == 0:
            retry = False
        retry_list = []

    for result, player in results:
        soup: bs4.BeautifulSoup = BeautifulSoup(result.content, "html.parser")
        parse_stat(soup.findAll("div", class_="user-stat__list-row"), player)
