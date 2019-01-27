# coding=utf-8
#
# MIT License
#
# Copyright (c) 2018 Sven Grübel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from urllib import quote

from PoroFetcherQueue import PoroFetcherQueue


class PoroFetcher:
    HOSTS = {
        "BR": "br1.api.riotgames.com",
        "EUNE": "eun1.api.riotgames.com",
        "EUW": "euw1.api.riotgames.com",
        "JP": "jp1.api.riotgames.com",
        "KR": "kr1.api.riotgames.com",
        "LAN": "la1.api.riotgames.com",
        "LAS": "la2.api.riotgames.com",
        "NA": "na1.api.riotgames.com",
        "OCE": "oc1.api.riotgames.com",
        "RU": "ru1.api.riotgames.com",
        "TR": "tr1.api.riotgames.com"
    }

    QUEUE_RANKED_SOLO = "RANKED_SOLO_5x5"
    QUEUE_RANKED_FLEX_SR = "RANKED_FLEX_SR"
    QUEUE_RANKED_FLEX_TT = "RANKED_FLEX_TT"

    def __init__(self, api_key):
        self._queues = dict()
        for region, host in self.HOSTS.iteritems():
            self._queues[region] = PoroFetcherQueue(host, api_key)

    def set_api_key(self, api_key):
        for queue in self._queues.values():
            queue.set_api_key(api_key)

    def request(self, region, url, return_func):
        self._queues[region].add(url, return_func)

    def wait_all(self):
        for queue in self._queues.values():
            queue.wait_all()

    ###################
    #                 #
    #    API CALLS    #
    #                 #
    ###################

    #######################
    # Champion Mastery v4 #
    #######################

    def champion_masteries_by_summoner(self, region, encrypted_summoner_id, return_func):
        self.request(region, "/lol/champion-mastery/v4/champion-masteries/by-summoner/{}".format(encrypted_summoner_id),
                     return_func)

    def champion_masteries_by_summoner_by_champion(self, region, encrypted_summoner_id, champion_id, return_func):
        self.request(region, "/lol/champion-mastery/v4/champion-masteries/by-summoner/{}/by-champion/{}"
                     .format(encrypted_summoner_id, champion_id), return_func)

    def champion_mastery_score_by_summoner(self, region, encrypted_summoner_id, return_func):
        self.request(region, "/lol/champion-mastery/v4/scores/by-summoner/{}".format(encrypted_summoner_id),
                     return_func)

    ###############
    # Champion v3 #
    ###############

    def champion_rotations(self, region, return_func):
        self.request(region, "/lol/platform/v3/champion-rotations", return_func)

    #############
    # League v4 #
    #############

    def _league_challengers_by_queue(self, region, queue, return_func):
        self.request(region, "/lol/league/v4/challengerleagues/by-queue/{}".format(queue), return_func)

    def league_challengers_solo(self, region, return_func):
        self._league_challengers_by_queue(region, self.QUEUE_RANKED_SOLO, return_func)

    def league_challengers_flex_sr(self, region, return_func):
        self._league_challengers_by_queue(region, self.QUEUE_RANKED_FLEX_SR, return_func)

    def league_challengers_flex_tt(self, region, return_func):
        self._league_challengers_by_queue(region, self.QUEUE_RANKED_FLEX_TT, return_func)

    def _league_grandmasters_by_queue(self, region, queue, return_func):
        self.request(region, "/lol/league/v4/grandmasterleagues/by-queue/{}".format(queue), return_func)

    def league_grandmasters_solo(self, region, return_func):
        self._league_grandmasters_by_queue(region, self.QUEUE_RANKED_SOLO, return_func)

    def league_grandmasters_flex_sr(self, region, return_func):
        self._league_grandmasters_by_queue(region, self.QUEUE_RANKED_FLEX_SR, return_func)

    def league_grandmasters_flex_tt(self, region, return_func):
        self._league_grandmasters_by_queue(region, self.QUEUE_RANKED_FLEX_TT, return_func)

    def _league_masterleagues_by_queue(self, region, queue, return_func):
        self.request(region, "/lol/league/v4/masterleagues/by-queue/{}".format(queue), return_func)

    def league_masterleagues_solo(self, region, return_func):
        self._league_masterleagues_by_queue(region, self.QUEUE_RANKED_SOLO, return_func)

    def league_masterleagues_flex_sr(self, region, return_func):
        self._league_masterleagues_by_queue(region, self.QUEUE_RANKED_FLEX_SR, return_func)

    def league_masterleagues_flex_tt(self, region, return_func):
        self._league_masterleagues_by_queue(region, self.QUEUE_RANKED_FLEX_TT, return_func)

    def league_by_league_id(self, region, league_id, return_func):
        self.request(region, "/lol/league/v4/leagues/{}".format(league_id), return_func)

    def league_positions_by_summoner(self, region, encrypted_summoner_id, return_func):
        self.request(region, "/lol/league/v4/positions/by-summoner/{}".format(encrypted_summoner_id), return_func)

    def league_positional_rank_queues(self, region, return_func):
        self.request(region, "/lol/league/v4/positional-rank-queues", return_func)

    def league_positional_rank_entries(self, region, queue, tier, division, position, page, return_func):
        self.request(region, "/lol/league/v4/positions/{}/{}/{}/{}/{}".format(queue, tier, division, position, page),
                     return_func)

    #################
    # LoL Status v3 #
    #################

    def status(self, region, return_func):
        self.request(region, "/lol/status/v3/shard-data", return_func)

    ############
    # Match v4 #
    ############

    def match_by_id(self, region, match_id, return_func):
        self.request(region, "/lol/match/v4/matches/{}".format(match_id), return_func)

    def match_list_by_account_id(self, region, encrypted_account_id, return_func):
        self.request(region, "/lol/match/v4/matchlists/by-account/{}".format(encrypted_account_id), return_func)

    def match_list_by_summoner_id(self, region, encrypted_summoner_id, return_func):
        def helper(response, status):
            if status == 200:
                self.match_list_by_account_id(region, response["accountId"], return_func)
            else:
                return_func(status, response)
        self.summoner_by_id(region, encrypted_summoner_id, helper)

    def match_timeline_by_id(self, region, match_id, return_func):
        self.request(region, "/lol/match/v4/timelines/by-match/{}".format(match_id), return_func)

    ################
    # Spectator v4 #
    ################

    def spectator_active_game_by_summoner(self, region, encrypted_summoner_id, return_func):
        self.request(region, "/lol/spectator/v4/active-games/by-summoner/{}".format(encrypted_summoner_id), return_func)

    def spectator_featured_games(self, region, return_func):
        self.request(region, "/lol/spectator/v4/featured-games", return_func)

    ###############
    # Summoner v4 #
    ###############

    def summoner_by_account(self, region, encrypted_accound_id, return_func):
        self.request(region, "/lol/summoner/v4/summoners/by-account/{}".format(encrypted_accound_id), return_func)

    def summoner_by_name(self, region, summoner_name, return_func):
        self.request(region, "/lol/summoner/v4/summoners/by-name/{}".format(quote(summoner_name.encode("utf8"))),
                     return_func)

    def summoner_by_puuid(self, region, encrypted_puuid, return_func):
        self.request(region, "/lol/summoner/v4/summoners/by-puuid/{}".format(encrypted_puuid), return_func)

    def summoner_by_id(self, region, encrypted_summoner_id, return_func):
        self.request(region, "/lol/summoner/v4/summoners/{}".format(encrypted_summoner_id), return_func)

    #######################
    # Third Party Code v4 #
    #######################

    def third_party_code(self, region, encrypted_summoner_id, return_func):
        self.request(region, "/lol/platform/v4/third-party-code/by-summoner/{}".format(encrypted_summoner_id),
                     return_func)
