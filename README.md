Battlefield 2042 Maps Shuffler
==============================

Creates a shuffled map rotation for a [Battlefield 2042 Portal](https://portal.battlefield.com) experience.


Dependencies
------------

- python
- pip
- selenium (pip install selenium)
- google chrome


Params
------

only from a list of favorites:
```
included_maps = ['ARICA HARBOR', 'BREAKAWAY', 'CASPIAN BORDER',
    'DISCARDED', 'FLASHPOINT', 'HAVEN', 'HOURGLASS', 'MANIFEST', 'ORBITAL',
    'RECLAIMED', 'RENEWAL', 'SPEARHEAD', 'VALPARAISO']
```

from all but these:
```
excluded_maps = ['EL ALAMEIN', 'REDACTED', 'STADIUM']
```

limit the number of maps:
```
max_maps = 5
```
