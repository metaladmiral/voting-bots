from random import randint
import time
import sys
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging

arguments = sys.argv
user_arguments = arguments[1:]
filename = 'voting_log_batch'+user_arguments[0]+'.log'
logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# options = Options()
# options.add_argument("-headless")

class app:
    def __init__(self) -> None:
        self.totalVotes = 0
        self.main_url = "https://my.syok.my/charts/my-music-chart-2020/my-20chart-186"        
        # self.main_url = "https://google.com"        
        self.first_run = True
        # self.total_captcha_err = 0
        self.run()

    def open_browser(self) :

        options = Options()

        ua = UserAgent()
        user_agent = ua.random

        service = Service(executable_path=r"C:\Users\mypra\Downloads\geckodriver.exe")
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference("browser.link.open_newwindow", 3)
        profile.set_preference("browser.link.open_newwindow.restriction", 2)
        profile.update_preferences()
        
        options.profile = profile
        options.add_argument("--width=800")
        options.add_argument("--height=600")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("-headless")

        self.driver = webdriver.Firefox(service=service, options=options)

    def vote(self):
        time.sleep(2)
        print('trying')
        try:
            if(self.first_run):
                self.driver.get(self.main_url)
                self.first_run = False
            else:
                self.driver.execute_script('''window.open("","_blank");''')
                previous_window = self.driver.window_handles[0]
                new_window = self.driver.window_handles[-1]
                time.sleep(2)
                self.driver.switch_to.window(previous_window)
                self.driver.close()

                time.sleep(2)

                self.driver.switch_to.window(new_window)
                self.driver.get(self.main_url)

                time.sleep(2)

            try:
                self.driver.find_element(By.XPATH, '//*[@id="p_lt_Content_pageplaceholder_p_lt_ctl02_Repeater_repItems_ctl00_ctl00_VoteBtn"]').click()
                self.totalVotes += 1
                logging.info(f"Vote cast "+str(self.totalVotes))
                time.sleep(5)
            except Exception as e:
                logging.info(f"Vote cast failed! trying again :"+str(e))

        except Exception as e:
            logging.info(f"exception occured: "+str(e))

        self.vote()

    def run(self):
        self.open_browser()
        time.sleep(2)
        self.vote()



app()