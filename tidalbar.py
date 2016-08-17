import tidalapi
import mpv
import getpass
import time
from requests import HTTPError
from collections import OrderedDict


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
        if session.login(username, password):
            try:
                print('\N{EIGHTH NOTE} Successfully logged in! \N{EIGHTH NOTE}')
            except UnicodeEncodeError:
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
#   MENUS
#
#   Menus are dictionaries where the key is the numeric selction
#   identifier for the menu, and the item is a tuple containing the
#   text to be displayed and the function to be executed for the
#   given selection
#
#   sw_menu = {'1':('Han',han_shot_first),'2':('Greedo',greedo_shot_first)}
#
#   would display the following menu when called with run_menu(sw_menu)
#
#   1) Han
#   2) Greedo
#
#   and execute either han_shot_first() or greedo_shot_first()
#
#   

#
#   MENU FUNCTIONS
#

def print_menu(menu_map):
    # Sort the menu and store in an collections.OrderedDict
    # to ensure that items are displayed 1-9
    ordered_menu = OrderedDict(sorted(menu_map.items()))
    
    print('\n')
    for item in ordered_menu:
        print('\t%s)\t%s' % (item, ordered_menu[item][0]))
    print('\n')

def receive_menu(menu_map):
    selection = input('Selection: ')
    # Look up the selection in the dictionary
    return(menu_map.get(selection))

def run_menu(menu):
    # Present menu and get user selection
    result = None
    while result is None:
        print_menu(menu) 
        # dict.get returns None if the selected item is not present
        result = receive_menu(menu)
        if not result:
            print('Invalid input')
    # Act on the action ('Menu Text',function_name)
    print(result[1])

#
#   MAIN MENU
#

# Functions
def tidal_whats_new():
    pass
def tidal_playlists():
    pass
def tidal_genres():
    pass
def user_playlists():
    pass
def user_albums():
    pass
def user_tracks():
    pass
def user_artists():
    pass
def cancel_menu():
    pass
def clean_exit():
    exit()
# Menu map
main_menu = {'1':('Tidal What\'s New', tidal_whats_new),
             '2':('Tidal Playlists', tidal_playlists),
             '3':('Tidal Genres', tidal_genres),
             '4':('Playlists', user_playlists),
             '5':('Albums', user_albums),
             '6':('Tracks', user_tracks),
             '7':('Artists', user_artists),
             '8':('Cancel',cancel_menu),
             '9':('Quit',clean_exit)}



playlists = session.get_user_playlists(session.user.id)

# Add the tracks of the first user playlist to the mpv playlist
# ! Need to slowly fetch URLs, say 3 at a time. If a playlist is 100 songs
#   long the URL may have expired
for track in session.get_playlist_tracks(playlists[0].id):
    player.command('loadfile','rtmp://'+session.get_media_url(track.id),'append-play')

# Print the number of tracks in the playlist
print('%s tracks added to the mpv playlist' % len(player.playlist))

while(len(player.playlist) != 0):
    time.sleep(60)

