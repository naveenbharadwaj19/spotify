import requests
import json
from shazam import shazam_
import csv

class Spotify_():
    def __init__(self):
        self.user_id = "ybhsn8f4y7q56c3uatusske9g"
        self.token = "BQAspkGaG_ct9GEIyracytDBbPdRl0954q6CgKgzHGJ3p1suMmeWuJBtOBxDf16J52DwI20wYHgbUUVBOwW5rECLJWUPmzkbdq2S3hV5I-c4rLSBdqhfwVRM-IMZKDG0MXE6uMNcEh_xBadG0y8Xn4Co-Qw7Z0o2hkBgznCDsHNeF58SmTJh9Hyc354ub20n0Ri_eK2l89BKU79hE6Kg_0O0816t"

    def create_playlist(self):
        req_body = json.dumps({
                "name": "Shazam tracked songs",
                "description": "Songs found in Shazam",
                "public": True,
            })

        req_body_dict = json.loads(req_body)
        if self.remove_duplication_playlist() != req_body_dict["name"]:
            query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
            req = requests.post(url=query, data=req_body, headers={"Content-Type": "application/json", "Authorization":f"Bearer {self.token}"})
            req_json = req.json()
            return req_json["id"]

        else:
            self.get_the_playlist_id()
            return "Playlist already exist"
    
    def remove_duplication_playlist(self):
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        req = requests.get(url,headers={"Accept": "application/json", "Authorization":f"Bearer {self.token}"})
        req_json = req.json()
        try:
            return req_json['items'][0]["name"]
        except Exception:
            return "Error No Id"

    def get_the_playlist_id(self):
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        req = requests.get(url,headers={"Accept": "application/json", "Authorization":f"Bearer {self.token}"})
        req_json = req.json()
        try:
            return req_json['items'][0]["id"]
        except Exception:
            return "Error No Id"

    def search_song(self):
        try:
            call_shazam = shazam_()
        except Exception:
            print("Error in fetching Shazam .Calling shazam again if failed run the script again")
            call_shazam
        with open("songartist.csv") as file_:
            reader = csv.reader(file_)
            song_names = []
            artist = []
            uri_lst = []
            for i in reader:
                song_names.append(i[1])
                artist.append(i[-1])
            song_names.pop(0)
            artist.pop(0)
            if len(song_names) == len(artist):
                for i in range(len(song_names)):
                    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
                        song_names[i],
                        artist[i]
                    )
                    response = requests.get(
                        query,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": "Bearer {}".format(self.token)
                        }
                    )
                    response_json = response.json()
                    songs = response_json["tracks"]["items"]
                    try:
                        uri = songs[0]["uri"]
                        uri_lst.append(uri)
                    except Exception:
                        continue
            # return song_uri_list
            return uri_lst


    def add_songs_to_playlist(self):
        self.create_playlist()
        try:
            songs_uri = self.search_song()
            songs_uri = list(dict.fromkeys(songs_uri))
            if not self.exitsting_songs_playlist():
                query = f"https://api.spotify.com/v1/playlists/{self.get_the_playlist_id()}/tracks?uris={songs_uri[0]}"
                requests.post(
                    query,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(self.token)
                    }
                )
                songs_uri.pop(0)
            if len(self.exitsting_songs_playlist()) >= 1:
                for i in range(len(songs_uri)):
                    if songs_uri[i] not in  self.exitsting_songs_playlist():
                        query = f"https://api.spotify.com/v1/playlists/{self.get_the_playlist_id()}/tracks?uris={songs_uri[i]}"
                        requests.post(
                            query,
                            headers={
                                "Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(self.token)
                            }
                        )
                return "Added songs to spotify"
                        
        except Exception:
            return "Error in adding songs to spotify"

    def exitsting_songs_playlist(self):
        query = f"https://api.spotify.com/v1/playlists/{self.get_the_playlist_id()}/tracks?fields=items(track(uri))"
        response = requests.get(query,headers= {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer {}".format(self.token)
                        })
        response_json = response.json()
        play_list_uri = []
        for i in response_json["items"]:
            play_list_uri.append(i["track"]["uri"])
        return play_list_uri

sp = Spotify_()
print(sp.add_songs_to_playlist())
