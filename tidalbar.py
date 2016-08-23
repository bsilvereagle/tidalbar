#!/usr/bin/env python3

import tidalapi
import mpv
import getpass
import time
from requests import HTTPError
from nonblockingkb import NonBlockingKB
from menu import Menu

#
#   KNOWN ISSUES
#

#   Pressing the arrow keys during a kb.input() cause immediate termination

#
#   EXTEND TIDALAPI
#

# All of the tidalapi classes are inherited from Model which has a .name
# Add a __str__ function so when things are converted to strings, they
# return their .name. Applied to Tracks/Albums/Artists/Playlists/etc
def patch__str__(self):
    return self.name
setattr(tidalapi.models.Model,'__str__',patch__str__)

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
#   
#   * nonblockingkb is not used since getpass is more secure

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

# Kick on the nonblocking keyboard now that getpass() has been used 
kb = NonBlockingKB()

#
#   MENUS
#
#   Menus are dictionaries where the key is the numeric selction
#   identifier for the menu, and the item is a tuple containing the
#   text to be displayed and the function to be executed for the
#   given selection and any data to be tagged with the item
#
#   sw_menu = {'1':('Han',han_shot_first,mf),'2':('Greedo',greedo_shot_first)}
#
#   would display the following menu when called with run_menu(sw_menu)
#
#   1) Han
#   2) Greedo
#
#   and execute either han_shot_first(mf) or greedo_shot_first()
#


#
#   MAIN MENU
#

def run_menu(menu):
    
    menu.print()
    selection = kb.input('Menu Selection: ')
    if not menu.get_item(selection):
        print('Invalid Selection',end='\r\n')
    else:
        menu.run_item(selection)

def play_playlist(playlist):
    # Accept either an id or a Playlist object
    if type(playlist) is tidalapi.Playlist:
        playlist_id = playlist.id
    else:
        # Assume we have an id
        playlist_id = playlist
    for track in session.get_playlist_tracks(playlist_id):
        player.loadfile('rtmp://'+session.get_media_url(track.id),'append-play')

#  Main Menu Functions
def tidal_whats_new():
    pass
def tidal_playlists():
    pass
def tidal_genres():
    pass
def user_playlists():
    playlist_menu = Menu()

    for counter, playlist in enumerate(session.get_user_playlists(session.user.id)):
        playlist_menu.add_item(str(counter),playlist.name,play_playlist,playlist)
    
    run_menu(playlist_menu)

def user_albums():
    pass
def user_tracks():
    pass
def user_artists():
    pass
def cancel_menu():
    pass

def clean_exit():
    kb.reset()
    exit()

main_menu = Menu({'1':('Tidal What\'s New', tidal_whats_new),
                  '2':('Tidal Playlists', tidal_playlists),
                  '3':('Tidal Genres', tidal_genres),
                  '4':('Playlists', user_playlists),
                  '5':('Albums', user_albums),
                  '6':('Tracks', user_tracks),
                  '7':('Artists', user_artists),
                  '8':('Cancel',cancel_menu),
                  '9':('Quit',clean_exit)})

def player_toggle_pause():
    if player.pause:
        player.pause = False
    else:
        player.pause = True

def player_next_track():
    pass

hotkey_menu = Menu({'p':('Pause', player_toggle_pause),
                    'n':('Next Track', player_next_track),
                    'm':('Main Menu', run_menu, main_menu),
                    'h':('Help', player_toggle_pause)})
                    


#
#   MAIN LOOP
#

try:
    # Run the main menu to start
    run_menu(main_menu)

    while True:
        # Check for hotkeys keyboard input
        keypress = kb.getch()
        if keypress != -1:
            if hotkey_menu.get_item(keypress):
                # Call the hotkey function if the keypress was valid
                hotkey_menu.run(keypress)
            
        # Move songs from the internal queue to the mpv queue
        # If no songs are left in the internal queue, start song radio
                


        # Get durations and what not if a song is playing
        if player.playback_time:
            total_m, total_s = [round(time) for time in divmod(player.duration, 60)]  
            current_m, current_s = [round(time) for time in divmod(player.playback_time, 60)]

            # Print play time
            print('%i:%i/%i:%i' % (current_m, current_s, total_m, total_s), end='\r')
        time.sleep(1)
except Exception as e:
    print(e)

finally:
    # Reset the terminal to a nice state
    clean_exit()
