from lxml import html
import requests
import codecs
import timeit
import time
import threading
from tkinter import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import date
import pandas as pd


def save_last_email(data):
    with open("email_amount.txt","w") as f:
        f.write(data)
        
def read_last_email():
    try:
        file = open("email_amount.txt", "r")
        last_email = file.read()
        # print(last_email)
        return last_email
    except:
        print("No last Eamil")
        return 0
    
def create_Driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=default')
    options.add_argument('--incognito')
    options.add_argument('--disable-plugin-discovery')
    options.add_argument('--start-maximized')
    # prefs = {
	# "profile.managed_default_content_settings.images":2,
	# "--disable-bundled-ppapi-flash":1
	# }
    # options = Options()
    # options.add_argument('--disable-logging')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_experimental_option("prefs", prefs)
    print("start_driver")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options = options)
    print("started driver")
    return driver

def login():
    driver = create_Driver()
    driver.get("https://mail.google.com")
    time.sleep(3)
    input_gmail = driver.find_element_by_xpath(".//html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")
    input_gmail.send_keys("rebic92000@gmail.com")
    btn_next = driver.find_element_by_id("identifierNext")
    btn_next.click()
    time.sleep(3)
    input_password = driver.find_element_by_xpath(".//div/div/div[@class = 'Xb9hP']/input")
    input_password.send_keys("balotelli92")
    btn_login = driver.find_element_by_xpath(".//html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div")
    btn_login.click()
    return driver
# def cron(driver):
#     amount_email = int(driver.find_element_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/span/span[2]").get_attribute("innerHTML"))
#     print(amount_email)
#     save_last_email(amount_email)
#     return amount_email

def get_current_email(driver):
    while True:
        driver.get("https://mail.google.com/mail/u/0/#inbox")
        current_email = (driver.find_element_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/span/div[1]/span/span[2]").get_attribute("innerHTML").replace("\u202f",""))
        # print(current_email)
        if int(current_email) > 0:
            break
        else:
            time.sleep(10)
            continue
    return int(current_email)
def Run(driver, selection):
    time.sleep(5)
    if selection == 1:
        # threading.Timer(60.0, Run, args=(driver, selection)).start()
        export_email(driver,True)
    else:
        export_email(driver,False)
        
    
    
def export_email(driver,Flag):
    current_email = get_current_email(driver)
    if Flag == True:
        if read_last_email() == "":
            last_email = 0
        else:
            last_email = int(read_last_email())
        target_email =  current_email -last_email
    else:
        target_email = current_email
    if target_email == 0:
        return
    else:
        time.sleep(2)
        driver.find_elements_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[6]/div/div[1]/div[2]/div/table/tbody/tr")[0].click()
        match_list = list()
        league_list = list()
        trend_list = list()
        minute_list = list()
        over_list = list()
        odds_list = list()
        dropped_list = list()
        print("target_email: " , target_email)
        x = 0
        for x in range(target_email):
            try:
                content = driver.find_element_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div").get_attribute("innerHTML").replace("<br>","").split("<div")[0]
                if "Starting in" not in content:
                    match_list.append(content.split("\n")[0])
                    league_list.append(content.split("\n")[1])
                    trend_list.append(content.split("\n")[4])
                    minute_list.append(content.split("\n")[5])
                    over_list.append(content.split("\n")[7].split(":")[0])
                    odds_list.append(content.split("\n")[7].split(" ")[2])
                    dropped_list.append(content.split("\n")[7].split(" ")[3])
                    print("OK")
                btn_next_email = driver.find_element_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[2]")
                if btn_next_email.get_attribute("aria-disabled") == "true" :
                    print("Done")
                    break
                else:
                    btn_next_email.click()
                    time.sleep(1)
                    continue
            except:
                print("Response Error")
                continue
        list_of_alert = list(zip(match_list, league_list, trend_list, minute_list, over_list, odds_list, dropped_list))
        df = pd.DataFrame(list_of_alert, columns = ['MATCH', 'LEAGUE', 'TREND', 'MINUTE', 'OVER', 'ODDS','DROPPED'])
        try:
            df_original = pd.read_csv('result.csv', delimiter = ',')
            df_result = df_original.append(df, ignore_index = True)
            df_result.to_csv(r"result.csv", encoding='utf-8-sig', index = False)
        except:
            df.to_csv(r"result.csv", encoding='utf-8-sig', index = False)    
        save_last_email(str(current_email))
    
    
    
    
def quit_loop():
    driver = login()
    print ("Selection:",var.get())
    global selection
    selection = var.get()
    master.quit()
    if selection == 2:
        Run(driver,selection)
    else:
        while True:
            Run(driver,selection)
    
    
        
        


master = Tk()
var = IntVar()
var.set(1)

Label(master, text = "Select Export Option").grid(row=0, sticky=W)
Radiobutton(master, text = "New Only", variable=var, value = 1).grid(row=1, sticky=W)
Radiobutton(master, text = "Export All", variable=var, value = 2).grid(row=2, sticky=W)
Button(master, width = 20, text = "OK", command=quit_loop).grid(row=3, sticky=W)

master.mainloop()




# driver.get("https://mail.google.com/mail/u/0/#inbox")
# time.sleep(5)
# status = list()
# while True:
#     time.sleep(5)
#     messages = driver.find_elements_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[6]/div/div[1]/div[2]/div/table/tbody/tr")
#     if len(messages) > 1:
#         for x in range(len(messages)):
#             class_name = messages[x].get_attribute("class")
#             status.append(class_name)
#         print(len(status))
#         print(status)
#         break
#     else:
#         continue
# # messages = driver.find_elements_by_xpath(".//td/div/div/div/span/span")


# match_list = list()
# league_list = list()
# trend_list = list()
# minute_list = list()
# over_list = list()
# odds_list = list()
# dropped_list = list()
# btn_prev = driver.find_element_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/span/div[2]")
# print(btn_prev.get_attribute("aria-disabled"))
# messages[0].click()
# while True:   
#     content = driver.find_element_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div").get_attribute("innerHTML").replace("<br>","").split("<div")[0]
#     if "Starting in" not in content:
#         print(len(content.split("\n")))
#         match_list.append(content.split("\n")[0])
#         league_list.append(content.split("\n")[1])
#         trend_list.append(content.split("\n")[4])
#         minute_list.append(content.split("\n")[5])
#         over_list.append(content.split("\n")[7].split(":")[0])
#         odds_list.append(content.split("\n")[7].split(" ")[2])
#         dropped_list.append(content.split("\n")[7].split(" ")[3])
#     # print(messages[x].get_attribute("innerHTML"))
#     but_next_email = driver.find_element_by_xpath(".//html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[2]")
#     if but_next_email.get_attribute("aria-disabled") == "true" :
#         break
#     else:
#         but_next_email.click()
#         continue

# filename = "alert_gmail" + str(date.today()) + ".csv"
# list_of_alert = list(zip(match_list, league_list, trend_list, minute_list, over_list, odds_list, dropped_list))
# df = pd.DataFrame(list_of_alert, columns = ['MATCH', 'LEAGUE', 'TREND', 'MINUTE', 'OVER', 'ODDS','DROPPED'])
# try:
#     df_original = pd.read_csv('result.csv', delimiter = ',')
#     df_result = df_original.append(df, ignore_index = True)
#     df_result.to_csv(r"result.csv", encoding='utf-8-sig', index = False)
# except:
#     df.to_csv(r"result.csv", encoding='utf-8-sig', index = False)



    