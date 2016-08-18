#!/usr/bin/env python3

#
#   KBHit
#
#   Inspired by Simon Levy's 'kbhit.py' and swyphcosmo's 'asyncconsoletest'
#   http://home.wlu.edu/~levys/software/kbhit.py
#   https://github.com/swyphcosmo/tidalbar/blob/master/asyncconsoletest.py

import os

# Check for Windows
if os.name == 'nt':
    import msvcrt
# Assume Posix (Linux, OS X, untested on BSD)
else:
    import curses

class KBHit:
    def __init__(self):
        # Initialize the keyboard object for nonblocking IO
        if os.name == 'nt':
            pass
        else: 
            # POSIX uses curses
            self.stdscr = curses.initscr()
            # Turn off key echo
            curses.noecho()
            # Don't require enter to be hit
            curses.cbreak()
            # Remove cursor from the screen
            curses.curs_set(False)
            # Get curses to monitor multibyte escape sequences
            self.stdscr.keypad(True)
            self.stdscr.nodelay(True)

    def getch(self):
        # If a key is down, return it
        if os.name == 'nt':
            if msvcrt.kbhit():
                # Key has been pressed
                return msvcrt.getwch() # Unicode variant of getch
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
    # Create a keyboard
    kb = KBHit()
    try:
        print('Press keys to see their keycode, \'q\' to quit')
        # Spin and spin printing the character hit until 'q' is hit
        while True:
            keypress = kb.getch()
            if keypress != -1:
                if keypress == ord('q'):
                    break
                else:
                    print(str(keypress)+ '\t' + chr(keypress))
        kb.reset()
    except:
        kb.reset()
        print('Clean Exit')
