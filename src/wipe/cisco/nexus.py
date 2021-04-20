#!/usr/bin/env python3
###############################################
#
# Class for wiping Cisco Nexus products, tested on (placeholder)
# Utilizes the global write class for writing to device's serial port. 
#
################################################

class nexus_wipe():

    def __init__(self):
        
        from cisco.global_write import global_write as writer

        self.write = writer()

    def rommon(self):
        
        self.write.write('')
