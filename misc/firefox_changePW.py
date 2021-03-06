from selenium import webdriver
from selenium.webdriver.common.by import By
from macOS.accountLists import connetivityAccounts31_40

current_password = "default" #enter current password here
new_password = "default" #enter new password here

#uncomment account list for changing passwords 
#Accounts = connetivityAccounts01_10
#Accounts = connetivityAccounts11_20
#Accounts = connetivityAccounts21_30
Accounts = connetivityAccounts31_40
#Accounts = developerAccounts01_10
#Accounts = developerAccounts11_20
#Accounts = developerAccounts21_30
#Accounts = developerAccounts31_40
#Accounts = developerAccounts41_50
#Accounts = developerAccounts51_60


for i in Accounts:
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get("https://www2.industrysoftware.automation.siemens.com/webkey/")
    driver.find_element(By.XPATH, "//tr[5]/td[2]/ul/font/li/a/font").click()
    driver.find_element(By.XPATH, "//td[2]/input").click()
    driver.find_element(By.NAME, "WebKey_Username").send_keys(i)
    driver.find_element(By.NAME, "Existing_WebKey_Password").send_keys(current_password)
    driver.find_element(By.NAME, "pass").click()
    driver.find_element(By.NAME, "pass").send_keys(new_password)
    driver.find_element(By.NAME, "repass").click()
    driver.find_element(By.NAME, "repass").send_keys(new_password)
    driver.find_element(By.XPATH, "//div[3]/div[2]/div/form/fieldset/input").click()
    print (i+'   password changed to  ' + new_password)
    driver.close()

print ('password change finished')

