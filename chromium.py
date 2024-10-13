import os
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


CONFIGS = {
    'nt': [
        {
            'binary': r'C:\Program Files\BraveSoftware'
                r'\Brave-Browser\Application\brave.exe',
            'data_dir': os.path.expanduser(
                r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data'),
        },
        {
            'binary': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'data_dir': os.path.expanduser(
                r'~\AppData\Local\Google\Chrome\User Data'),
        },
    ],
    'posix': [
        {
            'binary': '/opt/brave.com/brave/brave',
            'data_dir': os.path.expanduser(
                '~/.config/BraveSoftware/Brave-Browser'),
        },
        {
            'binary': '/opt/google/chrome/chrome',
            'data_dir': os.path.expanduser('~/.config/google-chrome'),
        },
    ],
}[os.name]
KILL_CMD = {
    'nt': 'taskkill /IM {binary}',
    'posix': 'pkill {binary}',
}[os.name]
PROFILE_DIR = 'selenium'


class Chromium:
    def __init__(self, profile_dir=PROFILE_DIR):
        self.profile_dir = profile_dir
        config = self._get_config()
        self.data_dir = config['data_dir']
        self.binary = config['binary']
        self.driver = self._get_driver()

    def _get_config(self):
        for config in CONFIGS:
            if all(os.path.exists(p) for p in config.values()):
                return config
        raise Exception('no available browser')

    def _kill_running_browser(self):
        subprocess.call(KILL_CMD.format(
            binary=os.path.basename(self.binary)), shell=True)

    def _get_driver(self):
        self._kill_running_browser()
        options = Options()
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
