import spotipy
import spotipy.util as util
import pandas as pd

# The purpose of this function is to authorize the user into the Spotify API and format the data from their song list
# into a CSV format


def authorize():

    # Authorization into Spotify API account, able to access Spotipy functions as well

    username = input("Enter in your spotify username: ")
    client_id = input("Enter in your client ID (found in Spotify API developer website): ")
    client_secret = input("Enter in your client secret key: ")
    liked_playlist_name = input("Enter the playlist uri for your liked playlist, e.g. "
                              "'spotify:playlist:24lzIIsd847YMTU1QOP5Hm'")
    disliked_playlist_name = input("Enter the playlist uri for your disliked playlist, "
                                 "e.g. 'spotify:playlist:24lzIIsd847YMTU1QOP5Hm'")

    scope = 'user-top-read'

    token = util.prompt_for_user_token(username, scope, client_id, client_secret,
                                       redirect_uri='https://www.google.com/')

    # Instantiating the Spotify API "object" by which we can call relevant methods

    sp = spotipy.Spotify(auth=token)

    # Obtaining the relevant fields from the API data we pulled

    list_song_ids = []
    liked_song_ids = []
    all_track_names = []
    length_liked_playlist = sp.user_playlist(username, liked_playlist_name)['tracks']['total']
    length_disliked_playlist = sp.user_playlist(username, disliked_playlist_name)['tracks']['total']
    offset = 0
    offset2 = 0

    # Configuring the list of song IDs as well as the list of all the track names

    for i in range(length_liked_playlist // 100 + 1):
        liked_playlist_tracks = sp.user_playlist_tracks(username, playlist_id=liked_playlist_name, offset=offset)
        for playListDef in liked_playlist_tracks['items']:
            liked_song_ids.append(playListDef['track']['id'])
            list_song_ids.append(playListDef['track']['id'])
            all_track_names.append(playListDef['track']['name'])
        offset += 100

    for i in range(length_disliked_playlist // 100 + 1):
        disliked_playlist_tracks = sp.user_playlist_tracks(username, playlist_id=disliked_playlist_name, offset=offset2)
        for playListDef in disliked_playlist_tracks['items']:
            list_song_ids.append(playListDef['track']['id'])
            all_track_names.append(playListDef['track']['name'])
        offset2 += 100

    # Audio Analysis for all the requisite 200 songs

    liked_flag = 0
    i = 0

    total_list_metrics = [['name', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                         'liveness', 'valence', 'tempo', 'like/dislike']]
    liked_list_metrics = [['name', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                         'liveness', 'valence', 'tempo']]
    disliked_list_metrics = [['name', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                            'liveness', 'valence', 'tempo']]

    for tid in list_song_ids:
        track_name = all_track_names[i]
        analysis = sp.audio_features(tid)
        if tid in liked_song_ids:
            liked_list_metrics.append([track_name,
                                     float(analysis[0]['danceability']),
                                     float(analysis[0]['energy']),
                                     float(analysis[0]['key']),
                                     float(analysis[0]['loudness']),
                                     float(analysis[0]['mode']),
                                     float(analysis[0]['speechiness']),
                                     float(analysis[0]['acousticness']),
                                     float(analysis[0]['liveness']),
                                     float(analysis[0]['valence']),
                                     float(analysis[0]['tempo'])])
            liked_flag = 1
        elif tid not in liked_song_ids:
            disliked_list_metrics.append([track_name,
                                     float(analysis[0]['danceability']),
                                     float(analysis[0]['energy']),
                                     float(analysis[0]['key']),
                                     float(analysis[0]['loudness']),
                                     float(analysis[0]['mode']),
                                     float(analysis[0]['speechiness']),
                                     float(analysis[0]['acousticness']),
                                     float(analysis[0]['liveness']),
                                     float(analysis[0]['valence']),
                                     float(analysis[0]['tempo'])])

        total_list_metrics.append([track_name,
                            float(analysis[0]['danceability']),
                            float(analysis[0]['energy']),
                            float(analysis[0]['key']),
                             float(analysis[0]['loudness']),
                            float(analysis[0]['mode']),
                            float(analysis[0]['speechiness']),
                             float(analysis[0]['acousticness']),
                            float(analysis[0]['liveness']),
                            float(analysis[0]['valence']),
                             float(analysis[0]['tempo']),
                            liked_flag])
        i += 1
        liked_flag = 0

    # Converts data into a CSV format, with diff CSVs for Liked and Disliked

    df = pd.DataFrame(total_list_metrics)
    df.to_csv('classification_song_metrics.csv', index=False)
    df_liked = pd.DataFrame(liked_list_metrics)
    df_liked.to_csv('liked_song_metrics.csv', index=False)
    df_disliked = pd.DataFrame(disliked_list_metrics)
    df_disliked.to_csv('disliked_song_metrics.csv', index=False)

