#!/usr/bin/env python3

#
#   NonBlockingKB
#
#   Inspired by Simon Levy's 'kbhit.py' and swyphcosmo's 'asyncconsoletest'
#   http://home.wlu.edu/~levys/software/kbhit.py
#   https://github.com/swyphcosmo/tidalbar/blob/master/asyncconsoletest.py
#
#   Standard raw_input/input is blocking in Python. The user must enter text
#   before the program can output information. For a media player, this is
#   undesirable. Hotkeys for pause/play/next/previous/etc should be listened
#   for continously while the screen is updating with current playtime, etc
#   This class uses curses on Posix systems and msvcrt on Windows in order
#   to detect keypresses in a nonblocking fashion. getch() returns the 
#   last pressed key on both systems. For hotkeys the user does not need to see
#   the key that has been pressed. However, it is also desireable when
#   interacting with a menu for the user to see their input. menuinput()
#   accomplishes this by turning back on curses echo and requires a user
#   to hit enter prior to the input being read. 
#
#   A big chunk of this codebase is to work around curses, msvcrt seems to 
#   play pretty nicely
#
#   Small demo program when nonblockingkb is run as main to demonstrate
#   how to use .getch and .input

import os

# Check for Windows
if os.name == 'nt':
    import msvcrt
# Assume Posix (Linux, OS X, untested on BSD)
else:
    import curses

class NonBlockingKB:
    def __init__(self):
        # Initialize the keyboard object for nonblocking IO
        if os.name == 'nt':
            pass
        else: 
            # POSIX uses curses
            self.stdscr = curses.initscr()
            curses.noecho()         # Turn off key echo
            curses.cbreak()         # Don't require enter to be hit
            curses.curs_set(False)  # Remove cursor from the screen
            # Get curses to monitor multibyte escape sequences
            self.stdscr.keypad(True)
            self.stdscr.nodelay(True) # Make curses async

        # A screen refresh may occur on the first self.getch() call
        # This call makes sure that refresh occurs before any application
        # code is ran
        self.getch()

    def input(self, prompt):
        # Returns prompt to a line entry state where input is echoed, etc
        if os.name == 'nt':
            pass
        else:
            # Turns on echo, requires enter, and makes curses blocking
            curses.echo()
            curses.nocbreak()
            curses.curs_set(True)
            self.stdscr.nodelay(False)
        
        # Display the prompt
        print(prompt, end='', flush=True)
        # Get input
        if os.name == 'nt':
            print('Functionality not implemented')
        else:
            result = self.stdscr.getstr().decode(encoding='utf-8')
            # Reset terminal to non line entry state
            curses.noecho()
            curses.cbreak()
            curses.curs_set(False)
            self.stdscr.nodelay(True)
            curses.flushinp()
            self.getch()
        
        return result


    def getch(self):
        # If a key is down, return it
        if os.name == 'nt':
            if msvcrt.kbhit():
                # Key has been pressed
                return msvcrt.getch()
            else:
                return -1
        else:
            # curses.getch() automatically returns -1 if no key is available
            return self.stdscr.getch()
        
    def reset(self):
        # Resets terminal to 'normal' operation
        if os.name == 'nt':
            pass
        else:
            # Reset curses
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.curs_set(True)
            self.stdscr.nodelay(False)
            curses.endwin()

if __name__ == '__main__':
    import time
    # Create a keyboard
    kb = NonBlockingKB()
    try:
        print('Press keys to see their keycode, \'q\' to quit, \'p\' to enter a string.', end='\r\n')
        # Spin and spin printing the character hit until 'q' is hit
        while True:
            keypress = kb.getch()
            if keypress != -1:
                if keypress == ord('q'):
                    break
                elif keypress == ord('p'):
                    user_input = kb.input('Enter a string: ')
                    print('Entered string: ' + user_input, end='\r\n')
                else:
                    print(str(keypress)+ '\t' + chr(keypress), end='\r\n')
            time.sleep(0.01)
    except:
        pass # Any printing here is lost when curses is reset
    finally:
        kb.reset()
