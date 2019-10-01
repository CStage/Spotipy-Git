# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:21:00 2019

@author: cstag
"""

import sys
import copy
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials


sys.setrecursionlimit(2000)



redirect_url=
client=
secret=
username=

Unique_client_credentials_manager = oauth2.SpotifyClientCredentials(
        client_id=client,
        client_secret=secret
)
token = Unique_client_credentials_manager.get_access_token()
spotify = spotipy.Spotify(auth=token)


class SpotipyShell(object):
    def __init__(self, auth=None, requests_session=True, client_credentials_manager=None, proxies=None, requests_timeout=None):
        self.auth=auth
        self.client_credentials_manager=client_credentials_manager
        self.proxies=proxies
        self.requests_timeout=requests_timeout
        #sp is the token that allows us to do authorized requests
        sp = spotipy.Spotify(auth=self.auth)
        self.sp=sp
        playlistList={}
        self.playlistList=playlistList
        self.TrackDict={}


    def getAlbum(self, albumList):
        """Returns list of album names given album URI, URL or ID """
        albumNames=[]
        for album_id in albumList:
            if self.sp.album(album_id)["name"] in albumNames:
                print("Album already in list")
            else:
                albumNames.append(self.sp.album(album_id)["name"])
        return albumNames

    def getAlbumTracks(self, album_id, limit=100, offset=0):
        """Returns tracks of an album given album URI, URL or ID"""
        tracklist=[]
        for i in range(self.sp.album(album_id)["total_tracks"]):
            if i>=limit:
                break
            tracklist.append(self.sp.album(album_id)["tracks"]["items"][i+offset]["name"])
        return tracklist

    def getArtists(self, artistList):
        """Returns artist names given list of artist URL, URI or ID"""
        artistNames=[]
        for artist_id in artistList:
            if self.sp.artist(artist_id)["name"] in artistNames:
                print(self.sp.artist(artist_id)["name"], "is already in list")
            else:
                artistNames.append(self.sp.artist(artist_id)["name"])
        return artistNames

    def getAlbumsFromArtist(self, artist_id, album_type=None, country=None, limit=50, offset=0):
        """Returns albums of given type from given artist. NOTE: spotipy max(limit)  is 50"""
        albumList=[]
        for i in range(len(self.sp.artist_albums(artist_id, album_type, None, limit, offset)["items"])):
            if self.sp.artist_albums(artist_id, album_type, None, limit, offset)["items"][i]["name"] in albumList:
                pass
            else:
                albumList.append(self.sp.artist_albums(artist_id, album_type, None, limit, offset)["items"][i]["name"])
        return albumList

    def getRelatedArtistsNames(self, artist_id):
        """Returns a list of related artists to an artist, given artist URL, URI or ID"""
        relatedArtistList=[]
        for i in range(len(self.sp.artist_related_artists(artist_id)["artists"])):
            relatedArtistList.append(self.sp.artist_related_artists(artist_id)["artists"][i]["name"])
        return relatedArtistList

    def getArtistTopTracks(self, artist_id, country="US"):
        """Returns a list of top tracks given an artist URL, URI or ID and a Country-code"""
        artistTopTracksList=[]
        for i in range(len(self.sp.artist_top_tracks(artist_id, country)["tracks"])):
            artistTopTracksList.append(self.sp.artist_top_tracks(artist_id, country)["tracks"][i]["name"])
        return artistTopTracksList

    def getAudioAnalysis(self, track_id):
        """Returns analysis of given track along Spotify's own parameters"""
        return self.sp.audio_analysis(track_id)

    def getAudioFeatures(self, tracks):
        """Returns a bunch of parameters for a track given track URL, URI or ID"""
        return self.sp.audio_features(tracks)

    def getNewCategories(self, country=None, locale=None, limit=50, offset=0):
        """Returns a list of newly released categories for a given country or in the world"""
        newCategories=[]
        for i in range(len(self.sp.categories(country, locale, limit, offset)["categories"]["items"])):
            newCategories.append(self.sp.categories(country, locale, limit, offset)["categories"]["items"][i]["name"])
        return newCategories

    def getNewReleases(self, category_id=None, country=None, limit=50, offset=0):
        """Returns a list of newly released albums given a certain category and country"""
        newReleaseslist=[]
        for i in range(len(self.sp.category_playlists(category_id, country, limit, offset)["playlists"]["items"])):
            newReleaseslist.append(self.sp.category_playlists(category_id, country, limit, offset)["playlists"]["items"][i]["name"])
        return newReleaseslist


    def getCurrentUser(self):
        """Returns user information. NOTE requires explicit access from the user"""
        scope="user-read-private, user-top-read, user-read-recently-played, user-library-read, user-read-email, user-follow-read, user-read-playback-state, user-read-currently-playing"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        userInformation={}
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            userInformation["Country"]=self.sp.current_user()["country"]
            userInformation["Name"]=self.sp.current_user()["display_name"]
            userInformation["Email"]=self.sp.current_user()["email"]
            userInformation["Followers"]=self.sp.current_user()["followers"]["total"]

        print(userInformation)
        return userInformation

    def getCurrentUserPlayback(self, market=None):
        """Returns the current user's playback"""
        scope="user-read-currently-playing, user-read-playback-state, user-modify-playback-state"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            print("Title", self.sp.current_playback(market)["item"]["name"])
            if len(self.sp.current_playback(market)["item"]["artists"])>1:
                featured_artists=""
                for i in range(len(self.sp.current_playback(market)["item"]["artists"])):
                    if i+1==len(self.sp.current_playback(market)["item"]["artists"]):
                        featured_artists+=self.sp.current_playback(market)["item"]["artists"][i]["name"]+"."
                    else:
                        featured_artists+=self.sp.current_playback(market)["item"]["artists"][i]["name"]+", "
                print("Featuring: ", featured_artists)
            else:
                print("Artist: ", self.sp.current_playback(market)["item"]["artists"][0]["name"])
            print("Album: ", self.sp.current_playback(market)["item"]["album"]["name"])
        return self.sp.current_playback(market)

    def getCurrentUserFollowedArtists(self, type="artist", limit=50, after=None):
        """Returns user's followed artists"""
        followedArtistsList=[]
        scope="user-follow-modify, user-follow-read, user-top-read"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
        for i in range(len(self.sp.current_user_followed_artists()["artists"]["items"])):
            followedArtistsList.append(self.sp.current_user_followed_artists()["artists"]["items"][i]["name"])
        return followedArtistsList

    def getCurrentUserPlaylists(self, limit=1, offset=0):
        """Returns playlists of current user (Public and Private)"""
        scope="playlist-read-private, playlist-modify-private"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            for i in range(len(self.sp.current_user_playlists(limit, offset)["items"])):
                self.playlistList[self.sp.current_user_playlists(limit, offset)["items"][i]["name"]]=self.sp.current_user_playlists(limit, offset)["items"][i]["id"]
        if len(self.sp.current_user_playlists(limit, offset)["items"])>0:
            return self.getCurrentUserPlaylists(limit, offset+limit)
        print("Final playlistList", self.playlistList)
        return self.playlistList

    def getCurrentUserRecentlyPlayed(self, limit=50):
        """Returns current user's recently played songs"""
        scope="user-read-recently-played"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        currentUserRecentlyPlayedList=[]
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            for i in range(limit):
                if self.sp.current_user_recently_played(limit)["items"][i]["track"]["name"] not in currentUserRecentlyPlayedList:
                    currentUserRecentlyPlayedList.append(self.sp.current_user_recently_played(limit)["items"][i]["track"]["name"])
        return currentUserRecentlyPlayedList

    def getCurrentUserTopArtists(self, limit=50, offset=0, time_range="medium_term"):
        """Returns current user's recently played artists"""
        scope="user-top-read"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        TopArtistsList=[]
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            for i in range(len(self.sp.current_user_top_artists(limit, offset, time_range)["items"])):
                print(self.sp.current_user_top_artists(limit, offset, time_range)["items"][i]["name"])
                TopArtistsList.append(self.sp.current_user_top_artists(limit, offset, time_range)["items"][i]["name"])
        return TopArtistsList

    def getCurrentUserTopTracks(self, limit=50, offset=0, time_range="medium_term"):
        """Returns current user's top tracks"""
        scope="user-top-read"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        TopTracksDict={}
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            for i in range(len(self.sp.current_user_top_tracks(limit, offset, time_range)["items"])):
                TopTracksDict["No." + str(i+1)]={str(self.sp.current_user_top_tracks(limit, offset, time_range)["items"][i]["name"]) : str(self.sp.current_user_top_tracks(limit, offset, time_range)["items"][i]["artists"][0]["name"])}
        return TopTracksDict



    def getUser(self, user_id):
        print(self.sp.user(user_id))
        return self.sp.user(user_id)

    def getUserPlaylists(self, user_id, limit=50, offset=0):
        """Returns all playlists of a user"""
        userShell={}
        userPlaylistsDict={}
        for i in range(len(self.sp.user_playlists(user_id, limit, offset)["items"])):
            userPlaylistsDict[self.sp.user_playlists(user_id, limit, offset)["items"][i]["name"]]=self.sp.user_playlists(user_id, limit, offset)["items"][i]["id"]
        userShell[user_id]=userPlaylistsDict
        return userShell

    def getUserPlaylistTracks(self, user_id, playlist_id, fields=None, limit=1, offset=0, market=None, Private=False):
        """Returns title and artists of all tracks in a given playlist by a given user"""
        if Private==True:
            scope="playlist-read-private, playlist-modify-private, playlist-read-collaborative"
            token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
            self.sp=spotipy.Spotify(auth=token1)
        for i in range(len(self.sp.user_playlist_tracks(user_id, playlist_id, fields, limit, offset, market)["items"])):
            title=self.sp.user_playlist_tracks(user_id, playlist_id, fields, limit, offset, market)["items"][i]["track"]["name"]
            artistKey=""
            idKey=self.sp.user_playlist_tracks(user_id, playlist_id, fields, limit, offset, market)["items"][i]["track"]["id"]
            self.TrackDict[idKey]=title
        if len(self.sp.user_playlist_tracks(user_id, playlist_id, fields, limit, offset, market)["items"])>0:
            return self.getUserPlaylistTracks(user_id, playlist_id, fields, limit, offset+limit, market)
        else:
            relevantDict=copy.deepcopy(self.TrackDict)
            self.TrackDict={}
            return relevantDict

    def createAPlaylistForCurrentUser(self, user_id, name, Public=True, description=""):
        """Creates a playlist for the current user"""
        NewPlaylistDict={}
        scope="playlist-modify-public, user-library-modify"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            NewPlaylist=self.sp.user_playlist_create(user_id, name, Public, description)
            NewPlaylistDict["name"]=NewPlaylist["name"]
            NewPlaylistDict["id"]=NewPlaylist["id"]
            return NewPlaylistDict

    def AddTracksToUserPlaylist(self, user_id, playlist_id, tracks, position=None):
        """Adds tracks to a user playlist given user_id, playlist_id, and list of tracks"""
        scope="playlist-modify-public, playlist-read-private, playlist-modify-private, playlist-read-collaborative"
        token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
        if token1:
            self.sp=spotipy.Spotify(auth=token1)
            self.sp.user_playlist_add_tracks(user_id, playlist_id, tracks, position)

    def getEntireUserLibrary(self, user_id, Private=False):
        """Returns a dictionary of track names to track IDs for all playlists of a given user"""
        library={}
        keepTrack=0
        if Private==True:
            scope="playlist-read-private, playlist-modify-private, playlist-read-collaborative"
            token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
            if token1:
                self.sp=spotipy.Spotify(auth=token1)
                UserPlaylists=self.getCurrentUserPlaylists()
                for name in UserPlaylists:
                    token1=util.prompt_for_user_token(username, scope, client, secret, redirect_url)
                    self.sp=spotipy.Spotify(auth=token1)
                    keepTrack+=1
                    print("Total no. of playlists", len(UserPlaylists), "current no.", keepTrack)
                    individualTrackDict=self.getUserPlaylistTracks(user_id, UserPlaylists[name], fields=None, limit=1, offset=0, market=None, Private=True)
                    for i in individualTrackDict:
                        if individualTrackDict[i] in library:
                            pass
                        else:
                            library[i]=individualTrackDict[i]


        else:
            print("Private is not true")
            UserPlaylists=self.getUserPlaylists(user_id)

            for name in UserPlaylists[user_id]:
                keepTrack+=1
                print("Total no. of playlists", len(UserPlaylists[user_id]), "current no.", keepTrack)
                individualTrackDict=self.getUserPlaylistTracks(user_id, UserPlaylists[user_id][name])

                for i in individualTrackDict:
                    if individualTrackDict[i] in library:
                        pass
                    else:
                        library[i]=individualTrackDict[i]
        return library

    def CompareUserLibraries(self, Private=None, user_id=username):
        """Creates a playlist of tracks present in BOTH libraries of two users."""
        Commonground={}
        GroundForPlaylist=[]
        User1OK=False
        User2OK=False
        spectrumIsHandled=False
        Spectrum=input("Include own personal playlists? Y/N: ")

        while spectrumIsHandled==False:
            if Spectrum == "Y" or Spectrum == "y":
                print("Private playlists will be included")
                Private=True
                spectrumIsHandled=True
            elif Spectrum == "N" or Spectrum == "n":
                print("Private playlists will be excluded")
                Private=False
                spectrumIsHandled=True
            else:
                print("Invalid input")

        while User1OK==False:
            User1=input("Enter your user-ID: ")
#            if not len(User1)==10:
#                print("Invalid user-ID")
#            else:
            User1OK=True

        while User2OK==False:
            User2=input("Enter a second user-ID: ")
#            if not len(User2)==10:
#                print("Invalid user-ID")
#            else:
            User2OK=True
        print("Comparing", User1, "to", User2, ". This will take a little while")

        print("Fetching second library")
        Secondlibrary=self.getEntireUserLibrary(User2)
        print("Fetching first library")
        if Private==True:
            Firstlibrary=self.getEntireUserLibrary(User1, Private)
        else:
            Firstlibrary=self.getEntireUserLibrary(User1)


#        print("First", Firstlibrary)
#        print("Length", len(Firstlibrary))
#        print("")
#        print("Second", Secondlibrary)
#        print("Length", len(Secondlibrary))

        for i in Firstlibrary:
            if i in Secondlibrary:
                GroundForPlaylist.append(i)
            else:
                pass

        while None in GroundForPlaylist:
            for k in GroundForPlaylist:
                if k==None:
                    GroundForPlaylist.remove(k)


        print("Ground", GroundForPlaylist)
        print("length", len(GroundForPlaylist))

        Playlist=self.createAPlaylistForCurrentUser(username, "Common Ground", True, "Between: " + str(User1) + " and " +str(User2))
        while len(GroundForPlaylist)>100:
            self.AddTracksToUserPlaylist(username, Playlist["id"], GroundForPlaylist[:100])
            for j in range(0,99):
                GroundForPlaylist.remove(GroundForPlaylist[0])
        self.AddTracksToUserPlaylist(username, Playlist["id"], GroundForPlaylist)




testClass=SpotipyShell(token, True, Unique_client_credentials_manager, None, None)
