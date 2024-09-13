import os
from pprint import pformat
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


IS_WIN = os.name == 'nt'
DATA_DIR = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data'
    if IS_WIN else '~/.config/google-chrome')
DEFAULT_PROFILE_DIR = 'selenium'
MAX_MAPS = 20


class BFShuffler(object):

    def __init__(self, profile_dir=DEFAULT_PROFILE_DIR):
        self.profile_dir = profile_dir
        self.driver = self._get_driver()


    def _get_driver(self):
        if not os.path.exists(DATA_DIR):
            raise Exception(f'chrome data dir {DATA_DIR} does not exist')
        subprocess.call('taskkill /IM chrome.exe'
            if IS_WIN else 'pkill chrome', shell=True)
        options = Options()
        options.add_argument(f'--user-data-dir={DATA_DIR}')
        options.add_argument(f'--profile-directory={self.profile_dir}')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches',
            ['enable-automation'])
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(1)
        return driver


    def _get_map_rotation_url(self, url):
        try:
            playground_id = parse_qs(urlparse(url).query)['playgroundId'][0]
        except KeyError:
            raise Exception(f'invalid url {url}')
        return 'https://portal.battlefield.com/experience/mode/choose-maps' \
            f'?playgroundId={playground_id}'


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


    def _get_map_name(self, map_element):
        return map_element.find_element(By.XPATH, './/span[@title]').text


    def _get_and_clear_map_rotation(self):
        res = []
        while True:
            try:
                el = self.driver.find_element(By.XPATH,
                    '//app-map-row[contains(@class, "map-row") and contains(@class, "compact")]')
                res.append(self._get_map_name(el))
                el.find_element(By.XPATH,
                    './/button[mat-icon[@data-mat-icon-name="remove_circle_outline"]]',
                    ).click()
            except NoSuchElementException:
                break
        return res


    def _select_maps(self, available_maps, map_rotation,
            included_maps, excluded_maps, max_maps):
        print(f'map rotation:\n{pformat(map_rotation)}')
        print(f'available maps:\n{pformat(sorted(available_maps))}')
        if included_maps:
            new_map_rotation = list(available_maps & set(included_maps))
        elif excluded_maps:
            new_map_rotation = list(available_maps - set(excluded_maps))
        else:
            new_map_rotation = list(available_maps)
        random.shuffle(new_map_rotation)
        new_map_rotation = new_map_rotation[:min(max_maps, MAX_MAPS)]
        if map_rotation and new_map_rotation[0] == map_rotation[0]:
            new_map_rotation.append(new_map_rotation.pop(0))
        print(f'new map rotation:\n{pformat(new_map_rotation)}')
        return new_map_rotation


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
        map_rotation = self._get_and_clear_map_rotation()
        map_els = self._find_map_elements()   # reload to avoid stale elements
        map_data = {self._get_map_name(e): {'el': e, 'y': e.location['y']}
            for e in map_els}
        selected_maps = self._select_maps(set(map_data.keys()),
            map_rotation, included_maps, excluded_maps, max_maps)
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
