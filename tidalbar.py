import tidalapi
import mpv
import getpass
import time
from requests import HTTPError


#
#   CREATE OBJECTS
#

# Get the mpv player up and running
player = mpv.MPV()
# ! Check for errors

# Establish the Tidal session using the Kodi tidalapi library
session = tidalapi.Session()

#
#   LOGIN TO TIDAL
#
#   Use the tidalapi to login, give the user 3 attempts before aborting

login_attempts = 0
allowed_attempts = 3
while login_attempts < allowed_attempts:
    try:
        username = input('TIDAL username: ')
        password = getpass.getpass('TIDAL password: ')
        session.login(username,password)
        if session.check_login():
            print('Successfully logged in!')
            break
        else:
            print('Error establishing a session. Check your internet connection.')
    except HTTPError:
        print('Error logging in. Please try again.')
        login_attempts = login_attempts + 1
if login_attempts == allowed_attempts:
    print('Failed to login after three attempts. Aborting.')
    exit()

#
#   CAST THE CURSES
#

playlist = session.get_user_playlists(session.user.id)

# Add the tracks of the first user playlist to the mpv playlist
# ! Need to slowly fetch URLs, say 3 at a time. If a playlist is 100 songs
#   long the URL may have expired
for track in session.get_playlist_tracks(playlists[0].id):
    player.command('loadfile','rtmp://'+session.get_media_url(track.id),'append-play')

# Print the number of tracks in the playlist
print('%s tracks added to the mpv playlist' % len(player.playlist))

while(len(player.playlist) != 0):
    time.sleep(60)

