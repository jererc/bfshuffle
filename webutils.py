import os
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


BROWSER_CONFIGS = {
    'nt': {
        'brave': {
            'binary': r'C:\Program Files\BraveSoftware'
                r'\Brave-Browser\Application\brave.exe',
            'data_dir': os.path.expanduser(
                r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data'),
        },
        'chrome': {
            'binary': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'data_dir': os.path.expanduser(
                r'~\AppData\Local\Google\Chrome\User Data'),
        },
    },
    'posix': {
        'brave': {
            'binary': '/opt/brave.com/brave/brave',
            'data_dir': os.path.expanduser(
                '~/.config/BraveSoftware/Brave-Browser'),
        },
        'chrome': {
            'binary': '/opt/google/chrome/chrome',
            'data_dir': os.path.expanduser('~/.config/google-chrome'),
        },
    },
}[os.name]
BROWSER_KILL_CMD = {
    'nt': 'taskkill /IM {binary}',
    'posix': 'pkill {binary}',
}[os.name]
BROWSER_PROFILE_DIR = 'selenium'


class Browser:
    def __init__(self, browser_id=None, profile_dir=BROWSER_PROFILE_DIR,
            headless=False, page_load_strategy=None):
        self.profile_dir = profile_dir
        self.headless = headless
        self.page_load_strategy = page_load_strategy
        config = self._get_config(browser_id)
        self.data_dir = config['data_dir']
        self.binary = config['binary']
        self.driver = self._get_driver()

    def _get_config(self, browser_id):
        if browser_id:
            try:
                return BROWSER_CONFIGS[browser_id]
            except KeyError:
                raise Exception(f'unsupported browser_id {browser_id}')
        for config in BROWSER_CONFIGS.values():
            if all(os.path.exists(p) for p in config.values()):
                return config
        raise Exception('no available browser')

    def _kill_running_browser(self):
        subprocess.call(BROWSER_KILL_CMD.format(
            binary=os.path.basename(self.binary)), shell=True)

    def _get_driver(self):
        self._kill_running_browser()
        options = Options()
        if self.page_load_strategy is not None:
            options.page_load_strategy = self.page_load_strategy
        if self.headless:
            options.add_argument('--headless')
        options.add_argument(f'--user-data-dir={self.data_dir}')
        options.add_argument(f'--profile-directory={self.profile_dir}')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches',
            ['enable-automation'])
        options.add_experimental_option('detach', True)
        options.binary_location = self.binary
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(1)
        return driver

    def quit(self):
        self.driver.quit()
