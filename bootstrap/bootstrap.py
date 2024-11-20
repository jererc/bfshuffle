import os
import urllib.request

url = 'https://raw.githubusercontent.com/jererc/svcutils/refs/heads/main/svcutils/bootstrap.py'
exec(urllib.request.urlopen(url).read().decode('utf-8'))
Bootstrapper(
    name='bfshuffle',
    cmd_args=['bfshuffle.main'],
    install_requires=[
        # 'git+https://github.com/jererc/bfshuffle.git',
        'bfshuffle @ https://github.com/jererc/bfshuffle/archive/refs/heads/main.zip',
    ],
    force_reinstall=True,
).setup_script()
