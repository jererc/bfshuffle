import argparse
import os

from svcutils.service import Config

from bfshuffle.shuffler import Shuffler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p')
    args = parser.parse_args()
    config = Config(
        os.path.join(os.path.expanduser(args.path), 'user_settings.py'),
        BROWSER_ID='chrome',
    )
    Shuffler(config).run()


if __name__ == '__main__':
    main()
