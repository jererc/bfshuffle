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

`url` is the direct link to an experience map rotation, e.g.:
```
https://portal.battlefield.com/experience/mode/choose-maps?playgroundId=00000000-0000-0000-0000-000000000000
```

shuffle only from a list of favorites:
```
included_maps = ['ARICA HARBOR', 'BREAKAWAY', 'CASPIAN BORDER',
    'DISCARDED', 'FLASHPOINT', 'HAVEN', 'HOURGLASS', 'MANIFEST', 'ORBITAL',
    'RECLAIMED', 'RENEWAL', 'SPEARHEAD', 'VALPARAISO']
```

shuffle from all but these:
```
excluded_maps = ['EL ALAMEIN', 'REDACTED', 'STADIUM']
```

limit the number of maps:
```
max_maps = 5
```
