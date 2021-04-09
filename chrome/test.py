from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

#import chromedriver_binary
import time
import sys 


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


service_log_path = "chromedriver.log"
service_args = ['--verbose']
# Parametros de funcionamiento de Chrome
"""
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-dev-shm-usage");
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--ignore-certificate-errors')  # Importante par sitios SSL que no tengamos CA
chrome_options.add_argument("--user-data-dir=/tmp/selenium")
#chrome_options.add_experimental_option("prefs", {"profile.block_third_party_cookies": False})
chrome_options.AcceptInsecureCertificates = True
#driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options, service_args=service_args, service_log_path=service_log_path)
from selenium.webdriver import Firefox 
"""
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
#action = ActionChains(driver)
wait = WebDriverWait(driver, 10) # Timeout maximo de pagina

print("Pido")
driver.get("https://accounts.google.com/o/oauth2/v2/auth?client_id=901857448933-immj7hkvc618r2hnm7130e3lanc535l5.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Fbueso.itelsys.com%3A1313%2FSJC%2FOARedir&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube&login_hint=internoSjc%40gmail.com&access_type=offline&response_type=code&state=Interno&prompt=consent")
print("Salvo")
driver.save_screenshot('screenshot1.png') 
print("busco clsass")
if (check_id(driver, "next")):
    e=driver.find_element_by_id("next")
    print("Click")
    e.click()
    print("Espero")
    time.sleep(2)  
    print("Salvo")
    driver.save_screenshot('screenshot2.png') 
    e=driver.find_element_by_id("password")
    print("escribo pass")
    e.send_keys("2de01ad4")
    print("Picbho click")
    e=driver.find_element_by_id("submit")
    e.click()
    time.sleep(2)
    driver.save_screenshot('screenshot3.png') 
if (check_id(driver, "submit_approve_access")):
    print("Mando aprove")
    e=driver.find_element_by_id("submit_approve_access")
    e.click()
    time.sleep(2)
    driver.save_screenshot('screenshot4.png') 
    if (check_id(driver, "submit_approve_access")):
        print("Mando aprove2")
        e=driver.find_element_by_id("submit_approve_access")
        e.click()
        time.sleep(2)
        driver.save_screenshot('screenshot5.png') 


pinta_ids(driver)
