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
    "client_id": *CLIENT ID*,
    "client_secret": *CLIENT Secret*,
    "redirect_uri": *REDIRECTET URIS*,
    "scope": "user-library-read",
    "username": *USER NAME*
}
"""

sp_config_dict = json.loads(sp_config_file.read())
sp = Spotify(auth_manager=SpotifyOAuth(**sp_config_dict)
            )
# ------------------------------------------

dz = Client() # Deezer

class Song:

    __name: str = "" # name
    __ytm_id: str = "" # YT Music ID
    __sp_id: str = "" # Spotify ID
    __dz_id: str = "" # Deezer ID

    def __init__(self, name: str = "", ytm_link: str = "", sp_link: str = "", dz_link: str = "") -> None:
        try:
            if name != "":
                self.__name = name
            elif ytm_link != "":
                self.__name = ytm.get_song(videoId=ytm_link[ytm_link.find("=") + 1 : ytm_link.find("&")])["videoDetails"]["title"]
            elif sp_link != "":
                self.__name = sp.track(sp_link)["name"]
            elif dz_link != "":
                self.__name = dz.get_track(dz_link[dz_link.rfind("/") + 1 : ]).title
            else:
                raise Exception("We can't find your track. Please, give us some info(name or any link)")
        except:
            print("Something went wrong. Recheck data that you give")

    def __count_ytm_id(self) -> None: # count YT Music ID
        self.__ytm_id = str(ytm.search(query=self.__name, filter="songs")[0]["videoId"])

    def __count_sp_id(self) -> None: # count Spotify ID 
        self.__sp_id = str(sp.search(q=self.__name, type="track")["tracks"]["items"][0]["id"])

    def __count_dz_id(self) -> None: # count Deezer ID
        self.__dz_id = str(dz.search(query=self.__name)[0].id)

    def get_name(self) -> str: # get name
        return self.__name

    def get_ytm_id(self) -> str: # get YT Music ID
        if self.__ytm_id == "":
            self.__count_ytm_id()
        return self.__ytm_id

    def get_sp_id(self) -> str: # get Spotify ID
        if self.__sp_id == "":
            self.__count_sp_id()
        return self.__sp_id

    def get_dz_id(self) -> str: # get Deezer ID
        if self.__dz_id == "":
            self.__count_dz_id()
        return self.__dz_id

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