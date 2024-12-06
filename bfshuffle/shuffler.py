from contextlib import contextmanager
import os
from pprint import pformat
import random
import time
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import sync_playwright

from bfshuffle import NAME, WORK_DIR, logger


MAX_MAPS = 20


class Shuffler:
    def __init__(self, config):
        self.config = config
        self.work_dir = WORK_DIR

    @contextmanager
    def playwright_context(self):
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        state_path = os.path.join(self.work_dir, 'state.json')
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(
                    headless=False,
                    args=[
                        # '--disable-blink-features=AutomationControlled',
                    ],
                )
                context = browser.new_context(storage_state=state_path
                    if os.path.exists(state_path) else None)
                yield context
            finally:
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
        elements = page.locator('xpath=//app-map-row[contains(@class, "map-row") '
            'and contains(@class, "compact")]').all()
        res = []
        for element in reversed(elements):
            span = element.locator('xpath=.//span[@title]').nth(0)
            res.insert(0, span.text_content().strip().lower())
            element.locator('xpath=.//button[mat-icon[@data-mat-icon-name'
                '="remove_circle_outline"]]').click()
        return res

    def _get_available_map_elements(self, page):
        res = {}
        for element in page.locator('xpath=//app-map-row').element_handles():
            element.scroll_into_view_if_needed()
            span = element.query_selector('xpath=.//span[@title]')
            res[span.text_content().strip().lower()] = element
        return res

    def _select_maps(self, available_maps, map_rotation,
            included_maps, excluded_maps, max_maps):
        logger.info(f'map rotation:\n{pformat(map_rotation)}')
        if included_maps:
            new_map_rotation = list(available_maps
                & {r.lower() for r in included_maps})
        elif excluded_maps:
            new_map_rotation = list(available_maps
                - {r.lower() for r in excluded_maps})
        else:
            new_map_rotation = list(available_maps)
        if not new_map_rotation:
            logger.info('fallback on all available maps')
            new_map_rotation = list(available_maps)
        random.shuffle(new_map_rotation)
        new_map_rotation = new_map_rotation[:min(max_maps, MAX_MAPS)]
        if map_rotation and new_map_rotation[0] == map_rotation[0]:
            new_map_rotation.append(new_map_rotation.pop(0))
        logger.info(f'new map rotation:\n{pformat(new_map_rotation)}')
        return new_map_rotation

    def shuffle(self, page, url, included_maps=None, excluded_maps=None,
            max_maps=MAX_MAPS):
        map_url = self._get_map_rotation_url(url)
        logger.info(f'map rotation url: {map_url}')
        page.goto(map_url)
        page.wait_for_selector('xpath=//app-map-row', timeout=120000)
        current_maps = self._get_current_maps(page)
        available_map_elements = self._get_available_map_elements(page)
        available_maps = set(available_map_elements.keys())
        selected_maps = self._select_maps(available_maps,
            current_maps, included_maps, excluded_maps, max_maps)
        for name in selected_maps:
            element = available_map_elements[name]
            element.scroll_into_view_if_needed()
            element.query_selector(
                'xpath=.//button[mat-icon[@data-mat-icon-name="add_circle_outline"]]').click()
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
