#!/usr/bin/env python3
###############################################
#
# Class for wiping Cisco switching products, tested on (placeholder)
# Utilizes the global write class for writing to device's serial port. 
# Notes: Future versions will use the AI engine to see what files actually need to be deleted from any one unit instaed of relying on the arbitrary file list.
#
################################################

class plain_switch_wipe():

    import time

    def __init__(self):

        import os
        import sys
        from cisco.global_write import global_write as writer
        
        self.switch_commands_list = os.path.join(sys.path[0], 'switch_commands.txt')

        with open(self.switch_commands_list, 'r') as switch:
            self.cm2 = switch.read()
            self.slist = self.cm2.splitlines()
            self.slen = str(len(self.slist))

         # Random Vars

        self.rm = 'del flash:'
        self.rm1 = 'del '
        self.enter = '\n'
        self.config = 'conf t'
        self.confreg = 'confreg'
        self.reset = 'reset'
        self.register1 = '0x2142'
        self.register2 = '0x2102'
        self.space = ' '
        self.sleep_time = 0.05
        self.dirflash = 'dir flash:\n'

        self.write = writer()

    def switch_file_del(self):
    
    # Switch Deletion Logic
        self.write(self.enter)
        for y in self.slist:
            self.write(self.rm + y + 3 * self.enter)
            self.time.sleep(self.sleep_time)
        self.write('# Succesfully Removed/Attempted to Remove ' + self.slen + ' files from Switch!\n# Here is a list of remaining files: \n' + self.dirflash)

    def switch_rommon_exec(self):
        self.write(self.enter)
        for y in self.slist:
            self.write(self.rm + y + self.enter + 'y' + self.enter)
            self.time.sleep(self.sleep_time)