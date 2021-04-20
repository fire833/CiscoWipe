#!/usr/bin/env python3
###############################################
#
# Initial write method (used by all device-oriented wipe methods)
# Defines how to interface with the devices (default is with the pyserial API).
#
################################################

class global_write():

    def __init__(self, port, baud, bytesize, parity, stopbits, timeout, ):
        
        import serial

        ser = serial.Serial(port, baud, bytesize, parity, stopbits, timeout)

        ser.open()