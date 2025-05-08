import json
import logging
from typing import Optional, List

import requests

from .cache import APICache
from .models.match_detail import MatchDetail
from .models.match_timeline import MatchTimeline
from .models.riot_acount import RiotAccount
from .secrets import API_KEY


logger = logging.getLogger(__name__)


class RiotAPIClient:
    def __init__(self, api_key=API_KEY, api_cache=APICache(), region="europe"):
        self.api_key = api_key
        self.base_url = f"https://{region}.api.riotgames.com"
        self.headers = {
            "X-Riot-Token": self.api_key
        }
        self.api_cache = api_cache

    def _get_request_with_cache(self, url, cache_enabled=True, params=None, **kwargs):
        sorted_params = json.dumps(params, sort_keys=True)
        raw_key = f"{url}?{sorted_params}"
        if cache_enabled:
            cached_data = self.api_cache.get(raw_key)
            if cached_data:
                return cached_data

        response = requests.get(url, params, **kwargs)

        if response.status_code == 200:
            response_body = response.json()
            self.api_cache.set(raw_key, response_body)
            return response_body
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return None

    def get_account_by_riot_id(self, game_name, tag_line) -> RiotAccount:
        """
        Fetch Riot account info by Riot ID (gameName#tagLine)
        """
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        url = self.base_url + endpoint
        response_body = self._get_request_with_cache(url, headers=self.headers)
        return RiotAccount.from_dict(response_body)

    def get_match_ids_by_puuid(self, puuid: str, start: int = 0, count: int = 20) -> Optional[List[str]]:
        """
        Get list of match IDs for a given PUUID.
        """
        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            "start": start,
            "count": count,
            "queue": 400, # 5v5 normal
        }
        url = self.base_url + endpoint
        response_body = self._get_request_with_cache(url, cache_enabled=False, headers=self.headers, params=params)
        return response_body

    def get_match_detail(self, match_id: str) -> MatchDetail:
        endpoint = f"/lol/match/v5/matches/{match_id}"
        url = self.base_url + endpoint
        response_body = self._get_request_with_cache(url, headers=self.headers)
        return MatchDetail.from_dict(response_body)

    def get_match_timeline(self, match_id: str) -> MatchTimeline:
        endpoint = f"/lol/match/v5/matches/{match_id}/timeline"
        url = self.base_url + endpoint
        response_body = self._get_request_with_cache(url, headers=self.headers)
        return MatchTimeline.from_dict(response_body)
