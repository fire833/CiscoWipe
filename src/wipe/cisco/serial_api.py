#!/usr/bin/env python3
###############################################
#
# Classes for interfacing with serial-to-information APIs for Cisco, Dell, HP, among others.
# Uses requests package and json to send out RESTful API requests and parses the JSON responses for each of the 
#
################################################

class cisco_api():

    def __init__(self):
        pass

    def cisco_req(self, serial):
        import requests
        
        self.req = requests.get("https://api.cisco.com/product/v1/information/serial_numbers/" + str(serial))

        self.req.json()

        return self.req

class juniper_api():

    def __init__(self):
        pass

    def juniper_req(self, serial):
        import requests

        self.req = requests.get("")

    