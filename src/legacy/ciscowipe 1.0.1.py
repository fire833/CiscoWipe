
#import pyautogui
import keyboard
import os
import sys
import time
from colorama import Fore, Back, Style, Cursor

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
        keyboard.write(rm + y + 3 * enter)
        time.sleep(sleep_time)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.send(slen)
    keyboard.write(' files from Switch!\n# Here is a list of remaining files: \n' + dirflash + enter)

def router_file_del():
    keyboard.write(enter)
    for z in rlist:
        keyboard.write(rm + z + 3 * enter)
        time.sleep(sleep_time)
    keyboard.write('write erase' + enter)
    time.sleep(2)
    keyboard.write(enter)
    keyboard.write('conf t' + enter)
    time.sleep(0.1)
    keyboard.write('config-register 0x2102' + enter)
    time.sleep(0.1)
    keyboard.write('exit' + enter)
    time.sleep(0.1)
    keyboard.write('wr' + enter)
    time.sleep(2)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.send(rlen)
    keyboard.write(' files from Router!\n# Here is a list of remaining files: \n' + dirflash + enter)

def asa_file_del():
    keyboard.write(enter)
    for w in alist:
        keyboard.write(rm1 + w + 4 * enter)
        time.sleep(sleep_time)
    keyboard.write('write erase' + enter)
    time.sleep(2)
    keyboard.write(enter)
    keyboard.write('conf t' + enter + 'a' + enter)
    time.sleep(0.1)
    keyboard.write('config-register 0x2102' + enter)
    time.sleep(0.1)
    keyboard.write('exit' + enter)
    time.sleep(0.1)
    keyboard.write('wr' + enter)
    time.sleep(2)
    keyboard.write('# Succesfully Removed/Attempted to Remove ')
    keyboard.send(alen)
    keyboard.write(' files from ASA!\n# Here is a list of remaining files: \n' + dirflash + enter)

# ROMMON RESET Functions

def router_rommon_exec():
    keyboard.write(enter)
    keyboard.write(confreg + space + register1 + enter)
    time.sleep(3.5)
    keyboard.write(reset + enter)

def wap_rommon_exec():
    keyboard.write(enter)
    time.sleep(0.1)
    keyboard.write(rm + 'private-multiple-fs' + enter)
    time.sleep(0.2)
    keyboard.write('y' + enter)
    time.sleep(0.1)
    keyboard.write(reset + enter)
    time.sleep(0.1)
    keyboard.write('y' + enter)

def switch_rommon_exec():
    keyboard.write(enter)
    for y in slist:
        keyboard.write(rm + y + enter + 'y' + enter)
        time.sleep(0.25)
    keyboard.write(reset + enter + 'y' + enter)

def asa_rommon_exec():
    keyboard.write('escape')
    keyboard.write(confreg + space + register1 + enter)
    time.sleep(10)
    keyboard.write('boot' + enter)


print(Fore.LIGHTYELLOW_EX + 'Thank you for utilizing CiscoWipe 1.0.1! \nThe program has a keyboard input listener, which listens for keybinds to type out certain keystrokes on the keyboard in order to do basic wiping functions over serial terminal!\n' + Fore.RESET)
print(Fore.RED + 'Ctrl' + Fore.CYAN + ' indicates that you want to do initial resetting in ROMMON\n')
print(Fore.LIGHTRED_EX + 'F5' + Fore.CYAN + ' indicates you want to wipe (either in rommon ' + Fore.BLUE + 'with' + Fore.RESET + Fore.CYAN + ' ctrl, or in priv exec without) a Cisco WAP\n' + Fore.RESET)
print(Fore.LIGHTRED_EX + 'F6' + Fore.CYAN + ' indicates you want to wipe (either in rommon ' + Fore.BLUE + 'with' + Fore.RESET + Fore.CYAN + ' ctrl, or in priv exec without) a Cisco Switch\n' + Fore.RESET)
print(Fore.LIGHTRED_EX + 'F7' + Fore.CYAN + ' indicates you want to wipe (either in rommon ' + Fore.BLUE + 'with' + Fore.RESET + Fore.CYAN + ' ctrl, or in priv exec without) a Cisco Router\n' + Fore.RESET)
print(Fore.LIGHTRED_EX + 'F8' + Fore.CYAN + ' indicates you want to wipe (either in rommon ' + Fore.BLUE + 'with' + Fore.RESET + Fore.CYAN + ' ctrl, or in priv exec without) a Cisco Adaptive Security Appliance (ASA)\n' + Fore.RESET)
print(Fore.LIGHTYELLOW_EX + 'Happy Wiping!\n' + Fore.RESET)
# Initial loops for searching for keypresses

msg = 'Deleted / Tried to delete this many files: '

while True:
       
    if keyboard.is_pressed('ctrl+F8'):
        asa_rommon_exec()
    
    elif keyboard.is_pressed('ctrl+F7'):
        router_rommon_exec()

    elif keyboard.is_pressed('ctrl+F6'):
        switch_rommon_exec()

    elif keyboard.is_pressed('ctrl+F5'):
        wap_rommon_exec()
    
    elif keyboard.is_pressed('F5'):
        wap_file_del()
        print(msg + str(wlen))

    elif keyboard.is_pressed('F6'):
        switch_file_del()
        print(msg + str(slen))

    elif keyboard.is_pressed('F7'):
        router_file_del()
        print(msg + str(rlen))
    
    elif keyboard.is_pressed('F8'):
        asa_file_del()
        print(msg + str(alen))
  
    time.sleep(0.1)
