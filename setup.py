from setuptools import setup, find_packages

setup(
    name='bfshuffle',
    version='0.1.0',
    author='jererc',
    author_email='jererc@gmail.com',
    url='https://github.com/jererc/bfshuffle',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.10',
    install_requires=[
        # 'svcutils @ git+https://github.com/jererc/svcutils.git@main#egg=svcutils',
        # 'webutils @ git+https://github.com/jererc/webutils.git@main#egg=webutils',
        'svcutils @ https://github.com/jererc/svcutils/archive/refs/heads/main.zip',
        'webutils @ https://github.com/jererc/webutils/archive/refs/heads/main.zip',
    ],
    extras_require={
        'dev': ['flake8', 'pytest'],
    },
    entry_points={
        'console_scripts': [
            'bfshuffle=bfshuffle.main:main',
        ],
    },
    include_package_data=True,
)
