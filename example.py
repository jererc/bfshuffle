from bfshuffle import BFShuffler


def main():
    url = 'https://portal.battlefield.com/experience/mode/choose-maps?playgroundId=00000000-0000-0000-0000-000000000000'
    included_maps = ['ARICA HARBOR', 'BREAKAWAY', 'CASPIAN BORDER',
        'DISCARDED', 'FLASHPOINT', 'HAVEN', 'HOURGLASS', 'MANIFEST', 'ORBITAL',
        'RECLAIMED', 'RENEWAL', 'SPEARHEAD', 'VALPARAISO']
    max_maps = 5
    BFShuffler().shuffle(url, included_maps=included_maps, max_maps=max_maps)


if __name__ == '__main__':
    main()
