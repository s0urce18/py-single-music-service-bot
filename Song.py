# imports ----------------------------------
from ytmusicapi import YTMusic
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from deezer import Client
import json
# ------------------------------------------

ytm = YTMusic() # Youtube Music

# Spotify ----------------------------------
sp_config_file = open("spotify_config.json", "r")

"""spotify_config.json:
{
    "cid": *Client ID*,
    "secret": *Client Secret*,
    "rur": *Redirect URIs*,
    "scope": "user-library-read",
    "user": *User name*
}
"""

sp_config_dict = json.loads(sp_config_file.read())
sp = Spotify(auth_manager=SpotifyOAuth(client_id=sp_config_dict["cid"], 
                                        client_secret=sp_config_dict["secret"], 
                                        redirect_uri=sp_config_dict["rur"], 
                                        scope=sp_config_dict["scope"], 
                                        username=sp_config_dict["user"])
            )
# ------------------------------------------

dz = Client() # Deezer

class Song:

    _name: str = "" # name
    _ytm_id: str = "" # YT Music ID
    _sp_id: str = "" # Spotify ID
    _dz_id: str = "" # Deezer ID

    def __init__(self, name: str = "", ytm_link: str = "", sp_link: str = "", dz_link: str = "") -> None:
        try:
            if name != "":
                self._name = name
            elif ytm_link != "":
                self._name = ytm.get_song(videoId=ytm_link[ytm_link.find("=") + 1 : ytm_link.find("&")])["videoDetails"]["title"]
            elif sp_link != "":
                self._name = sp.track(sp_link)["name"]
            elif dz_link != "":
                self._name = dz.get_track(dz_link[dz_link.rfind("/") + 1 : ]).title
            else:
                raise Exception("We can't find your track. Please, give us some info(name or any link)")
        except:
            print("Something went wrong. Recheck data that you give")

    def _count_ytm_id(self) -> None: # count YT Music ID
        self._ytm_id = str(ytm.search(query=self._name, filter="songs")[0]["videoId"])

    def _count_sp_id(self) -> None: # count Spotify ID 
        self._sp_id = str(sp.search(q=self._name, type="track")["tracks"]["items"][0]["id"])

    def _count_dz_id(self) -> None: # count Deezer ID
        self._dz_id = str(dz.search(query=self._name)[0].id)

    def get_name(self) -> str: # get name
        return self._name

    def get_ytm_id(self) -> str: # get YT Music ID
        if self._ytm_id == "":
            self._count_ytm_id()
        return self._ytm_id

    def get_sp_id(self) -> str: # get Spotify ID
        if self._sp_id == "":
            self._count_sp_id()
        return self._sp_id

    def get_dz_id(self) -> str: # get Deezer ID
        if self._dz_id == "":
            self._count_dz_id()
        return self._dz_id

    def get_ytm_link(self) -> str: # get YT Music link
        return "music.youtube.com/watch/" + self.get_ytm_id()

    def get_sp_link(self) -> str: # get Spotify link
        return "open.spotify.com/track/" + self.get_sp_id()

    def get_dz_link(self) -> str: # get Deezer link
        return "deezer.com/track/" + self.get_dz_id()

    def get_links(self) -> dict: # get all links
        return {
            "ytm": self.get_ytm_link(),
            "sp": self.get_sp_link(),
            "dz": self.get_dz_link()
        }