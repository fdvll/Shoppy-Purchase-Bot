import time
import json
from colorama import init, Fore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

init(autoreset=True)

json_file = open("../config.json")
variables = json.load(json_file)
json_file.close()
link = variables["productlink"]
amount = variables["amount"]
email = variables["email"]
cardholder = variables["cardholder"]
cardnumbers = variables["cardnumbers"]
expirationdate = variables["expirationdate"]
cvv = variables["cvv"]
zipcode = variables["zipcode"]

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("window-size=1800,800")
driver = webdriver.Chrome(options=options)
driver.get(link)
time.sleep(0.5)

print(Fore.BLUE + '[BEGINNING CHECK] Starting beginning checking process')
purchasebutton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-product"]/div/div[2]/div[1]/div[3]/div/div/div/button'))).get_attribute("class")
if purchasebutton == 'button button--primary button--block':
    outofstock = False
    print(Fore.GREEN + '[BEGINNING CHECK] Product in stock, beginning buy process')
elif purchasebutton == 'button button--primary':
    outofstock = True
    print(Fore.RED + '[BEGINNING CHECK] Product out of stock, beginning reload process')

print(Fore.BLUE + '[RELOAD PROCESS] Starting reload process')
while outofstock == True:
    driver.get(link)
    time.sleep(0.25)
    print(Fore.WHITE + '[RELOAD PROCESS] Reloaded, checking if product is in stock')
    purchasebutton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-product"]/div/div[2]/div[1]/div[3]/div/div/div/button'))).get_attribute("class")
    if purchasebutton == 'button button--primary button--block':
        outofstock = False
        print(Fore.GREEN + '[RELOAD PROCESS] Product in stock, beginning buy process')
    elif purchasebutton == 'button button--primary':
        outofstock = True
        print(Fore.RED + '[RELOAD PROCESS] Product is not in stock, reloading')

if outofstock == False:
    print(Fore.BLUE + '[BUY PROCESS] Started buy process')
    print(Fore.WHITE + '[BUY PROCESS] Entering details')
    driver.find_element_by_xpath('//*[@id="user-product"]/div/div[2]/div[1]/div[3]/div/div/div/div/input').clear()
    print(Fore.WHITE + '[BUY PROCESS] Cleared amount input')
    driver.find_element_by_xpath('//*[@id="user-product"]/div/div[2]/div[1]/div[3]/div/div/div/div/input').send_keys(amount)
    print(Fore.WHITE + '[BUY PROCESS] Input amount')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="user-product"]/div/div[2]/div[1]/div[3]/div/div/div/button'))).click()
    print(Fore.WHITE + '[BUY PROCESS] Pressed purchase button')
    driver.find_element_by_xpath('//*[@id="user-product"]/div/div[2]/div[1]/div[3]/div/ul/div[1]/li/div').click()
    print(Fore.WHITE + '[BUY PROCESS] Chose payment option')
    driver.find_element_by_xpath('//*[@id="user-product"]/div/div[2]/div[1]/div[3]/div/span/input').send_keys(email)
    print(Fore.WHITE + '[BUY PROCESS] Input email')
    driver.find_element_by_xpath('//*[@id="user-product"]/div/div[2]/div[1]/div[4]/div/div[2]').click()
    print(Fore.WHITE + '[BUY PROCESS] Proceeding to next page')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="stripe-card-element-cardholder"]'))).send_keys(cardholder)
    print(Fore.WHITE + '[BUY PROCESS] Input cardholder')
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="stripe-card-element"]/div/iframe'))
    print(Fore.WHITE + '[BUY PROCESS] Entered frame')
    driver.find_element_by_xpath('//*[@id="root"]/form/div/div[2]/span[1]/span[2]/div/div[2]/span/input').send_keys(cardnumbers)
    print(Fore.WHITE + '[BUY PROCESS] Input card numbers')
    driver.find_element_by_xpath('//*[@id="root"]/form/div/div[2]/span[2]/span/span/input').send_keys(expirationdate)
    print(Fore.WHITE + '[BUY PROCESS] Input card expiration date')
    driver.find_element_by_xpath('//*[@id="root"]/form/div/div[2]/span[3]/span/span/input').send_keys(cvv)
    print(Fore.WHITE + '[BUY PROCESS] Input card CVV')
    driver.find_element_by_xpath('//*[@id="root"]/form/div/div[2]/span[4]/span/span/input').send_keys(zipcode)
    print(Fore.WHITE + '[BUY PROCESS] Input zipcode')
    driver.switch_to.default_content()
    print(Fore.WHITE + '[BUY PROCESS] Exited frame')
    driver.find_element_by_xpath('//*[@id="[object Object]"]/div/div/div/div[2]/div[2]/button').click()
    print(Fore.WHITE + '[BUY PROCESS] Sent purchase request')

    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present(),'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.accept()
        print(Fore.RED + "[CARD] Your card was not accepted!")
    except TimeoutException:
        print(Fore.GREEN + "[CARD] Your card was accepted! Your purchase has been complete! Please check the inbox of the email account " + email + " for the product(s)!")
        orderid = driver.find_element_by_xpath('//*[@id="user-product"]/div/div/div/div[2]/div[2]/div/div[1]/span/small')
        print(Fore.WHITE + '[ORDER ID] ' + orderid)