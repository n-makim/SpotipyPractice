import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# get username
username = sys.argv[1]

# https://open.spotify.com/user/naahsin-us?si=HWFFBjcSQ0mDAW3IuqKycw

# erase cache and prompt user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-(username)")
    token = util.prompt_for_user_token(username)

# create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
# print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print(">>> Hello " + displayName + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("0: Access full artist discography")
    print("1: Search top ten tracks for an artist")
    print("2: Audio analysis information")
    print("3: Exit program")
    print()
    choice = input("Your input: ")

    # search
    if choice == "0":
        print()
        searcher = input("Artist name? : ")
        print()
        searchResults = spotifyObject.search(searcher, 1, 0, "artist")
        # print(json.dumps(searchResults, sort_keys=True, indent=4))
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        # print(artist['genres'][1])
        print()
        # webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        trackURIs = []
        trackArt = []
        z = 0

        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("Album: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            # print(json.dumps(item, sort_keys=True, indent=4))

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        while True:
            selection = input("Enter song # to view album artwork/audio descriptors: ")
            if selection == "x":
                break
            # webbrowser.open(trackArt[int(selection)])
            audioData = spotifyObject.audio_features(trackURIs[int(selection)])
            print(json.dumps(audioData, sort_keys=True, indent=4))
            print()

            print("Song Number: " + str(selection))
            # print("Key: " + str(audioData["key"]))

            '''
            print("Time Signature: " + str(audioData['time_signature']))
            print("Track Duration (ms): " + str(audioData['duration_ms']))
            print("Acousticness: " + str(audioData['acousticness']))
            print("Danceability: " + str(audioData['danceability']))
            print("Energy: " + str(audioData['energy']))
            print("Instrumentalness: " + str(audioData['instrumentalness']))
            print("Loudness: " + str(audioData['loudness']))
            '''
            print()

    if choice == "3":
        break

    if choice == "1":
        print("Get artist top 10 songs: ")
        print()
        searcher = input("Artist name? : ")
        print()
        searchResults = spotifyObject.search(searcher, 1, 0, "artist")
        artist = searchResults['artists']['items'][0]
        artistID = artist['id']

        topTen = spotifyObject.artist_top_tracks(artistID)
        topTen = topTen['tracks']
        # print(json.dumps(topTen, sort_keys=True, indent=4))
        t = 1
        print()
        for track in topTen:
             print(str(t) + ": " + track['name'])
             t+=1
        print()

    if choice == "2":
        print()
        print("Duration_ms: duration in milliseconds")
        print("Key: estimated key of the track")
        print("Mode: modality (major = 1/minor = 0)")
        print("Acousticness: 0.0 to 1.0, 1.0 represents high confidence the track is acoustic")
        print("Danceability: 0.0 to 1.0, higher value represents higher potential for dancing (based on tempo, rhythm, beat strength, and overall stability")
        print("Energy: measure of intensity and activity (based on dynamic range, perceived loudness, timbre, and general entropy)")
        print("Instrumentalness: values above 5 intended to represent instrumental tracks (measure of vocals)")
        print("Liveness: detects presence of an audience, higher value represents higher likelihood of a live performance")
        print("Liudness: overall loudness in decibels")
        print("Speechiness: detects presence of spoken words, more speech-like will be closer to 1.0")
        print("Valence: 0.0 to 1.0, high valence is positive (happy, cheerful) while low valence is negative (sad, depressing, angry)")
        print("Tempo: estimated tempo in BPM")
        print()
# print(json.dumps(VARIABLE, sort_keys=True, indent=4))
