from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec 

import time
import threading 
import keyboard
import os
from typing_database import add_data , show_data , clear_data

URL = "https://www.keybr.com/" 

# EMAIL = "youremail"
# PASSWORD = "your_password"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach" , True) 

# google will nag us with its features 
chrome_options.add_experimental_option(
    "prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False ,  "profile.password_manager_leak_detection": False   # 🔥 THIS is the missing one
    }
)

# this bz google would throw it do not recognize page or page is unsecure error
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Give Selenium it's own user profile. Have your script create a directory in your project folder to store your Chrome Profile information with:

user_data_dir = os.path.join(os.getcwd(),  "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # we are telling to use the directory specified to store our profile. That way when i quit chrome , rerurn selenium script , it keeps all the preferences and settings from my profile .

# below is main part starting . 


class TypingSpeed:
    def __init__(self):
        self.driver = webdriver.Chrome(options = chrome_options) 
        self.wait = WebDriverWait(self.driver, timeout= 60) 

    
    def login(self):
        self.driver.maximize_window()
        self.driver.get(URL) 
        time.sleep(3)

        # crossing the X symbol first 
        # cross_symbol = self.driver.find_element(By.XPATH , value= '//*[@id="nbMLwfFOWk"]/div/div[2]/div/a')  
        # cross_symbol.click()

        # # clicking on sign in button 

        # time.sleep(1)
        # sign_in = self.driver.find_element(By.XPATH, value= '//*[@id="kqbwpAfch2"]/div/nav/div/div[1]/a')
        # sign_in.click()

        # signing with googlu 
        # time.sleep(1)

        # google_btn = self.driver.find_element(By.XPATH , value = '//*[@id="kqbwpAfch2"]/div/main/article/div[1]/span[1]')
        # google_btn.click()


        # entering email 
        # time.sleep(1) 
        # email = self.driver.find_element(By.NAME , value = "identifier") 
        # email.send_keys(EMAIL)

        # # clicking next after entering email 
        # time.sleep(0.5)

        # next = self.driver.find_element(By.XPATH, value = '//*[@id="identifierNext"]/div/button') 
        # next.click()

        # # entering password 
        # time.sleep(2)
        # pwd= self.driver.find_element(By.NAME , value= 'Passwd') 
        # pwd.send_keys(PASSWORD) 
        # time.sleep(0.5)
        # pwd.send_keys(Keys.ENTER) 


    def print_typing_speed(self):
        old_speed = self.driver.find_element(By.XPATH , value= '//*[@id="WDVkIKvR38"]').text
        old_accr = self.driver.find_element(By.XPATH, value= '//*[@id="wDhvk0rXZS"]').text
        previous_stats = (old_speed , old_accr)
        print(f"user-stats = {previous_stats}")


        while(True):
            new_speed = self.driver.find_element(By.XPATH , value= '//*[@id="WDVkIKvR38"]').text # gettig new speed 
            new_accr = self.driver.find_element(By.XPATH, value= '//*[@id="wDhvk0rXZS"]').text
            new_stats = (new_speed , new_accr)

            if(new_stats != previous_stats):
                print(f"new stats = {new_stats}")

                speed = float(new_speed.split(" ")[1].split("w")[0] )
                accuracy = float(new_accr.split(" ")[1].split("%")[0] )
                print("\n\n") 
                add_data(speed, accuracy) 

                previous_stats = new_stats 



            time.sleep(0.3)



    def reset_test(self):
        reset_btn = self.driver.find_element(By.XPATH , value= '//*[@id="xmhZRpmiVa"]/button[2]')
        reset_btn.click() 


    def global_keys(self):
        keyboard.add_hotkey("alt + r" , self.reset_test) 
        keyboard.add_hotkey("alt+s" , show_data)
        keyboard.add_hotkey('alt+c' , clear_data)
        keyboard.wait() 



    

   




obj = TypingSpeed() 
obj.login()
# obj.print_typing_speed()
# time.sleep(10)

# making thread 1 for speed  and thread 2 to reset it .
t1 = threading.Thread(target= obj.print_typing_speed)
t2 = threading.Thread(target= obj.global_keys) 


t1.start() 
t2.start() 

t1.join() 
t2.join() 
 

