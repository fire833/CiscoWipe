#!/usr/bin/env python3
###############################################
#
# Class for wiping Cisco WAP products, tested on (placeholder)
# Utilizes the global write class for writing to device's serial port. 
# Notes: Future versions will use the AI engine to see what files actually need to be deleted from any one unit instaed of relying on the arbiitrary file list.
#
################################################

class wap_wipe():

    import time

    def __init__(self):

        import os
        import sys
        from global_write import global_write as writer
        
        self.wap_commands_list = os.path.join(sys.path[0], 'wap_commands.txt')

        with open(self.wap_commands_list, 'r') as wap:
            self.cm1 = wap.read()
            self.wlist = self.cm1.splitlines()
            self.wlen = str(len(self.wlist))

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

    def wap_file_del(self):
        
        # WAP Deletion logic
        self.write(self.enter)
        for x in self.wlist:
            self.write(self.rm1 + x + 3 * self.enter)
            self.time.sleep(self.sleep_time)
        self.write('delete /recursive /force flash:configs\n')
        self.write('# Succesfully Removed/Attempted to Remove ' + self.wlen + ' files from WAP!\n# Here is a list of remaining files: \n' + self.dirflash)
        
    def wap_rommon_exec(self):
        self.write(self.enter)
        self.write(self.rm + 'private_multiple_fs' + self.enter + 'y' + self.enter)
        self.time.sleep(0.1)
        self.write(self.reset + self.enter + 'y' + self.enter)