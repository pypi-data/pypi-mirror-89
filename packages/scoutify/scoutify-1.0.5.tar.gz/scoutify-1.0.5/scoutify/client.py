import json
from typing import Any

import requests as rq


class Scoutify(object):

    def __init__(
            self,
            access_token: str = None,
            client_id: str = None,
            client_secret: str = None,
            redirect_url: str = None,
            grant_access: str =None
    ):
        """
        Create a scoutify client
        Arguments:
            access_token: An OAUTH2 token
            client_id: A client id from user's client dashboard
            client_secret: A client secret from user's client dashboard
            redirect_url: A client secret defined in user's client dashboard
            grant_access: A grant access for client made
        """
        self._access_token = access_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_url = redirect_url
        self._header = None
        self._prefix = 'https://api.spotify.com/v1'

    def __get__(self, instance, owner):
        return self

    def __str__(self):
        return self._client_id

    def set_access_token(self, access_token: str):
        """
        Set access token from OAUTH2 token obtained.
        Arguments:
            access_token: access token obtained.
        """
        self._access_token = access_token
        self._header = {'Authorization': 'Bearer {}'.format(access_token)}

    def search(self, search_type: str, q: str) -> Any:
        """
        Searches for an item
        In this method, users will be able to search an artist, album, track, or playlist with keyword given
        Arguments:
            q: the search query (see how to write a query in the official documentation https://developer.spotify.com/documentation/web-api/reference/search/search/)
            search_type: the search type (available: artist, track, album, playlist)

        """
        if not self._header:
            return "No token available"
        search_url = "{}/{}".format(self._prefix, 'search')
        if search_type.lower() not in ['artist', 'track', 'album', 'playlist']:
            print('Invalid search type')
            return 'Invalid search type'
        params = {'type': search_type.lower(), 'q': q.lower()}
        resp = rq.get(search_url, params=params, headers=self._header)
        return resp.json()

    def several_artists(self, artist_ids: list):
        """
        Searches for several artists
        Spotify recommends to use several artists instead of single artist to prevent too many requests made.
        In this method, users will be able to search for multiple artists at once
        Arguments:
            artist_ids: List of artists' id
        """
        if not self._header:
            return "No token available"
        url = "{}/{}".format(self._prefix, 'artists')
        params = {'ids': ",".join(artist_ids)}
        resp = rq.get(url, params=params, headers=self._header)
        return resp.json()

    def get_current_user_profile(self) -> Any:
        """
        Current user's profile

        Returns:
            Information about current user
        """
        if not self._header:
            return "No token available"
        url = "{}/{}".format(self._prefix, 'me')
        resp = rq.get(url, headers=self._header)
        return resp.json()

    def find_user_profile(self, user_ids: str) -> Any:
        """
        Get a user's profile
        Arguments:
            user_ids: ID of a user wanted to find
        Returns:
            Information about user with id given.
        """
        if not self._header:
            return "No token available"
        url = "{}/{}/{}".format(self._prefix, 'user', user_ids)
        resp = rq.get(url, headers=self._header)
        return resp.json()

    def several_album(self, albums_ids: list):
        """
        Searches for several albums
        Spotify recommends to use several albums instead of single album to prevent too many requests made.
        In this method, users will be able to search for multiple albums at once
        Arguments:
            albums_ids: List of albums' id
        """
        if not self._header:
            return "No token available"
        url = "{}/{}".format(self._prefix, 'albums')
        params = {'ids': ",".join(albums_ids)}
        resp = rq.get(url, params=params, headers=self._header)
        return resp.json()

    def several_track(self, tracks_ids: list):
        """
        Searches for several tracks
        Spotify recommends to use several tracks instead of single track to prevent too many requests made.
        In this method, users will be able to search for multiple tracks at once
        Arguments:
            tracks_ids: List of tracks' id
        """
        if not self._header:
            return "No token available"
        url = "{}/{}".format(self._prefix, 'tracks')
        params = {'ids': ",".join(tracks_ids)}
        resp = rq.get(url, params=params, headers=self._header)
        return resp.json()

    def playlist(self, playlist_ids: str) -> Any:
        """
        Get information about playlist
        Arguments:
            playlist_ids: ID of playlist
        Returns:
            Information about playlist
        """
        if not self._header:
            return "No token available"
        url = "{}/{}/{}".format(self._prefix, 'playlists', playlist_ids)
        resp = rq.get(url, headers=self._header)
        return resp.json()
    
    def playlist_tracks(self, playlist_ids: str):
        """
        Get tracks inside a playlist
        Arguments:
            playlist_ids: ID of playlist
        """
        if not self._header:
            return "No token available"
        url = "{}/{}/{}/{}".format(self._prefix, 'playlists', playlist_ids, 'tracks')
        resp = rq.get(url, headers=self._header)
        return resp.json()
    
    def get_current_user_playlists(self) -> Any:
        """
        Get all playlists of current user.
        Returns:
            All playlists of current user.
        """
        if not self._header:
            return "No token available"
        url = "{}/{}/{}".format(self._prefix, 'me', 'playlists')
        resp = rq.get(url, headers=self._header)
        return resp.json()
    
    def user_playlists(self, user_ids: str) -> Any:
        """
        Get all playlists of a user.
        Arguments:
            user_ids: ID of a user.
        Returns:
            All playlists of user with ID given.
        """
        if not self._header:
            return "No token available"
        url = "{}/{}/{}/{}".format(self._prefix, 'users', user_ids, 'playlists')
        resp = rq.get(url, headers=self._header)
        return resp.json()
