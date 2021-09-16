from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

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

#click through to reservations
driver.find_element_by_link_text("Reserve a Court").click()

#click on each div maybe?
boxes = driver.find_elements_by_class_name("ca-element-error-wrapper")
i = 0
for box in boxes:
    i = i + 1
    if (box.text == "Any Location"):
        box.click()

box2 = driver.find_elements_by_xpath("//li[@class='active-result']")
for li in box2:
    #print(li.text)
    if li.text == "Pickleball / Mini Tennis":
        li.click()

#populate the form, may need to click elements to trigger the javascript
box1 = driver.find_element_by_id("component")
#box1.click()
Select(box1).select_by_visible_text("Tennis")



#Select(box2).select_by_visible_text("Pickleball / Mini Tennis")
#driver.close()