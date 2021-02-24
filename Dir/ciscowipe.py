
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

# Vars for Tech web interfacing

link = 'http://mrmprodnew/ProcessSteps/AssetRecoverySummary.aspx'

asset_input = '//*[@id="ctl00_CPH1_txtSearch"]'
search_assets = '//*[@id="ctl00_CPH1_btnSearch"]'
pallet = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_cmbPallets_Input"]'
grade = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlGrade_Input"]'
next_process = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlNextProcess"]'
compliance_label = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlComplianceLabel"]'
misc = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_btnAdd"]'
misc_textbx = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833637_38_0_True"]'
misc_textbx_2 = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833678_38_0_True"]'
misc_textbx_3 = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833679_38_0_True"]'
submit_asset = '//*[@id="ctl00_CPH1_ccTransGrid1_btnAssetInfoSubmit_input"]'

chromedriver = os.path.join(sys.path[0], 'chromedriver.exe')

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


class Tech_stuff():
    
    import time
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver

    def __init__(self):
        self.options = Options()
        # options.add_argument("--headless")
        self.options.add_argument("--window_size=1920X1080")
        
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=chromedriver)
        self.driver.get(link)

    def find_element(self, xpath, data):
        self.findthing = self.driver.find_element_by_xpath(xpath)
        self.findthing.send_keys(data)
        time.sleep(0.25)
    
    def click_element(self, xpath2):
        self.click = self.driver.find_element_by_xpath(xpath2)
        self.click.click()

    def new_misc(self):
        self.click_element(misc)

    def print_basic_tech(self, asset, palletinput, gradeinput, processinput, complianceinput):
        self.find_element(asset_input, asset)
        self.time.sleep(1)
        map(self.find_element, (pallet, grade, next_process, compliance_label), (palletinput, gradeinput, processinput, complianceinput))

    def print_misc_info(self, license, random, custom):
        self.new_misc()
        self.find_element(misc_textbx, license)
        self.new_misc()
        self.find_element(misc_textbx_2, random)
        self.new_misc()
        self.find_element(misc_textbx_3, custom)

    def submit_tech(self):
        self.click_element(submit_asset)

class serialwords():

    def __init__(self):
        pass

    def options(self):
        pass

class ser_open(Tech_stuff):
    
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
    
    def reader(self):
        # In theory, read 5 lines, place them into a list, and update _is reading done to trigger the word search function.
        num = 0 
        self.lines = []
        while num < 1:
            self.ser.read_until().append(self.lines)
            num = num + 1
        self.is_reading_done = True
    
    def search_keywords(self):
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
            
            elif(words_and_phrases[8] or words_and_phrases[10] in self.lines):
                
                self.username_and_pass()
                self.lines = []
            
            elif(words_and_phrases[3] or words_and_phrases[13] in self.lines):
                
                self.ser.write("\n")
                self.lines = []
            
            elif(words_and_phrases[4] in self.lines):
                
                self.is_router = True
            
            elif(words_and_phrases[5] in self.lines):

                self.is_wap = True
            
            elif(words_and_phrases[14] in self.lines):

                self.is_asa = True

            elif(words_and_phrases[15] in self.lines):

                self.is_in_rommon = True
            
            elif(words_and_phrases[16] in self.lines):

                self.is_asa = True

            elif(words_and_phrases[17] in self.lines):
                
                self.info = True
            
            else:
                self.lines = []
            
    def no_config_dialogue(self):
        no = 'no'
        self.ser.write(no.encode())
        self.ser.write('\n')

    def username_and_pass(self):
        cisco = 'Cisco'
        self.ser.write(cisco.encode())
        self.ser.write('\n')

# Toggling the while loop for break loop

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

