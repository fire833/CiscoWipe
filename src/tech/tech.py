<<<<<<< HEAD

# Classes for tech'ing stuff, including the class for raw selenium interaction, and others.
# Copyright 2021 Kendall Tauser

import os
import sys
import threading
import exceptions

class credentials():

    def user(self):
        # Get user input for what their Makor login credentials are, and save them as a string in memory. 
        user = input('Please type your username for logging into Makor: ')
        return user
    
    def passwd(self):
        passwd = input('Please type your password for logging into Makor: ')
        return passwd

class Tech_stuff(credentials):
        
    import time

    
    def __init__(self, pallet_in, grade_in, process_in, compliance_in, assets_to_tech):

        self.link = 'http://mrmprodnew/ProcessSteps/AssetRecoverySummary.aspx'

        self.chromedriver = os.path.join(sys.path[0], 'chromedriver.exe')
        
        self.palletinput = pallet_in
        self.gradeinput = grade_in
        self.processinput = process_in
        self.complianceinput = str(compliance_in)
        self.assets = assets_to_tech
        self.is_list = None
        
        self.asset_input = '//*[@id="ctl00_CPH1_txtSearch"]'
        self.search_assets = '//*[@id="ctl00_CPH1_btnSearch"]'
        self.pallet = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_cmbPallets_Input"]'
        self.grade = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlGrade_Input"]'
        self.next_process = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlNextProcess"]'
        self.compliance_label = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlComplianceLabel"]'
        self.misc = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_btnAdd"]'
        self.misc_textbx = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833637_38_0_True"]'
        self.misc_textbx_prefix = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_783363'
        self.misc_textbx_suffix = '_38_0_True"]'
        self.submit_asset = '//*[@id="ctl00_CPH1_ccTransGrid1_btnAssetInfoSubmit_input"]'

        if assets_to_tech == list:
            self.is_list == True
        else:
            self.is_list == False
        
        self.start(assets_to_tech)
        
    def start(self, assets):
        
        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        
        self.options = Options()
        # self.options.add_argument("--headless")

        self.options.add_argument("--window_size=1920X1080")
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=self.chromedriver)

        try:
            self.driver.get(self.link)
        except:
            raise ConnectionError('Unable to connect to Makor. Is the server down?')

        for asset in self.assets:
            working_asset = self.assets[asset].split()
            self.print_basic_tech(working_asset[0], self.palletinput, self.gradeinput, self.processinput, self.complianceinput)
            self.process_args(working_asset[1])
            if self.process_args(working_asset[1]) == True:
                print(f"Successfully added arguments for asset {working_asset[0]}")
            else:
                print(f"Didn't add any arguments for asset {working_asset[0]}")
            self.submit_tech()
            print(f"Successfully tech'd asset {working_asset[0]}")
                
    def find_element(self, xpath, data):
        
        self.findthing = self.driver.find_element_by_xpath(xpath)
        self.findthing.send_keys(data)
        self.time.sleep(0.25)
    
    def click_element(self, xpath2):
        
        self.click = self.driver.find_element_by_xpath(xpath2)
        self.click.click()

    def new_misc(self, data, num):
        
        self.click_element(self.misc)
        self.time.sleep(0.5)
        self.find_element((self.misc_textbx_prefix + num + self.misc_textbx_suffix), data)

    def print_basic_tech(self, asset, palletinput, gradeinput, processinput, complianceinput):
        
        self.find_element(self.asset_input, asset)
        self.time.sleep(0.5)
        map(self.find_element, (self.pallet, self.grade, self.next_process, self.compliance_label), (self.palletinput, self.gradeinput, self.processinput, self.complianceinput))

    def submit_tech(self):
        
        self.click_element(self.submit_asset)
        self.driver.switch_to_alert().accept()

    def process_args(self, listboi):
        # Now comes processing the list and applying the different facets to individual assets depending on what flags are defined in the .txt file.
        # If there is a / after the asset, then the proigram will check for any of the following flags:
        # "r" means that 'Ray or Eric mentioned to scrap/tech selected asset.'
        # "d" means that 'Unit is damaged and unable/not worth being refurbished.'
        # "o" means that 'Unit is deprecated/old/no longer financially viable to resell.'
        # "f" means that 'Unit failed to power on or work properly or is unable to be reset."
        # "p" means that 'Unit is from a provider and may have customer data on it that is unremovable.'
        #

        for letters in listboi:
            num = 7
            if letters == 'r':
                self.new_misc('Ray or Eric mentioned to scrap/tech selected asset.', str(num))
                num = num + 1
            elif letters == 'd':
                self.new_misc('Unit is damaged and unable/not worth being refurbished.', str(num))
                num = num + 1
            elif letters == 'o':
                self.new_misc('Unit is deprecated/old/no longer financially viable to resell.', str(num))
                num = num + 1
            elif letters == 'f':
                self.new_misc('Unit failed to power on or work properly or is unable to be reset.', str(num))
                num = num + 1
            elif letters == 'p':
                self.new_misc('Unit is from a provider and may have customer data on it that is unremovable.', str(num))
                num = num + 1
                self.applied_attributes = str(num)
            return True
        else: 
            return False


def __main__():

    import argparse
    import concurrent.futures

    parser = argparse.ArgumentParser(
        description="Define how and what you you want tech'd into Makor with these arguments.")

    parser.add_argument(
        'grade', 
        choices=['a', 'b', 'c', 'd', 'f'], 
        help="Define the grade that you want the asset/s to be tech'd as in Makor",  
        )

    parser.add_argument(
        '-a', '--asset', 
        help=' List a single asset, or assets separated by a comma', 
        type=str, 
        default=None, 
        )

    parser.add_argument('--filename', '-f',
    help="(Optional) define the path to the filename that contains the assets you wanrt tech'd"
    )
    
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

    is_list = None

    if args.grade is None:
        parser.error("You need to define what grade you want the assets to be tech'd as")
    
    if args.pallet is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.pallet = '1000000-Default'
        elif args.grade == 'f':
            args.pallet = '1-Default-Pallet-T'
    
    if args.compliance is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.compliance = '1'
        elif args.grade == 'f':
            args.compliance = '2'
    
    if args.process is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.process = 'Resale'
        elif args.grade == 'f':
            args.process = 'Teardown'
    
    if args.asset is None:
        if args.filename is not None:
            try:
                if args.filename.endswith('.txt'):
                    assets2ttech = open(args.filename)
                    list_assets = assets2ttech.read.splitlines()
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
        want_split = 4
        lists = [list_assets[i*num_lines // want_split: (i+1)*num_lines // want_split]
            for i in range(want_split)  ]
        for x in range(start=0, stop=3):
            tech_web_thread = Tech_stuff(args.pallet, args.grade, args.process, args.compliance, lists[x])
            thread = threading.Thread(tech_web_thread)
            thread.start()

#       Outdated version:
#        with concurrent.futures.ThreadPoolExecutor() as executor:
#            # Start threadpool executor for each thread to start parsing args for each asset and teching the assets in each thread's assigned list. 
#            executor.map(Tech_Stuff, args.pallet, args.grade, args.process, args.compliance, (lists[0], lists[1], lists[2], lists[3]))
    
    elif is_list == False:
        try:
            tech_web_thread = Tech_stuff(args.pallet, args.grade, args.process, args.compliance, args.asset)
            thread = threading.Thread(target=tech_web_thread)
            thread.join()
            print("Successfully tech'd asset " + args.asset + " as grade " + args.grade)
        except Exception:
            print(f'Unable to tech asset {args.asset}')


=======

# Classes for tech'ing stuff, including the class for raw selenium interaction, and others.
# Copyright 2021 Kendall Tauser

import os
import sys
import threading
import exceptions

class credentials():

    def user(self):
        # Get user input for what their Makor login credentials are, and save them as a string in memory. 
        user = input('Please type your username for logging into Makor: ')
        return user
    
    def passwd(self):
        passwd = input('Please type your password for logging into Makor: ')
        return passwd

class Tech_stuff(credentials):
        
    import time

    
    def __init__(self, pallet_in, grade_in, process_in, compliance_in, assets_to_tech):

        self.link = 'http://mrmprodnew/ProcessSteps/AssetRecoverySummary.aspx'

        self.chromedriver = os.path.join(sys.path[0], 'chromedriver.exe')
        
        self.palletinput = pallet_in
        self.gradeinput = grade_in
        self.processinput = process_in
        self.complianceinput = str(compliance_in)
        self.assets = assets_to_tech
        self.is_list = None
        
        self.asset_input = '//*[@id="ctl00_CPH1_txtSearch"]'
        self.search_assets = '//*[@id="ctl00_CPH1_btnSearch"]'
        self.pallet = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_cmbPallets_Input"]'
        self.grade = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlGrade_Input"]'
        self.next_process = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlNextProcess"]'
        self.compliance_label = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetInformation_ddlComplianceLabel"]'
        self.misc = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_btnAdd"]'
        self.misc_textbx = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_7833637_38_0_True"]'
        self.misc_textbx_prefix = '//*[@id="ctl00_CPH1_ccTransGrid1_rmaAssetComponents_ctl03_TextBox_Comp_11_2211768_783363'
        self.misc_textbx_suffix = '_38_0_True"]'
        self.submit_asset = '//*[@id="ctl00_CPH1_ccTransGrid1_btnAssetInfoSubmit_input"]'

        if assets_to_tech == list:
            self.is_list == True
        else:
            self.is_list == False
        
        self.start(assets_to_tech)
        
    def start(self, assets):
        
        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        
        self.options = Options()
        # self.options.add_argument("--headless")

        self.options.add_argument("--window_size=1920X1080")
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=self.chromedriver)

        try:
            self.driver.get(self.link)
        except:
            raise ConnectionError('Unable to connect to Makor. Is the server down?')

        for asset in self.assets:
            working_asset = self.assets[asset].split()
            self.print_basic_tech(working_asset[0], self.palletinput, self.gradeinput, self.processinput, self.complianceinput)
            self.process_args(working_asset[1])
            if self.process_args(working_asset[1]) == True:
                print(f"Successfully added arguments for asset {working_asset[0]}")
            else:
                print(f"Didn't add any arguments for asset {working_asset[0]}")
            self.submit_tech()
            print(f"Successfully tech'd asset {working_asset[0]}")
                
    def find_element(self, xpath, data):
        
        self.findthing = self.driver.find_element_by_xpath(xpath)
        self.findthing.send_keys(data)
        self.time.sleep(0.25)
    
    def click_element(self, xpath2):
        
        self.click = self.driver.find_element_by_xpath(xpath2)
        self.click.click()

    def new_misc(self, data, num):
        
        self.click_element(self.misc)
        self.time.sleep(0.5)
        self.find_element((self.misc_textbx_prefix + num + self.misc_textbx_suffix), data)

    def print_basic_tech(self, asset, palletinput, gradeinput, processinput, complianceinput):
        
        self.find_element(self.asset_input, asset)
        self.time.sleep(0.5)
        map(self.find_element, (self.pallet, self.grade, self.next_process, self.compliance_label), (self.palletinput, self.gradeinput, self.processinput, self.complianceinput))

    def submit_tech(self):
        
        self.click_element(self.submit_asset)
        self.driver.switch_to_alert().accept()

    def process_args(self, listboi):
        # Now comes processing the list and applying the different facets to individual assets depending on what flags are defined in the .txt file.
        # If there is a / after the asset, then the proigram will check for any of the following flags:
        # "r" means that 'Ray or Eric mentioned to scrap/tech selected asset.'
        # "d" means that 'Unit is damaged and unable/not worth being refurbished.'
        # "o" means that 'Unit is deprecated/old/no longer financially viable to resell.'
        # "f" means that 'Unit failed to power on or work properly or is unable to be reset."
        # "p" means that 'Unit is from a provider and may have customer data on it that is unremovable.'
        #

        for letters in listboi:
            num = 7
            if letters == 'r':
                self.new_misc('Ray or Eric mentioned to scrap/tech selected asset.', str(num))
                num = num + 1
            elif letters == 'd':
                self.new_misc('Unit is damaged and unable/not worth being refurbished.', str(num))
                num = num + 1
            elif letters == 'o':
                self.new_misc('Unit is deprecated/old/no longer financially viable to resell.', str(num))
                num = num + 1
            elif letters == 'f':
                self.new_misc('Unit failed to power on or work properly or is unable to be reset.', str(num))
                num = num + 1
            elif letters == 'p':
                self.new_misc('Unit is from a provider and may have customer data on it that is unremovable.', str(num))
                num = num + 1
                self.applied_attributes = str(num)
            return True
        else: 
            return False


def __main__():

    import argparse
    import concurrent.futures

    parser = argparse.ArgumentParser(
        description="Define how and what you you want tech'd into Makor with these arguments.")

    parser.add_argument(
        'grade', 
        choices=['a', 'b', 'c', 'd', 'f'], 
        help="Define the grade that you want the asset/s to be tech'd as in Makor",  
        )

    parser.add_argument(
        '-a', '--asset', 
        help=' List a single asset, or assets separated by a comma', 
        type=str, 
        default=None, 
        )

    parser.add_argument('--filename', '-f',
    help="(Optional) define the path to the filename that contains the assets you wanrt tech'd"
    )
    
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

    is_list = None

    if args.grade is None:
        parser.error("You need to define what grade you want the assets to be tech'd as")
    
    if args.pallet is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.pallet = '1000000-Default'
        elif args.grade == 'f':
            args.pallet = '1-Default-Pallet-T'
    
    if args.compliance is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.compliance = '1'
        elif args.grade == 'f':
            args.compliance = '2'
    
    if args.process is None:
        if args.grade == 'a' or 'b' or 'c' or 'd':
            args.process = 'Resale'
        elif args.grade == 'f':
            args.process = 'Teardown'
    
    if args.asset is None:
        if args.filename is not None:
            try:
                if args.filename.endswith('.txt'):
                    assets2ttech = open(args.filename)
                    list_assets = assets2ttech.read.splitlines()
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
        want_split = 4
        lists = [list_assets[i*num_lines // want_split: (i+1)*num_lines // want_split]
            for i in range(want_split)  ]
        for x in range(start=0, stop=3):
            tech_web_thread = Tech_stuff(args.pallet, args.grade, args.process, args.compliance, lists[x])
            thread = threading.Thread(tech_web_thread)
            thread.start()

#       Outdated version:
#        with concurrent.futures.ThreadPoolExecutor() as executor:
#            # Start threadpool executor for each thread to start parsing args for each asset and teching the assets in each thread's assigned list. 
#            executor.map(Tech_Stuff, args.pallet, args.grade, args.process, args.compliance, (lists[0], lists[1], lists[2], lists[3]))
    
    elif is_list == False:
        try:
            tech_web_thread = Tech_stuff(args.pallet, args.grade, args.process, args.compliance, args.asset)
            thread = threading.Thread(target=tech_web_thread)
            thread.join()
            print("Successfully tech'd asset " + args.asset + " as grade " + args.grade)
        except Exception:
            print(f'Unable to tech asset {args.asset}')


>>>>>>> 702a546da1e7687c7f6840999a5263ae5a294833
__main__()