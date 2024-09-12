from bfshuffle import BFShuffler


def main():
    url = 'https://portal.battlefield.com/experience/package/era?playgroundId=33950500-6dbf-11ef-b522-56bc172295fa'
    BFShuffler().shuffle(url)


if __name__ == '__main__':
    main()
