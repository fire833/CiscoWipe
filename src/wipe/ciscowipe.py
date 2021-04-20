#!/usr/bin/env python3
###############################################
#
# Classes for wiping Cisco and other products with the yserial API, among other features.
# Notes: Look to replace with API calls in the future, since web interaction is slow and unstable. 
# Copyright 2021 Kendall Tauser
#
###############################################

#import pyautogui
# import keyboard
import os
import sys
import time
import argparse
import serial
import selenium
import nltk
import pynput
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pynput.keyboard import Key, Controller, Listener, KeyCode
from pynput import keyboard

# Random Vars

rm = 'del flash:'
rm1 = 'del '
enter = '\n'
config = 'conf t'
confreg = 'confreg'
reset = 'reset'
register1 = '0x2142'
register2 = '0x2102'
space = ' '
sleep_time = 0.05
dirflash = 'dir flash:\n'
router_commands_list = os.path.join(sys.path[0], 'router_commands.txt')
asa_commands_list = os.path.join(sys.path[0], 'security_appl_commands.txt')
w = 0
x = 0
y = 0
z = 0
breakloop = False
keyrelease = True

# Importing the command lists and saving them as collections in memory

with open(router_commands_list, 'r') as router:
    cm3 = router.read()
    rlist = cm3.splitlines()
    rlen = str(len(rlist))

with open(asa_commands_list, 'r') as asa:
    cm4 = asa.read()
    alist = cm4.splitlines()
    alen = str(len(alist))

# Basic purge all files based on command list functions

class main_del():

    import time
    import serial
    
    def write(self, data):
        keyboard = Controller()
        keyboard.type(data)

class serialwords():

    def __init__(self):
        pass

    def options(self):
        pass

class ser_instance():
    
    from tech.tech import Tech_stuff
    import time

    def __init__(self, port, baud):
        self.ser = serial.Serial(port=port, baudrate=baud)
        
        self.port = port
        self.is_reading_done = False
        self.is_wap = False
        self.is_switch = False
        self.is_router = False
        self.is_asa = False
        self.is_in_rommon = False
        self.is_in_priv_exec = False
        self.alive = None
        self.print = None

        self.ser.open()

    def start(self):
        self.alive = True
        while True:
            self.reader()
    
    def reader(self):
        # In theory, read 1\ lines, place the string into a list, and update _is reading done to trigger the word search function.
        if self.is_reading_done == False:
            self.num = 0 
            self.lines = []
            while self.num < 1:
                self.ser.read_until().decode('utf-8').append(self.lines)
                if self.print == True:
                    print(self.port + self.lines)
                self.num = self.num + 1
            self.is_reading_done = True
            self.search_keywords()
    
    def search_keywords(self):
        # With each line, this method looks for each of these arguments that could be in the string (common Cisco CLI indicators) and then determines what should be done, 
        # whether it be just inform the class object what type of device is being worked on, what stage in the resetting process it is in, 
        # or to tell the object class what to do next based off what has been parsed.
        if self.is_reading_done == True:
            words_and_phrases = ['#', ":", 
#2
        "Would you like to enter the initial configuration dialog? [yes/no]", 
        "Press RETURN to get started!", 
        "Router#", 
        "ap:", 
        "examining image...", 
#7        
        "Restricted Rights Legend", 
        "Username:", 
        "User Access Verification", 
        "Password:", 
        "capwap process not yet started.Please execute enable command again", 
#12        
        "% Invalid input detected at '^' marker.", 
        "con0 is now available",
        "Use BREAK or ESC to interrupt boot.", 
        "rommon #>", 
        "Pre-configure Firewall now through interactive prompts [yes]?", 
#17
        "Licensed features for this platform:", 
        "rommon",
        
        ]
            if(words_and_phrases[2] in self.lines):
                
                self.no_config_dialogue()
                self.lines = []
                self.is_reading_done = False
            
            elif(words_and_phrases[8] or words_and_phrases[10] in self.lines):
                
                self.username_and_pass()
                self.lines = []
                self.is_reading_done = False
            
            elif(words_and_phrases[3] or words_and_phrases[13] in self.lines):
                
                self.ser.write("\n".encode('utf-8'))
                self.lines = []
                self.is_reading_done = False
            
            elif(words_and_phrases[4] in self.lines):
                
                self.is_router = True
                self.is_reading_done = False
            
            elif(words_and_phrases[5] in self.lines):

                self.is_wap = True
                self.is_reading_done = False
            
            elif(words_and_phrases[14] in self.lines):

                self.is_asa = True
                self.is_reading_done = False

            elif(words_and_phrases[15] or words_and_phrases[18] in self.lines):

                self.is_in_rommon = True
                self.is_reading_done = False
            
            elif(words_and_phrases[16] in self.lines):

                self.is_asa = True
                self.is_reading_done = False

            elif(words_and_phrases[17] in self.lines):
                
                self.info = True
                self.is_reading_done = False

            elif(words_and_phrases[11] in self.lines):
                self.enable()
            
            else:
                
                self.lines = []
                self.is_reading_done = False
            
    def no_config_dialogue(self):
        no = 'no'
        self.write(no)
        self.write('\n')

    def username_and_pass(self):
        cisco = 'Cisco'
        self.write(cisco)
        self.write('\n')

    def enable(self):
        self.write('\n')
        self.write('en' + '\n')

    def write(self, data):
        self.ser.write(data.encode('utf-8'))
    
        # ROMMON RESET Functions

    def router_rommon_exec(self):
        self.write(enter)
        self.write(confreg + register1 + enter)
        time.sleep(3.5)
        self.write(reset + enter)

    def asa_rommon_exec(self):
        self.write('escape')
        self.write(confreg + space + register1)
        time.sleep(10)
        self.write('boot' + enter)

    def router_file_del(self):
    
        # Router Deletion Logic
        self.write(enter)
        for z in rlist:
            self.write(rm + z + 3 * enter)
            time.sleep(sleep_time)
        self.write('# Succesfully Removed/Attempted to Remove ' + rlen + ' files from Router!\n# Here is a list of remaining files: \n' + dirflash)

    def asa_file_del(self):

        # ASA Deletion Logic
        self.write(enter)
        for w in alist:
            self.write(rm1 + w + 4 * enter)
            time.sleep(sleep_time)
        self.write('# Succesfully Removed/Attempted to Remove ' + alen + ' files from ASA!\n# Here is a list of remaining files: \n' + dirflash)

# Toggling the while loop for break loop

class command_open(ser_instance):

    def __init__(self):
        pass

    def command_keywords(self):
        pass     

"""
while True:
    if keyboard.is_pressed('F9') and keyrelease:
        while breakloop == True:
            breakcmd = 'break'
            keyboard.press(breakcmd)
            print('ON')
            time.sleep(1)
        status = 'ON'
        notstatus = 'OFF'
        keyboard.write('# You have successfully turned ' + status + ' the automatic break loop that triggers every second.\n# To toggle ' + notstatus + ' the looping function, please press F9 again\n')
        breakloop = not breakloop
        keyrelease == False
    if not keyboard.is_pressed('F9'):
        keyrelease == True
        status = 'OFF'
        notstatus = 'ON'
"""

# Start the PyQt based application window which will house smaller views of each of the consoles, as well as buttons for performing different functions

