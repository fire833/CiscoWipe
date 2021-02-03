
#import pyautogui
import keyboard
import os
import sys
import time
import argparse
import cmd
import serial
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
    wlen = len(wlist)

with open(switch_commands_list, 'r') as switch:
    cm2 = switch.read()
    slist = cm2.splitlines()
    slen = len(slist)

with open(router_commands_list, 'r') as router:
    cm3 = router.read()
    rlist = cm3.splitlines()
    rlen = len(rlist)

with open(asa_commands_list, 'r') as asa:
    cm4 = asa.read()
    alist = cm4.splitlines()
    alen = len(alist)

# Basic purge all files based on command list functions

def wap_file_del():
    keyboard.write(enter)
    for x in wlist:
        keyboard.write(rm1 + x + 3 * enter)
        time.sleep(sleep_time)
    keyboard.write('delete /recursive /force flash:configs\n')
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.send(wlen)
    keyboard.write(' files from WAP!\n# Here is a list of remaining files: \n' + dirflash + enter)

def switch_file_del():
    keyboard.write(enter)
    for y in slist:
        keyboard.write(rm + y + enter + 'y' + enter)
        time.sleep(sleep_time)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.send(slen)
    keyboard.write(' files from Switch!\n# Here is a list of remaining files: \n' + dirflash + enter)

def router_file_del():
    keyboard.write(enter)
    for z in rlist:
        keyboard.write(rm + z + 3 * enter)
        time.sleep(sleep_time)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.send(rlen)
    keyboard.write(' files from Router!\n# Here is a list of remaining files: \n' + dirflash + enter)

def asa_file_del():
    keyboard.write(enter)
    for w in alist:
        keyboard.write(rm1 + w + 4 * enter)
        time.sleep(sleep_time)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.send(alen)
    keyboard.write(' files from ASA!\n# Here is a list of remaining files: \n' + dirflash + enter)

# ROMMON RESET Functions

def router_rommon_exec():
    keyboard.write(enter)
    keyboard.write(confreg + register1 + enter)
    time.sleep(3.5)
    keyboard.write(reset + enter)

def wap_rommon_exec():
    keyboard.write(enter)
    keyboard.write(rm + 'private_multiple_fs' + enter + 'y' + enter)
    time.sleep(0.1)
    keyboard.write(reset + enter + 'y' + enter)

def switch_rommon_exec():
    keyboard.write(enter)
    for y in slist:
        keyboard.write(rm + y + enter + 'y' + enter)
        time.sleep(sleep_time)

def asa_rommon_exec():
    keyboard.write('escape')
    keyboard.write(confreg + space + register1)
    time.sleep(10)
    keyboard.write('boot' + enter)

"""
options = Options()
options.add_argument("--headless")
options.add_argument("--window_size=1920X1080")
        
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
driver.get(link)

def print_basic_tech(asset, palletinput, gradeinput, processinput, complianceinput):
    driver.find_element_by_xpath(asset_input)
    driver.send_keys(asset + enter)
    driver.find_element_by_xpath(pallet)
    driver.send_keys(palletinput)
    driver.find_element_by_xpath(grade)
    driver.send_keys(gradeinput)
    driver.find_element_by_xpath(next_process)
    driver.send_keys(processinput)
    driver.find_element_by_xpath(compliance_label)
    driver.send_keys(complianceinput)

def new_misc()
        driver.find_element_by_xpath(misc)
        driver.click(misc)

def print_misc_info(license, random, custom)
    new_misc()
    driver.find_element_by_xpath(misc_textbx)
    driver.send_keys(license)
    new_misc()
    driver.find_element_by_xpath(misc_textbx_2)
    driver.send_keys(random)
    new_misc()
    driver.find_element_by_xpath(misc_textbx_3)
    driver.send_keys(custom)

def submit_tech()
    driver.find_element_by_xpath(submit_asset)
"""

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

input('What do you want to do? Type "help" for help\n>>')

# Initial loops for searching for keypresses

one = 1
while True:
    if keyboard.is_pressed('F5'):
        wap_file_del()
        print(wlen)

    elif keyboard.is_pressed('F6'):
        switch_file_del()
        print(slen)

    elif keyboard.is_pressed('F7'):
        router_file_del()
        print(rlen)
    
    elif keyboard.is_pressed('F8'):
        asa_file_del()
        print(alen)
    
    time.sleep(0.1)

# Loops for looking for command input

