
[![PyPi version](https://badge.fury.io/py/circleparse.svg)](https://pypi.org/project/circleparse/)

# circleparse, a .osr and lzma parser

This fork is designed specifically for [Circlecore](https://github.com/circleguard/circlecore), and extends the functionality of the upstream repo by allowing parsing of a pure lzma bytestring, instead of the bytestring contents of an entire .osr file. Usage:

```python
from circleparse import parse_replay

# returns instance of Replay from an lzma bytestring with only the play_data field nonnull.
parse_replay(lzma_byte_string, pure_lzma=True)
```

Note that only information stored in the lzma bytestring is stored in the Replay instance. When pure_lzma is true, replay_data is the only populated field because lzma only contains cursor positioning and key presses. For more information, see [the wiki](https://osu.ppy.sh/help/wiki/osu%21_File_Formats/Osr_%28file_format%29).

## Installation

To install, simply

```sh
pip install circleparse
```

## Documentation

To parse a replay from a filepath:

```python
from circleparse import parse_replay_file

#returns instance of Replay
parse_replay_file("path/to/osr.osr")
```

To parse a replay from a bytestring:

```python
from circleparse import parse_replay

#returns instance of Replay given the replay data encoded as a bytestring
parse_replay(byte_string)
```

Replay instances provide these fields

```python
self.game_mode #GameMode enum
self.game_version #Integer
self.beatmap_hash #String
self.player_name #String
self.replay_hash #String
self.number_300s #Integer
self.number_100s #Integer
self.number_50s #Integer
self.gekis #Integer
self.katus #Integer
self.misses #Integer
self.score #Integer
self.max_combo #Integer
self.is_perfect_combo #Boolean
self.mod_combination #frozenset of Mods
self.life_bar_graph #String, unparsed as of now
self.timestamp #Python Datetime object
self.play_data #List of ReplayEvent instances
```

ReplayEvent instances provide these fields

```python
self.time_since_previous_action #Integer representing time in milliseconds
self.x #x axis location
self.y #y axis location
self.keys_pressed #bitwise sum of keys pressed, documented in OSR format page
```
