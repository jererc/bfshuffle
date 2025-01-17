from contextlib import contextmanager
import os
from pprint import pformat
import random
import time
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import TimeoutError, sync_playwright

from bfshuffle import WORK_DIR, logger


MAX_MAPS = 20


class Shuffler:
    def __init__(self, config):
        self.config = config

    @contextmanager
    def playwright_context(self):
        state_path = os.path.join(WORK_DIR, 'state.json')
        with sync_playwright() as p:
            context = None
            try:
                browser = p.chromium.launch(
                    headless=False,
                    args=[
                        # '--disable-blink-features=AutomationControlled',
                    ],
                )
                context = browser.new_context(
                    storage_state=state_path
                        if os.path.exists(state_path) else None,
                )
                yield context
            finally:
                if context:
                    context.storage_state(path=state_path)
                    context.close()

    def _get_map_rotation_url(self, url):
        try:
            playground_id = parse_qs(urlparse(url).query)['playgroundId'][0]
        except KeyError:
            raise Exception(f'invalid url {url}')
        return 'https://portal.battlefield.com/experience/mode/choose-maps' \
            f'?playgroundId={playground_id}'

    def _get_current_maps(self, page):
        res = []
        elements = page.locator('xpath=//app-map-row[contains(@class, '
            '"map-row") and contains(@class, "compact")]').all()
        for element in reversed(elements):
            span = element.locator('xpath=.//span[@title]').nth(0)
            res.insert(0, span.text_content().strip().lower())
            element.locator('xpath=.//button[mat-icon[@data-mat-icon-name'
                '="remove_circle_outline"]]').click()
        return res

    def _get_available_maps(self, page):
        res = {}
        for element in page.locator('xpath=//app-map-row[not(contains(@class, '
                '"compact"))]/div/div/span[@title]').all():
            text = element.text_content().strip()
            res[text.lower()] = text
        return res

    def _select_maps(self, available_maps, current_maps,
                     included_maps, excluded_maps, max_maps):
        if included_maps:
            selected_maps = list(available_maps
                & {r.lower() for r in included_maps})
        elif excluded_maps:
            selected_maps = list(available_maps
                - {r.lower() for r in excluded_maps})
        else:
            selected_maps = list(available_maps)
        if not selected_maps:
            logger.info('fallback on all available maps')
            selected_maps = list(available_maps)
        random.shuffle(selected_maps)
        selected_maps = selected_maps[:min(max_maps, MAX_MAPS)]
        if current_maps and selected_maps[0] == current_maps[0]:
            selected_maps.append(selected_maps.pop(0))
        return selected_maps

    def _wait_for_maps(self, map_url, page, selector_timeout=10000,
                       timeout=120):
        end_ts = time.time() + timeout
        page.goto(map_url)
        while time.time() < end_ts:
            try:
                page.wait_for_selector('xpath=//app-map-row',
                    timeout=selector_timeout)
                return
            except TimeoutError:
                try:
                    element = page.locator('xpath=//div[@title '
                        'and contains(text(), "CORE")]').all()
                except Exception:   # wait for login
                    element = None
                if element:
                    logger.warning('no map, reloading...')
                    page.goto(map_url)
                    end_ts = time.time() + selector_timeout * 2

    def shuffle(self, page, url, included_maps=None, excluded_maps=None,
                max_maps=MAX_MAPS):
        map_url = self._get_map_rotation_url(url)
        logger.info(f'map rotation url: {map_url}')
        self._wait_for_maps(map_url, page)
        current_maps = self._get_current_maps(page)
        logger.info(f'current map rotation:\n{pformat(current_maps)}')
        available_maps = self._get_available_maps(page)
        logger.info(f'available maps:\n{pformat(list(available_maps.keys()))}')
        selected_maps = self._select_maps(available_maps.keys(),
            current_maps, included_maps, excluded_maps, max_maps)
        logger.info(f'new map rotation:\n{pformat(selected_maps)}')
        for name in selected_maps:
            map_title = available_maps[name]
            element = page.locator('xpath=//app-map-row[not(contains(@class, '
                '"compact")) and .//span[@title '
                f'and contains(text(), "{map_title}")]]').nth(0)
            element.scroll_into_view_if_needed()
            element.locator('xpath=.//button[mat-icon['
                '@data-mat-icon-name="add_circle_outline"]]').nth(0).click()
        page.wait_for_selector('xpath=//button[@aria-label="save button"]',
            timeout=10000).click()
        time.sleep(3)

    def run(self):
        with self.playwright_context() as context:
            page = context.new_page()
            for config in self.config.CONFIGS:
                try:
                    self.shuffle(page, **config)
                except Exception:
                    logger.exception('failed')
