import argparse
import os

from svcutils.service import Config

from bfshuffle.shuffler import Shuffler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', default=os.getcwd())
    args = parser.parse_args()
    path = os.path.realpath(os.path.expanduser(args.path))
    config = Config(os.path.join(path, 'user_settings.py'))
    Shuffler(config).run()


if __name__ == '__main__':
    main()
