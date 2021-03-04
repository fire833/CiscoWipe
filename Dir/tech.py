
# Classes for tech'ing stuff, including the class for raw selenium interaction, and others.
# Copyright 2021 Kendall Tauser

import os
import sys
import threading
import exceptions
from exceptions import AssetIngestError
from exceptions import CredentialsError

class Tech_stuff():
    
    import time
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver

    def __init__(self, pallet_in, grade_in, process_in, compliance_in, args, misc, assets_to_tech):
        
        self.link = 'http://mrmprodnew/ProcessSteps/AssetRecoverySummary.aspx'

        self.chromedriver = os.path.join(sys.path[0], 'chromedriver.exe')
        
        self.palletinput = pallet_in
        self.gradeinput = grade_in
        self.processinput = process_in
        self.complianceinput = str(compliance_in)
        
        self.asset_input = '//*[@id="ctl00_CPH1_txtSearch"]'
        self.search_assets = '//*[@id="ctl00_CPH1_btnSearch"]'
        self.pallet = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_cmbPallets_Input"]'
        self.grade = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlGrade_Input"]'
        self.next_process = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlNextProcess"]'
        self.compliance_label = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlComplianceLabel"]'
        self.misc = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_btnAdd"]'
        self.misc_textbx = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833637_38_0_True"]'
        self.misc_textbx_2 = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833678_38_0_True"]'
        self.misc_textbx_3 = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833679_38_0_True"]'
        self.submit_asset = '//*[@id="ctl00_CPH1_ccTransGrid1_btnAssetInfoSubmit_input"]'
        
        self.options = self.Options()
        # options.add_argument("--headless")
        self.options.add_argument("--window_size=1920X1080")

        self.driver = self.webdriver.Chrome(chrome_options=self.options, executable_path=self.chromedriver)
        try:
            self.driver.get(self.link)
        except:
            raise ConnectionError('Unable to connect to Makor. Is the server down?')


    def find_element(self, xpath, data):
        
        self.findthing = self.driver.find_element_by_xpath(xpath)
        self.findthing.send_keys(data)
        self.time.sleep(0.25)
    
    def click_element(self, xpath2):
        
        self.click = self.driver.find_element_by_xpath(xpath2)
        self.click.click()

    def new_misc(self, data):
        
        self.click_element(self.misc)
        self.find_element(self.misc_textbx, data)

    def print_basic_tech(self, asset, palletinput, gradeinput, processinput, complianceinput):
        
        self.find_element(self.asset_input, asset)
        self.time.sleep(0.5)
        map(self.find_element, (self.pallet, self.grade, self.next_process, self.compliance_label), (self.palletinput, self.gradeinput, self.processinput, self.complianceinput))

    def submit_tech(self):
        
        self.click_element(self.submit_asset)

    def process_args(self, list):
        # Now comes processing the list and applying the different facets to individual assets depending on what flags are defined in the .txt file.
        # If there is a / after the asset, then the proigram will check for any of the following flags:
        # "r" means that 'Ray or Eric mentioned to scrap/tech selected asset.'
        # "d" means that 'Unit is damaged and unable/not worth being refurbished.'
        # "o" means that 'Unit is deprecated/old/no longer financially viable to resell.'
        # "f" means that 'Unit failed to power on or work properly or is unable to be reset."
        # "p" means that 'Unit is from a provider and may have customer data on it that is unremovable.'
        #
        self.asset_attributes = []
        if is_list == True:
            for line in self.list:
                for x in line:
                    if x == '/':
                        for letters in self.list:
                            if letters == 'r':
                                self.asset_attributes.append('r')
                            elif letters == 'd':
                                self.asset_attributes.append('d')

class credentials():

    def __init__(self):
        pass

    def user(self):
        # Get user input for what their Makor login credentials are, and save them as a string in memory. 
        user = input('Please type your username for logging into Makor: ')
        return user
    
    def passwd(self):
        passwd = input('Please type your password for logging into Makor: ')
        return passwd

def __main__():

    import argparse

    parser = argparse.ArgumentParser(
        description="Define how and what you you want tech'd into Makor with these arguments.")

    parser.add_argument(
        'grade', 
        choices=['a', 'b', 'c', 'd', 'f'], 
        help="Define the grade that you want the asset/s to be tech'd as in Makor", 
        required=True, 
        )

    parser.add_argument(
        '-a', 
        help=' List a single asset, or assets separated by a comma', 
        type=str, 
        default=None, 
        )

    parser.add_argument('filename')
    
    parser.add_argument('-p', '--pallet', 
        help='Define what pallet you want these assets to be placed in', )

    parser.add_argument(
        '--process', 
        choices=['r', 't'], 
        help='Type "r" for sending selected asset/s to Resale process, "t" to send to Teardown process', 
    )

    parser.add_argument(
        '--compliance', 
        choices=['1', '2', '3', '4'], 
        help=' Describe the compliance label you want applied. 1 is: Tested for Key functions. 2 is: Evaluated and Non-Functioning. 3 is: Tested for Full Functions. 4 is: Specialty Electronics.', 
        type=int
    )

    parser.add_argument(
        '--misc', '-m', 
        help='Write in some miscellaneous factor about this asset in Makor', 
        type=str
    )

    parser.add_argument(
        '--args', 
        choices=['r', 'd', 'o'],
        help='Use some of the premade arguments for miscellaneous entries for asset audit page in Makor'
    )

    args = parser.parse_args()

    if args.grade is None:
        parser.error("You need to define what grade you want the assets to be tech'd as")
    
    if args.pallet is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.pallet = '1000000-Default'
        elif args.grade == 'f':
            args.pallet = '1-Default-Pallet-T'
    
    if args.process is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.process = 'Resale'
        elif args.grade == 'f':
            args.process = 'Teardown'
    
    if args.a is None:
        if args.filename is not None:
            try:
                if args.filename.endswith('.txt'):
                    assets2ttech = open(args.filename)
                    list_assets = assets2ttech.read()
                    is_list == True
                    num_lines = len(assets2ttech.readlines())
                else:
                    raise Exception('File given is not a .txt file.')

            except Exception: 
                print('Please give a valid path to a txt file.') 
        else:
            raise FileNotFoundError('No file or asset defined.')
    else:
        is_list == False
    
    if is_list == True:
        lines_per = num_lines / 4
        remain = num_lines % 4
        if remain == 0:
            thread_1 = 1
            

    for _ in range(5):
        try:
            connection = threading.Thread(Tech_stuff(args.pallet, args.grade, args.process, args.compliance, ))
            connection.start()
        except Exception:
            print('Unable to start connections to server.')