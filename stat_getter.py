import time
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

THUNDERSKILL_URL = "https://thunderskill.com/", "/stat/"
WAR_THUNDER_URL = "https://warthunder.com/", "/community/userinfo/?nick="
PIXEL_STORM_URL = "https://warthunder.ru/", "/community/userinfo/?nick="  # Only this works for now

timeout = 3
options = Options()
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-web-security")
options.add_argument('--auto-open-devtools-for-tabs')
options.add_argument("disable-gpu")
options.add_argument("headless")
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"
url_start = PIXEL_STORM_URL[0] + settings.lang.value + PIXEL_STORM_URL[1]
driver = undetected_chromedriver.Chrome(version_main=settings.chrome_version, options=options, desired_capabilities=caps)


def terminate_chrome() -> None:
    for process in psutil.process_iter():
        with suppress(psutil.NoSuchProcess, ProcessLookupError):
            if process.name() == "chrome" and "--no-sandbox" in process.cmdline():
                process.terminate()


def parse_stat(divs: bs4.element.ResultSet, profile: bs4.element.ResultSet, player: model.Player) -> None:
    if len(divs) != 0:
        lvl = "".join([i for i in profile[0].select("li:nth-of-type(3)")[0].text if i.isdigit()])
        if lvl == "":
            lvl = "".join([i for i in profile[0].select("li:nth-of-type(4)")[0].text if i.isdigit()])
        player.set_stat(settings.STAT.LEVEL, lvl)
        player.set_stat(settings.STAT.WINS, divs[0].select("li:nth-of-type(2)")[model.DATA.diff_number].text)
        player.set_stat(settings.STAT.BATTLES, divs[0].select("li:nth-of-type(3)")[model.DATA.diff_number].text)
        player.set_stat(settings.STAT.WINRATE, divs[0].select("li:nth-of-type(4)")[model.DATA.diff_number].text)
        player.set_stat(settings.STAT.TIME_FIGHTER, divs[1].select("li:nth-of-type(6)")[model.DATA.diff_number].text)
        player.set_stat(settings.STAT.TIME_ATTACKER, divs[1].select("li:nth-of-type(8)")[model.DATA.diff_number].text)
        player.set_stat(settings.STAT.TIME_TANKS, divs[2].select("li:nth-of-type(7)")[model.DATA.diff_number].text)
        player.set_stat(settings.STAT.TIME_ANTI_AIR, divs[2].select("li:nth-of-type(10)")[model.DATA.diff_number].text)
        player.loaded = True


def findstat() -> None:
    players = model.DATA.get_players_to_load()

    # wait = WebDriverWait(driver, timeout=60, poll_frequency=0.1, ignored_exceptions=[NoSuchElementException])
    # driver.get(url_start + players[0].name)
    # wait.until(expected_conditions.presence_of_element_located((By.ID, "toTop")))
    # soup: bs4.BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
    # parse_stat(soup.findAll("div", class_="user-stat__list-row"), soup.findAll("div", class_="user-profile"), players[0])

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
    futures = [(session.get(url_start + player.name), player) for player in players]
    results = [(future.result(), player) for future, player in futures]
    retry: bool = settings.retry_to_get_all_stats
    retry_list: list = []
    while retry:
        for i in range(len(results)):
            if results[i][0].status_code == 429:
                retry_list.append(i)
            if results[i][0].status_code == 403:
                print("Got 403 code for " + url_start + results[i][1].name)
        new_futures = [(session.get(url_start + players[i].name), players[i]) for i in retry_list]
        new_results = [(future.result(), player) for future, player in new_futures]
        for i in range(len(new_results)):
            results[retry_list[i]] = new_results[i]
        if len(retry_list) == 0:
            retry = False
        retry_list = []

    for result, player in results:
        soup: bs4.BeautifulSoup = BeautifulSoup(result.content, "html.parser")
        parse_stat(soup.findAll("div", class_="user-stat__list-row"), soup.findAll("div", class_="user-profile"), player)
