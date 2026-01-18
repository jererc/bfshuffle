import os
import urllib.request

url = 'https://raw.githubusercontent.com/jererc/svcutils/refs/heads/main/svcutils/bootstrap.py'
exec(urllib.request.urlopen(url).read().decode('utf-8'))
Bootstrapper(
    name='bfshuffle',
    install_requires=[
        # 'git+https://github.com/jererc/bfshuffle.git',
        'bfshuffle @ https://github.com/jererc/bfshuffle/archive/refs/heads/main.zip',
    ],
    force_reinstall=True,
    init_cmds=[
        ['playwright', 'install-deps'],
    ],
    extra_cmds=[
        ['playwright', 'install', 'chromium'],
    ],
    shortcuts=[
        {'name': 'bfshuffle', 'args': ['bfshuffle.main', '-p', os.getcwd()]},
    ],
    download_assets=[
        {'filename': 'user_settings.py', 'url': 'https://raw.githubusercontent.com/jererc/bfshuffle/refs/heads/main/bootstrap/user_settings.py'},
    ],
)
