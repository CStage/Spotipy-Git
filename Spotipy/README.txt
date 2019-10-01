0. Introduction
1. Advantages of using SpotipyShell
	1.1. Limits have been overridden
	1.2. getEntireUserLibrary
	1.3. CompareUserLibraries
2. Final notes

______________________________
0. Introduction
________________________________

Spotipy successful.py was created to try and get familiar with Spotify's API.

The file uses a Spotify-class called SpotipyShell, which is a primitive implementation of the Class described in spotipy's own documentation.
For successful runs it requires:

1. Client ID
2. Secret ID
3. Redirect URI
4. Spotipy library (Plamere) NOTE: Should be installed through GitHub as the pip-version is outdated.
5. User ID

This file on GitHub will not include any ID's or URI's as they are personal and should not be compromised, but inserting your own should allow the program 
to run.

________________________________________________________________________________________________
1. Advantages of using SpotipyShell rather than the built-in Class from Spotipy:
________________________________________________________________________________________________

________________________________________________________________________________________________
1.1 Limits have been overridden
________________________________________________________________________________________________
Most Class-functons that make calls to playlists or tracks have limits on how many items you can get per call. By implementing new functions these limits
have effectively been overrridden through recursion. For example: user_playlist_tracks has a limit of 100, but SpotipyShell.getUserPlaylistTracks has no
limit.

The exception is getCurrentUsertopArtists which inherits its limit from the built-in Class. Reason being that my experiments didn't require the use of Top Artists
however, overriding the limit shouldn't be a problem.

________________________________________________________________________________________________
1.2 getEntireUserLibrary
________________________________________________________________________________________________
SpotipyShell has a function caleed getEntireUserLibrary which finds all playlists of a user and returns a dictionary of Track Names and Track ID's. The
function by default only includes Public playlists, but has implementation for private playlists as well. Note that accessing private playlists requires an
access token - in other words - you can only get private playlists if you have the username + password of the account in question.

________________________________________________________________________________________________
1.3 CompareUserLibraries
________________________________________________________________________________________________
Compares two users' entire public libraries and returns a Spotify-playlist with the tracks present in both libraries. The function allows you to see where 
two users' tastes in music overlap. The function CAN include your own private lists, but ONLY your own and will require an access token. Note also that if
you are planning on including the private lists, then the program can take quite a while to run and since the access token expires after ~1 hour the program
is likely to crash if you have many lists with a lot of songs. For most users this should not be a problem though.

Spotipy is quite slow at extracting tracks from a playlist (I estimate it to be about 2 seconds per song), so the program gives an update on how many lists
it has gone through per library, and how many lists there are in total.

________________________________________________________________________________________________
2. Final notes about the file
________________________________________________________________________________________________
The implementation is primitive and not particularly "pretty", but it gets the job done. I made it only to see if I could figure out how to use an API to 
create a program in Python. Safe to say - I was successful in my endeavors :)

I might go back one day and rewrite some of the code to make it prettier and more intuitive, but for now I'll leave it be.


//Christian