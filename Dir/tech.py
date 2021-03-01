
# Classes for tech'ing stuff, including the class for raw sleenium interaction, and others.
# Copyright 2021 Kendall Tauser

import os
import sys

class Tech_stuff():
    
    import time
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver

    def __init__(self):
        
        self.link = 'http://mrmprodnew/ProcessSteps/AssetRecoverySummary.aspx'

        self.chromedriver = os.path.join(sys.path[0], 'chromedriver.exe')
        
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
        self.driver.get(self.link)

    def find_element(self, xpath, data):
        
        self.findthing = self.driver.find_element_by_xpath(xpath)
        self.findthing.send_keys(data)
        self.time.sleep(0.25)
    
    def click_element(self, xpath2):
        
        self.click = self.driver.find_element_by_xpath(xpath2)
        self.click.click()

    def new_misc(self):
        
        self.click_element(self.misc)

    def print_basic_tech(self, asset, palletinput, gradeinput, processinput, complianceinput):
        
        self.find_element(self.asset_input, asset)
        self.time.sleep(1)
        map(self.find_element, (self.pallet, self.grade, self.next_process, self.compliance_label), (palletinput, gradeinput, processinput, complianceinput))

    def print_misc_info(self, license, random, custom):
        
        self.new_misc()
        self.find_element(self.misc_textbx, license)
        self.new_misc()
        self.find_element(self.misc_textbx_2, random)
        self.new_misc()
        self.find_element(self.misc_textbx_3, custom)

    def submit_tech(self):
        
        self.click_element(self.submit_asset)

import argparse

def __main__():
    
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
        choices=['r', 'r'], 
        help='Type "r" for sending selected asset/s to Resale process, "t" to send to Teardown process', 

    )