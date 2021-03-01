
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
wap_commands_list = os.path.join(sys.path[0], 'wap_commands.txt')
switch_commands_list = os.path.join(sys.path[0], 'switch_commands.txt')
router_commands_list = os.path.join(sys.path[0], 'router_commands.txt')
asa_commands_list = os.path.join(sys.path[0], 'security_appl_commands.txt')
space = ' '
sleep_time = 0.05
w = 0
x = 0
y = 0
z = 0
dirflash = 'dir flash:\n'
breakloop = False
keyrelease = True

# Importing the command lists and saving them as collections in memory

with open(wap_commands_list, 'r') as wap:
    cm1 = wap.read()
    wlist = cm1.splitlines()
    wlen = str(len(wlist))

with open(switch_commands_list, 'r') as switch:
    cm2 = switch.read()
    slist = cm2.splitlines()
    slen = str(len(slist))

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
    
    def write(self, data):
        keyboard = Controller()
        keyboard.type(data)

    def wap_file_del(self):
        
        # WAP Deletion logic
        self.write(enter)
        for x in wlist:
            self.write(rm1 + x + 3 * enter)
            time.sleep(sleep_time)
        self.write('delete /recursive /force flash:configs\n')
        self.write('# Succesfully Removed/Attempted to Remove ' + wlen + ' files from WAP!\n# Here is a list of remaining files: \n' + dirflash)

    def switch_file_del(self):
    
        # Switch Deletion Logic
        self.write(enter)
        for y in slist:
            self.write(rm + y + 3 * enter)
            time.sleep(sleep_time)
        self.write('# Succesfully Removed/Attempted to Remove ' + slen + ' files from Switch!\n# Here is a list of remaining files: \n' + dirflash)

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

class rommon_del(main_del):

    # ROMMON RESET Functions

    def router_rommon_exec(self):
        self.write(enter)
        self.write(confreg + register1 + enter)
        time.sleep(3.5)
        self.write(reset + enter)

    def wap_rommon_exec(self):
        self.write(enter)
        self.write(rm + 'private_multiple_fs' + enter + 'y' + enter)
        time.sleep(0.1)
        self.write(reset + enter + 'y' + enter)

    def switch_rommon_exec(self):
        self.write(enter)
        for y in slist:
            self.write(rm + y + enter + 'y' + enter)
            time.sleep(sleep_time)

    def asa_rommon_exec(self):
        self.write('escape')
        self.write(confreg + space + register1)
        time.sleep(10)
        self.write('boot' + enter)

class serialwords():

    def __init__(self):
        pass

    def options(self):
        pass

class ser_open():
    
    from tech import Tech_stuff
    import serial
    import keyword

    def __init__(self, port, baud):
        self.ser = serial.Serial(port=port, baudrate=baud)
        self.ser.open()
        self.is_reading_done = False
        self.is_wap = False
        self.is_switch = False
        self.is_router = False
        self.is_asa = False
        self.is_in_rommon = False
        self.is_in_priv_exec = False
        while True:
            self.reader().search_keywords()

    def reader(self):
        # In theory, read 1\ lines, place the string into a list, and update _is reading done to trigger the word search function.
        num = 0 
        self.lines = []
        while num < 1:
            self.ser.read_until().append(self.lines)
            num = num + 1
        self.is_reading_done = True
    
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
                
                self.ser.write("\n")
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

            elif(words_and_phrases[15] in self.lines):

                self.is_in_rommon = True
                self.is_reading_done = False
            
            elif(words_and_phrases[16] in self.lines):

                self.is_asa = True
                self.is_reading_done = False

            elif(words_and_phrases[17] in self.lines):
                
                self.info = True
                self.is_reading_done = False
            
            else:
                
                self.lines = []
                self.is_reading_done = False
            
    def no_config_dialogue(self):
        no = 'no'
        self.ser.write(no.encode())
        self.ser.write('\n')

    def username_and_pass(self):
        cisco = 'Cisco'
        self.ser.write(cisco.encode())
        self.ser.write('\n')

# Toggling the while loop for break loop

class command_open(ser_open):

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

main_del = main_del()

with keyboard.GlobalHotKeys({

'<f5>': main_del.wap_file_del(), 
'<f6>': main_del.switch_file_del(), 
'<f7>': main_del.router_file_del(), 
'<f8>': main_del.asa_file_del()

}) as hkeys:
    hkeys.join()

print("HI")
# Loops for looking for command input