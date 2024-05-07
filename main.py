import spotipy
import json
import webbrowser
import os
from spotipy.oauth2 import SpotifyOAuth

class SpotifyConverter:
    def __init__(self):
        # Set up credentials
        self.CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID") if os.environ.get("SPOTIFY_CLIENT_ID") else input("Enter Client ID: ")
        self.CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET") if os.environ.get("SPOTIFY_CLIENT_SECRET") else input("Enter Client Secret:")
        self.REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI") if os.environ.get("SPOTIFY_REDIRECT_URI") else input("Enter Redirect URI:")
        self.USERNAME = os.environ.get("SPOTIFY_USERNAME") if os.environ.get("SPOTIFY_USERNAME") else input("Enter Username:")

        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                                        client_secret=self.CLIENT_SECRET,
                                                        redirect_uri=self.REDIRECT_URI,
                                                        username=self.USERNAME,
                                                        scope='playlist-read-private'))
        print("SpotifyConverter initialized")
    
    def export_user_playlists(self, USERNAME):
        # The json file is to be formatted as: list of playlist objects > each playlist object > list of track objects
        playlists = self.sp.user_playlists(self.USERNAME)
        if playlists['items']:
            playlists_json = []
            first_playlist_id = playlists['items'][0]['id']
            for playlist in playlists['items']:
        
                playlist_id = playlist['id']
                playlist_name = playlist['name']
        
                playlist_json = {
                        "id":playlist_id,
                        "name":playlist_name,
                        "tracks": []
                }
                print(f"Listing songs in playlist '{playlist_name}':")
        
                # retrieve playlist tracks
                playlist_tracks = self.sp.playlist_tracks(playlist_id)
        
                for track in playlist_tracks['items']:
                    track_name = track['track']['name']
                    artist_name = track['track']['artists'][0]['name']
                    album_name = track['track']['album']['name']
                    track_json = {
                            "artist": artist_name,
                            "album_name": album_name,
                            "track_name": track_name
                    }
                    playlist_json['tracks'].append(track_json)
        
                
                    print(f"Artist: {artist_name}, Album: {album_name}, Title: {track_name}")
                playlists_json.append(playlist_json)
       
        else:
            print("No playlists found.")
        
        # Exporting the playlists object as a json file
        with open('./exported_playlists.json', 'w') as json_file:
            json.dump(playlists_json, json_file, indent=4)

    # Method that takes a json file path(in the format exported by export_user_playlists) and exports it as individual .m3u playlists
    def export_to_M3U_playlist(self,playlists_json_path):
        with open(playlists_json_path, 'r') as playlists_json:
            playlists = json.load(playlists_json)

        print("Number of playlists:", len(playlists))
        for playlist in playlists:
            playlist_name = playlist['name']
            with open(f"./{playlist_name}.m3u", 'w') as playlist_file:
                for track in playlist['tracks']:
                    file_path = f"{track['artist']}/{track['album_name']}/{track['track_name']}.mp3\n"
                    playlist_file.write(file_path)



SC = SpotifyConverter()
SC.export_to_M3U_playlist("./exported_playlists.json")


