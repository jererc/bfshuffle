Battlefield 2042 Maps Shuffler
==============================

Generates a random map rotation for a [Battlefield 2042 Portal](https://portal.battlefield.com) experience.


Requirements
------------

- python
- brave or chrome


Install
-------

- download `bootstrap\bootstrap.bat` in some directory
- run it
- create the config file `user_settings.py` in the same directory
- run `bfshuffle.bat`


Example config:

```
CONFIGS = [
    {
        'url': 'https://portal.battlefield.com/experience/package/era?playgroundId=33950500-6dbf-11ef-b522-000000000000',
        'included_maps': [
            'ARICA HARBOR',
            'BATTLE OF THE BULGE',
            'BREAKAWAY',
            'CASPIAN BORDER',
            'DISCARDED',
            # 'EL ALAMEIN',
            'EXPOSURE',
            'FLASHPOINT',
            'HAVEN',
            'HOURGLASS',
            'KALEIDOSCOPE',
            'MANIFEST',
            'NOSHAHR CANALS',
            'ORBITAL',
            'RECLAIMED',
            # 'REDACTED',
            'RENEWAL',
            'SPEARHEAD',
            # 'STADIUM',
            'STRANDED',
            'VALPARAISO',
        ],
        'max_maps': 7,
    },
]
```
