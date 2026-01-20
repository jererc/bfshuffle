from setuptools import setup, find_packages

setup(
    name='bfshuffle',
    version='2026.01.20.062120',
    author='jererc',
    author_email='jererc@gmail.com',
    url='https://github.com/jererc/bfshuffle',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.10',
    install_requires=[
        'playwright',
        # 'svcutils @ git+https://github.com/jererc/svcutils.git@main#egg=svcutils',
        'svcutils @ https://github.com/jererc/svcutils/archive/refs/heads/main.zip',
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
