#!/usr/bin/env python3
###############################################
#
# Logic for creating dataset for training an ai model for file classification on cisco IOS devices
# Notes: Looking to create some sort of modular 
# Copyright 2021 Kendall Tauser
#
###############################################

import itertools
from itertools import permutations
import csv
import os
import sys
import random
import pandas as pd

## Triggers for recomputing different parts of the data ##
ios_model_done = True
ap_model_done = True
pkg_model_done = True
cp_conf_done = True
##########################################################

model =  ['c2900-', 'c1000-', 'c1600-', 'c2500-', 'c2800-', 'c3620-', 'c3640-', 'c4000-', 'c4500-', 'c3750-', 'c3700-', 'c3600-', 'c2960s-']

service = ['universal','i-', 'a2-', 'a-', 'b-', 'c-', 'I-', 'j-', 'o-', 'p-', 'v-', 'advipservices', 'ipservices', 'advipservices-', 'ipservices-', 'universal-', 'ipbase','ipbase-', ]

crypto = ['k9', 'k8', '']

compression = ['', '-mz', '-m', '-z', '-tar', '-mx']

revision1 = ['.12', '.13', '.14', '.15', '.default', '.153', '.154', '.155', '.156', '.157', '.152', '.151']

revision2 = ['', '-1', '-2', '-3', '-4', '-5']

suffix = ['.bin']

ap_mod = ['ap3g1-', 'ap3g2-', 'ap3g3-', 'ap1g1-', 'ap1g2-', 'ap1g3-', 'ap2g1-', 'ap2g2-', 'ap2g3-']

ap_service = ['k9w7', 'k9w7-' ,'k9w8-', 'k9w8', 'rcvk9w8', 'rcvk9w8-']

ap_suffix = ['.JD14', '.JF7', '.JD10', '.JD11', '.JD12', '.JD13', '.JD15', '.JF5',  '.JF6', '.JF8', '.JF9',  '.JF10', '.JF11', '.JF12']

pkg_type = ['anyconnect-linux', 'anyconnect-macosx-i386', 'anyconnect-windows', 'securedesktop-asa', 'sslclient-win', 'securedesktop-ios', 'anyconnect-win', 'sslclient-win', 'csd_', 'anyconnect-macos']

pkg_numbers = ['-1.', '-2.', '-3.', '-4.', '-5.', '-6.', '-7.', '-8.', '-9.', '-0.']



combinations = []
with open(os.path.join(sys.path[0], "data.csv"), "w", newline='') as data:
    writer = csv.writer(data, dialect='excel')

    if ios_model_done == False:
        for mod in model:
            for serv in service:
                for crypt in crypto:
                    for comp in compression:
                        for rev1 in revision1:
                            for rev2 in revision2:
                                for suf in suffix:
                                    combinations = [mod + serv + crypt + comp + rev1 + rev2 + suf, '0']
                                    writer.writerow(combinations)
                                    combinations = []
    else:
        print('Skipping IOS image model data computation. ')

    if ap_model_done == False:
        for mod in ap_mod:
            for serv in ap_service:
                for comp in compression:
                    for rev1 in revision1:
                        for rev2 in revision2:
                            for suf in ap_suffix:
                                combinations = [mod + serv + comp + rev1 + rev2 + suf, '0']
                                writer.writerow(combinations)
                                combinations = []
    else:
        print('Skipping AP model data computation. ')

    
    if pkg_model_done == False:
        #Do five iterations for the sake of providing more random numbers
        for x in range(5):
            for typ in pkg_type:
                for num in pkg_numbers:
                    number = random.randint(1111,22222)
                    combinations = [typ + num + str(number) + '-k9.pkg', '1']
                    writer.writerow(combinations)
                    combinations = []
    else:
        print('Skipping Package model data computation. ')

    if cp_conf_done == False:
        for x in range(9999):
            num = x
            combinations = ['cpconfig-' + str(num) + '.cfg,1']
            writer.writerow(combinations)
            combinations = []
    else:
        print('Skipping cp-config model data computation. ')

dataset = pd.read_csv(os.path.join(sys.path[0], "data.csv"))
#dataset.shuffle()
    
dataset.head()