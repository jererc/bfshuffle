import os
import random
import subprocess
import time
from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
    ElementClickInterceptedException)
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By


CHROME_WIN_DATA_DIR = os.path.expanduser(
    r'~\AppData\Local\Google\Chrome\User Data')
CHROME_LINUX_DATA_DIR = os.path.expanduser(
    '~/.config/google-chrome')
IS_NT = os.name == 'nt'
DATA_DIR = CHROME_WIN_DATA_DIR if IS_NT else CHROME_LINUX_DATA_DIR
DEFAULT_PROFILE_DIR = 'selenium'
MAX_MAPS = 20


class BFShuffler(object):

    def __init__(self, profile_dir=DEFAULT_PROFILE_DIR):
        self.profile_dir = profile_dir
        self.driver = self._get_driver()


    def _get_driver(self):
        data_dir = CHROME_WIN_DATA_DIR if IS_NT else CHROME_LINUX_DATA_DIR
        if not os.path.exists(data_dir):
            raise Exception(f'chrome data dir {data_dir} does not exist')
        subprocess.call('taskkill /IM chrome.exe' if IS_NT else 'pkill chrome',
            shell=True)
        options = Options()
        options.add_argument(f'--user-data-dir={data_dir}')
        options.add_argument(f'--profile-directory={self.profile_dir}')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(1)
        return driver


    def _get_map_rotation_url(self, url):
        try:
            qs = parse_qs(urlparse(url).query)
            playground_id = qs['playgroundId'][0]
        except KeyError:
            raise Exception(f'invalid url {url}')
        return f'https://portal.battlefield.com/experience/mode/choose-maps?playgroundId={playground_id}'


    def _wait_for_login(self, url, poll_frequency=1, timeout=120):
        self.driver.get(url)
        end_ts = time.time() + timeout
        while time.time() < end_ts:
            try:
                return self.driver.find_element(By.XPATH,
                    '//div[@title and contains(., "CORE")]')
            except NoSuchElementException:
                time.sleep(poll_frequency)
        raise Exception('login timeout')


    def _find_map_elements(self):
        return self.driver.find_elements(By.XPATH, '//app-map-row')


    def _wait_for_maps(self, url, attempts=3, poll_frequency=1, timeout=5):
        for i in range(attempts):   # sometimes the content does not load
            end_ts = time.time() + timeout
            while time.time() < end_ts:
                if self._find_map_elements():
                    return
                time.sleep(poll_frequency)
            self.driver.get(url)
        raise Exception('maps timeout')


    def _clear_maps(self):
        xpath = '//button[mat-icon[@data-mat-icon-name="remove_circle_outline"]]'
        while True:
            try:
                self.driver.find_element(By.XPATH, xpath).click()
            except NoSuchElementException:
                break


    def _select_maps(self, all_maps, included_maps, excluded_maps, max_maps):
        print(f'all maps: {sorted(all_maps)}')
        if included_maps:
            candidates = list(all_maps & set(included_maps))
        elif excluded_maps:
            candidates = list(all_maps - set(excluded_maps))
        else:
            candidates = list(all_maps)
        random.shuffle(candidates)
        res = candidates[:min(max_maps, MAX_MAPS)]
        print(f'selected maps: {res}')
        return res


    def _scroll_from_element(self, element, y):
        scroll_origin = ScrollOrigin.from_element(element)
        (ActionChains(self.driver)
            .scroll_from_origin(scroll_origin, 0, y)
            .perform()
        )


    def _add_map_element(self, element):
        element.find_element(By.XPATH,
            './/button[mat-icon[@data-mat-icon-name="add_circle_outline"]]',
            ).click()


    def shuffle(self, url, included_maps=None, excluded_maps=None,
            max_maps=MAX_MAPS):
        map_url = self._get_map_rotation_url(url)
        self._wait_for_login(map_url)
        self._wait_for_maps(map_url)
        self._clear_maps()
        map_els = self._find_map_elements()   # reload to avoid stale elements
        get_name = lambda x: x.find_element(By.XPATH, './/span[@title]').text
        map_data = {get_name(e): {'el': e, 'y': e.location['y']}
            for e in map_els}
        selected_maps = self._select_maps(set(map_data.keys()),
            included_maps, excluded_maps, max_maps)
        y_offset = map_els[0].location['y']
        for name in selected_maps:
            data = map_data[name]
            try:
                self._add_map_element(data['el'])
            except ElementClickInterceptedException:
                y_delta = data['y'] - y_offset
                if y_delta:
                    self._scroll_from_element(map_els[0], y_delta)
                    try:
                        self._add_map_element(data['el'])
                    except ElementClickInterceptedException:
                        print(f'failed to add map {name}')

        self.driver.find_element(By.XPATH,
            '//button[@aria-label="save button"]').click()
        time.sleep(3)
        self.driver.quit()
