# CHANGELOG : athletes-unlimited-py

## 0.0.1a3 - The AUX Softball Update

- Implemented `get_aux_softball_season_id()` to allow a developer and/or function to get a proper Athletes Unlimited X (AUX) season ID for a given AUX softball season.
- Implemented `get_aux_softball_season_pbp()`, a function that works in tandem with `get_au_softball_pbp()` to get all PBP data within a given AUX softball season.
- Implemented `get_aux_softball_season_player_box()`, a function that works in tandem with `get_au_softball_game_stats()` to get all player box stats in a AUX softball season.
- Implemented `get_aux_softball_season_team_box()`, a function that works in tandem with `get_au_softball_game_stats()` to get all team box stats in a AUX softball season.
- Reworked `get_au_softball_season()` to work with AUX Softball season IDs.
- Reworked `get_au_softball_game_stats()` to take `season_id` as a required input, instead of a `season`.
- Reworked `get_au_softball_pbp()` to take `season_id` as a required input, instead of a `season`.
- Updated package version to `0.0.1a3`.

## 0.0.1a2 - The Softball Update

- Updated column names for both pandas DataFrames returned by `get_au_basketball_pbp()`.
- Updated column names for the pandas DataFrame returned by `get_au_basketball_game_stats()`.
- Implemented `get_au_softball_season()`, to allow a developer and/or function to get the coresponding season for a given AU softball season ID.
- Implemented `get_au_softball_season_id()` to allow a developer and/or function to get a proper AU season ID for a given AU softball season.
- Implemented `get_au_softball_game_stats()`, a function that allows one to get the player and/or team box score stats for a game within a Athletes Unlimited (AU) softball season.
- Implemented `get_au_softball_pbp()`, a function that allows one to get all play-by-play (PBP) data from a given AU softball game.
- Implemented `get_au_softball_season_player_box()`, a function that works in tandem with `get_au_softball_game_stats()` to get all player box stats in a AU softball season.
- Implemented `get_au_softball_season_team_box()`, a function that works in tandem with `get_au_softball_game_stats()` to get all team box stats in a AU softball season.
- Implemented `get_au_softball_season_pbp()`, a function that works in tandem with `get_au_softball_pbp()` to get all PBP data within a given AU softball season.
- Fixed spelling errors in `CHANGELOG.md`.
- Updated package version to `0.0.1a2`.

## 0.0.1a1 - First Steps

- Implemented the basic structure of the package.
- Implemented `get_au_basketball_game_stats()`, a function that allows one to get the player and/or team box score stats for a game within a Athletes Unlimited (AU) basketball season.
- Implemented `get_au_basketball_season_player_box()`, a function that works in tandem with `get_au_basketball_game_stats()` to get all player box stats in a AU basketball season.
- Implemented `get_au_basketball_season_team_box()`, a function that works in tandem with `get_au_basketball_game_stats()` to get all team box stats in a AU basketball season.
- Implemented `get_au_basketball_season_id()` to allow a developer and/or function to get a proper AU season ID for a given AU basketball season.
- Implemented `get_au_basketball_season()` to allow a developer and/or function to get the coresponding season for a given AU basketball season ID.
- Implemented `get_au_basketball_pbp()`, a function that allows one to get all play-by-play (PBP) data from a given AU basketball game.
- Implemented `get_au_basketball_season_pbp()`, a function that works in tandem with `get_au_basketball_pbp()` to get all PBP data within a given AU basketball season.
