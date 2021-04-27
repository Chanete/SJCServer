from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time
import sys 
import config
import os
import logging

falcon_logger = logging.getLogger('gunicorn.error')

def pinta_ids(driver):
    ids = driver.find_elements_by_xpath('//*[@id]')
    for ii in ids:
    #print ii.tag_name
        print(ii.get_attribute('id') )

def check_id(driver,id):
    ids = driver.find_elements_by_xpath('//*[@id]')
    for ii in ids:
        if (ii.get_attribute('id') == id):
            return True
    return False


def auth(url,canal):
    falcon_logger.info("Matando instancias del navegador abiertas...")
    os.system("pkill firefox")
    """
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path="/home/sjc/SJCServer/chrome/geckodriver")
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10) # Timeout maximo de pagina
    """
    clave=config.YT.CANALES[canal][1]


    falcon_logger.info("Solicitando URL %s " %url)

    driver_path = "/home/sjc/SJCServer/chrome/chromedriver"
    brave_path = "/usr/bin/brave-browser"

    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
# option.add_argument("--incognito") OPTIONAL
    option.add_argument("--headless") 

# Create new Instance of Chrome
    print("voy")
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    print("vengo")


#    driver.get("https://accounts.google.com/o/oauth2/v2/auth?client_id=901857448933-immj7hkvc618r2hnm7130e3lanc535l5.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Fbueso.itelsys.com%3A1313%2FSJC%2FOARedir&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube&login_hint=internoSjc%40gmail.com&access_type=offline&response_type=code&state=Interno&prompt=consent")
    driver.get(url)
    driver.save_screenshot('screenshot1.png') 
    
    if (check_id(driver, "next")):
        e=driver.find_element_by_id("next")
        falcon_logger.info("Pulsando Next")
        e.click()
        time.sleep(2)  
        driver.save_screenshot('screenshot2.png') 
        e=driver.find_element_by_id("password")
        falcon_logger.info("Escribiendo clave")
        e.send_keys(clave)
        e=driver.find_element_by_id("submit")
        falcon_logger.info("Click en Submit")
        e.click()
        time.sleep(2)
        driver.save_screenshot('screenshot3.png') 
    if (check_id(driver, "submit_approve_access")):
        falcon_logger.info("Mandando Aprove")
        e=driver.find_element_by_id("submit_approve_access")
        e.click()
        time.sleep(2)
        driver.save_screenshot('screenshot4.png') 
        if (check_id(driver, "submit_approve_access")):
            falcon_logger.info("Mandando Aprove")
            e=driver.find_element_by_id("submit_approve_access")
            e.click()
            time.sleep(2)
            driver.save_screenshot('screenshot5.png') 
    falcon_logger.info("Logon Terminado")

