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

- `url` is the direct link to an experience's map rotation, e.g.:
```
https://portal.battlefield.com/experience/mode/choose-maps?playgroundId=00000000-0000-0000-0000-000000000000
```

- `included_maps` allows to shuffle only from a list of favorites, e.g.:
```
included_maps = ['ARICA HARBOR', 'BREAKAWAY', 'CASPIAN BORDER',
    'DISCARDED', 'FLASHPOINT', 'HAVEN', 'HOURGLASS', 'MANIFEST', 'ORBITAL',
    'RECLAIMED', 'RENEWAL', 'SPEARHEAD', 'VALPARAISO']
```

- `excluded_maps` allows to exclude some maps, e.g.:
```
excluded_maps = ['EL ALAMEIN', 'REDACTED', 'STADIUM']
```

- `max_maps` limits the number of maps, e.g.:
```
max_maps = 5
```
