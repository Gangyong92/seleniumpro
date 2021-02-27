from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://repl.it/login")

github_page = browser.find_element_by_xpath(
    '//*[@id="page"]/div[2]/div[1]/div[1]/a[2]'
)
github_page.click()
# github login인 할때 다른 탭에 열려서 switch 해줘야 함.
browser.switch_to_window(browser.window_handles[1])

username_input = browser.find_element_by_xpath(
    "/html/body/div[3]/main/div/div[3]/form/input[2]"
)
password_input = browser.find_element_by_xpath(
    "/html/body/div[3]/main/div/div[3]/form/input[3]"
)
login_btn = browser.find_element_by_xpath(
    "/html/body/div[3]/main/div/div[3]/form/input[14]"
)

# github에 올릴거라 비워둠.
username_input.send_keys(input("What is your username?"))
password_input.send_keys(input("What is your password?"))
login_btn.click()

