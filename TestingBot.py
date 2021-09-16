from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#import login info
userPwd = {}
with open("loginInfo.txt") as f:
    for line in f:
        (key, val) = line.split()
        userPwd[key] = val


driver = webdriver.Chrome()
driver.get("https://gtc.clubautomation.com/")
login = driver.find_element_by_name("login")
login.clear()
login.send_keys(userPwd["user"])
login.send_keys(Keys.TAB)
#login.send_keys(Keys.TAB)
pwd = driver.find_element_by_name("pass")
pwd.send_keys(userPwd["pwd"])
pwd.send_keys(Keys.RETURN)
#driver.close()