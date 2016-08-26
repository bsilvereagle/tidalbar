#!/usr/bin/env python3

import tidalapi
import mpv
import getpass
import time
from requests import HTTPError
from nonblockingkb import NonBlockingKB
from menu import Menu
from doublelinkedlist import DoubleLinkedList

#
#   KNOWN ISSUES
#

#   Pressing downarrow immediatley causes .input to be read
#   Holding the spacebar pauses repeatedly. Pause toggles on/off every second for days
#   '10' as a list index shows up after the 1. 
#   session.get_genre_items always 404s

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

# Create list to keep track of playlist. Can't use mpv since the URLs given back from 
# Tidal have expiration dates. Usually, you can get 6 or so tracks in before the URLs
# start to go bad, but this object just fetches a URL as needed
internal_playlist = DoubleLinkedList()

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
        internal_playlist.append(track)
    refresh_player = True

# Given a list of tidalapi items, generate a menu where 'action' is the called function on the menu item
def dynamic_menu(itemlist, action=play_playlist):
    dynamic_menu = Menu()
    
    # If itemlist is not a true list, but instead an item (Playlist/Category), then
    #   get the list of items corresponding to that item
    if type(itemlist) is tidalapi.models.Category:
        # See if we have a Mood category
        try:
            itemlist = session.get_mood_playlists(itemlist.id)
        except:
            # Nope, it's a genre
            itemlist = session.get_genre_items(itemlist.id,'track')

    for counter, item in enumerate(itemlist):
        dynamic_menu.add_item(str(counter), item.name, action, item)

    run_menu(dynamic_menu)

#  Main Menu Functions
def search():
    pass

def tidal_whats_new():
    dynamic_menu(session.get_featured())

def tidal_moods():
    dynamic_menu(session.get_moods(), action=dynamic_menu)
    pass

def tidal_genres():
    dynamic_menu(session.get_genres(), action=dynamic_menu)

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

main_menu = Menu({'0':('Search', search),
                  '1':('Tidal What\'s New', tidal_whats_new),
                  '2':('Tidal Moods', tidal_moods),
                  # '3':('Tidal Genres', tidal_genres), # Genres 404
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
    # Get the next song and if none, start track radio for current song
    play_track(internal_playlist.next())

def player_prev_track():
    play_track(internal_playlist.prev())

def print_hotkeys():
    hotkey_menu.print()

def clear_playlist():
    internal_playlist = DoubleLinkedList()
    run_menu(main_menu)

def track_radio():
    current_track = internal_playlist.current_data()

    for track in session.get_track_radio(current_track.id):
        internal_playlist.insert(track)

hotkey_menu = Menu({' ':('Pause', player_toggle_pause),
                    'n':('Next Track', player_next_track),
                    'm':('Main Menu', run_menu, main_menu),
                    'h':('Help', print_hotkeys),
                    'k':('Show Playlist',print, internal_playlist),
                    'c':('Clear Playlist',clear_playlist),
                    'r':('Track Radio',track_radio)})

def play_track(track):
    if session.get_media_url(track.id):
        # See man page for mpv on 'replace' v 'append-play', etc
        player.loadfile('rtmp://'+session.get_media_url(track.id),'replace')
        print('', end='\r\n')
        while not player.duration:
            print('Loading stream...',end='\r')
        return track
    else:
        print('Error fetching URL',end='\r\n')
        return None

#
#   MAIN LOOP
#

try:
    current_track = None
    # Run the main menu to start
    run_menu(main_menu)

    while True:
        # Check for hotkeys keyboard input
        keypress = kb.getch()
        if keypress != -1:
            if keypress > 255:
                pass
            elif hotkey_menu.get_item(chr(keypress)):
                # Call the hotkey function if the keypress was valid
                hotkey_menu.run_item(chr(keypress))
                time.sleep(1)
            
        # If it's the first time through 
        if not current_track:
             current_track = play_track(internal_playlist.current_data())
        # If mpv is out of songs, add some
        elif not player.duration:
            current_track = internal_playlist.next()
            if not current_track:
                print('No More Tracks')
            else:
                current_track = play_track(current_track)

        # Get durations and what not if a song is playing
        song_duration = player.duration
        current_time = player.playback_time
        if song_duration and current_time:
            # Print play time
            total_m, total_s = [round(time) for time in divmod(song_duration, 60)]  
            current_m, current_s = [round(time) for time in divmod(current_time, 60)]
            print('\r{0:01d}:{1:02d}/{2:01d}:{3:02d} '.format(current_m, current_s, total_m, total_s), end='')

            # Print song name
            current_track = internal_playlist.current_data()
            print('{0} by {1}'.format(current_track.name, current_track.artist.name), end='\r')
        
        # Take a small pause
        time.sleep(0.01)

except Exception as e:
    print(e)
    import traceback
    traceback.print_exc()
    kb.input('Paused')

finally:
    # Reset the terminal to a nice state
    clean_exit()
    import traceback
    traceback.print_exc()
    exit()
