from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

page = "https://academy2.eu1.mindsphere.io/index.html#/"
driver = webdriver.Firefox(
    executable_path='webdriver/macOS/geckodriver')

driver.implicitly_wait(3)
# driver.minimize_window()
driver.get(page)

driver.find_element(By.XPATH, "//fieldset[@id='dr_signin']/div[2]/div/input").send_keys('EMAILADDRESS')
time.sleep(1)
driver.find_element(By.XPATH, "//fieldset[@id='dr_signin']/div[3]/div/input").send_keys('CURRENTPASSWORD')
time.sleep(1)
driver.find_element(By.XPATH, "//button[@id='login-button']").click()
time.sleep(3)
driver.find_element(By.XPATH,
                    "//div[@id='_mscontent']/mindsphere-app-root/div/mindsphere-launchpad-container/div/div/div/div[6]/div/mindsphere-launchpad-tile-container/a/div").click()

driver.find_element(By.XPATH, "(//input[@name='user'])[2]").send_keys('EMAILADDRESS')

driver.find_element(By.XPATH, "(//input[@name='password'])[2]").send_keys('NEWPASSWORD')

driver.find_element(By.XPATH, "(//button[@type='submit'])[5]").click()
time.sleep(3)
driver.find_element(By.XPATH, "//div[@id='app']/div/c8y-ui-header/div/div/div[3]/button/span").click()
time.sleep(3)
driver.find_element(By.XPATH, "//div[@id='app']/div/c8y-ui-header/div/div/div[3]/ul/li/a").click()
time.sleep(3)
driver.find_element(By.XPATH, "//div[9]/button/span").click()
time.sleep(3)
