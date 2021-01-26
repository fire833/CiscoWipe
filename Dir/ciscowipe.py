
#import pyautogui
import keyboard
import os
import sys
import time

# Random Vars

rm = 'del '
enter = '\n'
config = 'conf t'
register1 = '0x2142'
register2 = '0x2102'
wap_commands_list = os.path.join(sys.path[0], 'wap_commands.txt')
switch_commands_list = os.path.join(sys.path[0], 'switch_commands.txt')
router_commands_list = os.path.join(sys.path[0], 'router_commands.txt')
space = ' '
sleep_time = 0.05
x = 0
y = 0
z = 0
dirflash = 'dir flash\n'

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

# Basic purge all files based on command list functions

def wap_file_del():
    keyboard.write(enter)
    for x in wlist:
        keyboard.write(rm + x + 3 * enter)
        time.sleep(sleep_time)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.press(wlen)
    keyboard.write(' files from WAP!\n# Here is a list of remaining files: \n' + dirflash)

def switch_file_del():
    keyboard.write(enter)
    for y in slist:
        keyboard.write(rm + y + 3 * enter)
        time.sleep(sleep_time)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.press(slen)
    keyboard.write(' files from Switch!\n# Here is a list of remaining files: \n' + dirflash)

def router_file_del():
    keyboard.write(enter)
    for z in rlist:
        keyboard.write(rm + z + 3 * enter)
        time.sleep(sleep_time)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.press(rlen)
    keyboard.write(' files from Router!\n# Here is a list of remaining files: \n' + dirflash)

"""
with open(wap_commands) as f:
    content = f.readlines()
for line in content:
    print(line)
"""   

# Initial loops for searching for keypresses

while True:
    if keyboard.is_pressed('1'):
        wap_file_del()

    elif keyboard.is_pressed('2'):
        print('You are pressing key')

