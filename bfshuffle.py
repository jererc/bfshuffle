import os.path
import random
import subprocess
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By


CHROME_PROFILE_PATH = os.path.expanduser(
    r'~\AppData\Local\Google\Chrome\User Data')
MAX_MAPS = 20


class BFShuffler(object):

    def __init__(self):
        self.driver = self._get_driver()


    def _get_driver(self):
        if not os.path.exists(CHROME_PROFILE_PATH):
            raise Exception(f'chrome profile path {CHROME_PROFILE_PATH}'
                ' does not exist')
        subprocess.call('taskkill /IM chrome.exe', shell=True)
        options = Options()
        options.add_argument(f'--user-data-dir={CHROME_PROFILE_PATH}')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(1)
        driver.switch_to.window(driver.window_handles[-1])
        return driver


    def _find_map_elements(self):
        return self.driver.find_elements(By.XPATH, '//app-map-row')


    def _wait_for_maps(self, url, attempts=3, poll_frequency=1, timeout=5):
        for i in range(attempts):   # sometimes the content does not load
            self.driver.get(url)
            end_ts = time.time() + timeout
            while time.time() < end_ts:
                if self._find_map_elements():
                    return
                time.sleep(poll_frequency)
        raise Exception('timeout')


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


    def shuffle(self, url, included_maps=None, excluded_maps=None,
            max_maps=MAX_MAPS):
        self._wait_for_maps(url)
        self._clear_maps()
        map_els = self._find_map_elements()   # needs to be reloaded to avoid stale elements
        get_name = lambda x: x.find_element(By.XPATH, './/span[@title]').text
        map_data = {get_name(e): {'el': e, 'y': e.location['y']}
            for e in map_els}
        selected_maps = self._select_maps(set(map_data.keys()),
            included_maps, excluded_maps, max_maps)
        y_offset = map_els[0].location['y']
        for name in selected_maps:
            data = map_data[name]
            y_delta = data['y'] - y_offset
            if y_delta:
                self._scroll_from_element(map_els[0], y_delta)
            data['el'].find_element(By.XPATH,
                './/button[mat-icon[@data-mat-icon-name="add_circle_outline"]]',
                ).click()
        self.driver.find_element(By.XPATH,
            '//button[@aria-label="save button"]').click()
        time.sleep(3)
