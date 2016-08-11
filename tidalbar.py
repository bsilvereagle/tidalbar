import tidalapi
import mpv
import getpass
import time

# Get the mpv player up and running
player = mpv.MPV()

# Establish the Tidal session using the XBMC tidalapi library
session = tidalapi.Session()

# Need to add a better way to escape the while loop
username = ''
while len(username) == 0:
    username = input('TIDAL username: ')

# 'Securely' get the password
password = getpass.getpass('TIDAL password: ')

session.login(username, password)

#
# ! Check for session failure
#

playlists = session.get_user_playlists(session.user.id)

# Add the tracks of the first user playlist to the mpv playlist
for track in session.get_playlist_tracks(playlists[0].id):
    player.command('loadfile','rtmp://'+session.get_media_url(track.id),'append-play')

# Print the number of tracks in the playlist
print('%s tracks added to the mpv playlist' % len(player.playlist))

while(len(player.playlist) != 0):
    time.sleep(60)

