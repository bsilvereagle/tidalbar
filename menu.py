#!/usr/bin/env python3

#
#   MENU
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
#   print_menu orders a menu dict by key then displays it
#   receive_menu waits on a user selection and then returns the matching tuple
#   run_menu calls print_menu & receive_menu until a valid menu option is chosen

from collections import OrderedDict

class Menu:
    
    def __init__(self, menu_map={}):
        self.menu_map = menu_map 

    def add_item(self, key, text, function, data=None):
        # Adds the item to the current menu
        # key - menu item for user to hit
        # text - text to display in menu
        # function - function to call on press
        # data - any extraneous data to associate with this menu item (Track, Artist, etc)
        
        self.menu_map[key] = (text, function, data)

    def get_item(self, key):
        
        return(self.menu_map[key])

    def get_item_text(self, key):

        return(self.menu_map[key][0])

    def get_item_function(self, key):

        return(self.menu_map[key][1])

    def get_item_data(self, key):
        try:
            return(self.menu_map[key][2])
        except:
            return None

    def print(self, end='\r\n'):
        # Sort the menu and store in an collections.OrderedDict
        # to ensure that items are displayed 1-9 or a-z
        ordered_menu = OrderedDict(sorted(self.menu_map.items()))
        
        print('\n', end=end)
        for item in ordered_menu:
            print('\t%s)\t%s' % (item, ordered_menu[item][0]), end=end)
        print('\n', end=end)
    
    def run_item(self, key):
        
        function = self.get_item_function(key)
        data = self.get_item_data(key)
        
        if data:
            function(data)
        else:
            function()
            
