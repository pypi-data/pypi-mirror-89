# pylint: disable=too-many-arguments
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import urllib.request
from collections import Counter
from datetime import datetime
from json import loads
from sys import maxsize
from typing import List, Dict

from media_tools.util.buying.track import Track


class LastFM:

    API_BASE = 'http://ws.audioscrobbler.com/2.0/'

    def __init__(self, user: str, api_key: str) -> None:
        self.user = user
        self.api_key = api_key

    def base_url(self, method: str, limit: int) -> str:
        return f'{self.API_BASE}?method={method}&user={self.user}&api_key={self.api_key}&' \
            f'limit={limit}&format=json'

    def get_top_tracks(
            self, period: str = 'overall', limit: int = 50, min_plays: int = 1, page: int = 1
    ) -> List[Track]:
        url = f'{self.base_url("user.gettoptracks", limit * page)}&period={period}'
        tracks = self.get_response(url, 'toptracks')['track']
        top_tracks: List[Track] = [None] * len(tracks)
        for track in tracks:
            top_tracks[int(track['@attr']['rank']) - 1] = Track.from_dict(track)
        return [
            track for track in top_tracks if track.playcount >= min_plays
        ][limit * (page - 1):limit * page]

    def get_tracks_by_period(
            self, from_date: datetime, to_date: datetime = datetime.now(), limit: int = 50,
            min_plays: int = 1, page: int = 1
    ) -> List[Track]:
        url = f'{self.base_url("user.getrecenttracks", 200)}&' \
            f'from={from_date.timestamp()}&to={to_date.timestamp()}'
        tracks = Counter(self.get_tracks_paged(url, 'recenttracks'))
        for track, playcount in tracks.items():
            track.playcount = playcount
        return [
            track for track, num_plays in tracks.most_common(limit * page) if num_plays >= min_plays
        ][limit * (page - 1):limit * page]

    def get_tracks_paged(self, url: str, method: str) -> List[Track]:
        tracks = []
        page, total_pages = 1, maxsize
        while page <= total_pages:
            response = self.get_response(f'{url}&page={page}', method)
            total_pages = int(response['@attr']['totalPages'])
            page = int(response['@attr']['page']) + 1
            tracks.append(response['track'])
        return [Track.from_dict(t) for chunk in tracks for t in chunk]

    @staticmethod
    def get_response(url: str, method: str) -> Dict:
        with urllib.request.urlopen(url) as response:
            return loads(response.read())[method]
