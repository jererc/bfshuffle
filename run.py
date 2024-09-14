from bfshuffle import BFShuffler


def main():
    url = 'https://portal.battlefield.com/experience/package/era?playgroundId=33950500-6dbf-11ef-b522-01234567abcd'
    excluded_maps = [
        'EL ALAMEIN',
        'REDACTED',
        'STADIUM',
    ]
    max_maps = 5
    BFShuffler().shuffle(url, excluded_maps=excluded_maps, max_maps=max_maps)


if __name__ == '__main__':
    main()
