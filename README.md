Battlefield 2042 Maps Shuffler
==============================

Generates a random map rotation for a [Battlefield 2042 Portal](https://portal.battlefield.com) experience.

A new chrome profile is created in order not to mess with the user profile.
The user has to login during the first run since it's a new profile.

On windows, a shortcut can be created to the `pythonw.exe` executable (from a virtualenv is better) with the script as argument, e.g.:
```
C:\Users\jerer\venv\Scripts\pythonw.exe C:\Users\jerer\bfshuffle\bfshuffle.py
```
or without a virtualenv:
```
C:\Users\jerer\AppData\Local\Programs\Python\Python312\pythonw.exe C:\Users\jerer\bfshuffle\bfshuffle.py
```


Requirements
------------

- python
- selenium (pip install selenium)
- google chrome


Config
------

Create a `user_settings.py` file in the same directory than `bfshuffle.py`, and which content is for instance:

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
