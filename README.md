PoroFetcher v0.2.0
==================

PoroFetcher is an asynchronous wrapper for the RiotGames API with multithreading support.

Installation
------------

Download the files PoroFetcher.py and PoroFetcherQueue.py and put them somewhere in your
projects include path

Hello World request
-------------------

```python
from PoroFetcher import PoroFetcher

api_key = "" # Put your API key here

def return_function(response, status):
    print status, response

# Initialize PoroFetcher
pf = PoroFetcher(api_key)

# Schedule a request to a specific endpoint. The response will be returned asynchronously
# to the given return function with signature return_function(response, status)
pf.champion_rotations("EUW", return_function)

# Wait until all pending requests have finished
pf.wait_all()
```

Supported API calls
-------------------

All v3 and v4 API endpoints (except the tournament API endpoints) are supported. This is the list
of all available API function of the ```PoroFetcher``` class.

```python
# Champion Mastery v4
champion_masteries_by_summoner(region, encrypted_summoner_id, return_func)
champion_masteries_by_summoner_by_champion(region, encrypted_summoner_id, champion_id, return_func)
champion_mastery_score_by_summoner(region, encrypted_summoner_id, return_func)

# Champion v3
champion_rotations(region, return_func)

# League v4
league_challengers_solo(region, return_func)
league_challengers_flex_sr(region, return_func)
league_challengers_flex_tt(region, return_func)
league_grandmasters_solo(region, return_func)
league_grandmasters_flex_sr(region, return_func)
league_grandmasters_flex_tt(region, return_func)
league_masterleagues_solo(region, return_func)
league_masterleagues_flex_sr(region, return_func)
league_masterleagues_flex_tt(region, return_func)
league_by_league_id(region, league_id, return_func)
league_positions_by_summoner(region, encrypted_summoner_id, return_func)
league_positional_rank_queues(region, return_func)
league_positional_rank_entries(self, region, queue, tier, division, position, page, return_func)

# LoL Status v3
status(region, return_func)

# Match v4
match_by_id(region, match_id, return_func)
match_list_by_account_id(region, encrypted_account_id, return_func)
match_list_by_summoner_id(region, encrypted_summoner_id, return_func)
match_timeline_by_id(region, match_id, return_func)

# Spectator v4
spectator_active_game_by_summoner(region, encrypted_summoner_id, return_func)
spectator_featured_games(region, return_func)

# Summoner v4
summoner_by_account(region, encrypted_accound_id, return_func)
summoner_by_name(region, summoner_name, return_func)
summoner_by_id(region, encrypted_summoner_id, return_func)
summoner_by_puuid(self, region, encrypted_puuid, return_func)

# Third Party Code v4
third_party_code(region, encrypted_summoner_id, return_func)
```