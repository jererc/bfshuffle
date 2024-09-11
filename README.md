Battlefield 2042 Maps Shuffler
==============================

Generates a random map rotation for a [Battlefield 2042 Portal](https://portal.battlefield.com) experience.


Dependencies
------------

- python
- pip
- selenium (pip install selenium)
- google chrome


Params
------

- `url` is the experience's url, e.g.:
```
url = 'https://portal.battlefield.com/experience/package/era?playgroundId=33950500-6dbf-11ef-b522-01234567abcd'
```

- `included_maps` allows to shuffle only from a list of favorites, e.g.:
```
included_maps = ['ARICA HARBOR', 'BREAKAWAY', 'CASPIAN BORDER',
    'DISCARDED', 'FLASHPOINT', 'HAVEN', 'HOURGLASS', 'MANIFEST', 'ORBITAL',
    'RECLAIMED', 'RENEWAL', 'SPEARHEAD', 'VALPARAISO']
```

- `excluded_maps` allows to shuffle from all maps except these, e.g.:
```
excluded_maps = ['EL ALAMEIN', 'REDACTED', 'STADIUM']
```

- `max_maps` limits the number of maps, e.g.:
```
max_maps = 5
```
