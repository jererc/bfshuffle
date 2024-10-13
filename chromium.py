import os
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


DATA_DIRS = {
    'nt': {
        'brave': r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data',
        'chrome': r'~\AppData\Local\Google\Chrome\User Data',
    },
    'posix': {
        'brave': '~/.config/BraveSoftware/Brave-Browser',
        'chrome': '~/.config/google-chrome',
    },
}[os.name]
BINARY_LOCATION = {
    'nt': {
        'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    },
    'posix': {
        'brave': '/opt/brave.com/brave/brave',
        'chrome': '/opt/google/chrome/chrome',
    },
}[os.name]
KILL_CMD = {
    'nt': 'taskkill /IM {binary}',
    'posix': 'pkill {binary}',
}[os.name]
PROFILE_DIR = 'selenium'


class Browser:
    def __init__(self, name, profile_dir=PROFILE_DIR):
        self.name = name
        try:
            self.data_dir = os.path.expanduser(DATA_DIRS[self.name])
            self.binary_location = BINARY_LOCATION[self.name]
        except KeyError:
            raise Exception(f'unhandled browser {name}')
        self.profile_dir = profile_dir
        self.driver = self._get_driver()

    def _kill_running_browser(self):
        subprocess.call(KILL_CMD.format(
            binary=os.path.basename(self.binary_location)), shell=True)

    def _get_driver(self):
        if not os.path.exists(self.data_dir):
            raise Exception(f'{self.data_dir} not found')
        if not os.path.exists(self.binary_location):
            raise Exception(f'{self.binary_location} not found')
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
        options.binary_location = self.binary_location
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(1)
        return driver

    def quit(self):
        self.driver.quit()
