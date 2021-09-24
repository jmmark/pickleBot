#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta
import time

#import login info
userPwd = {}
with open("loginInfo.txt") as f:
    for line in f:
        (key, val) = line.split()
        userPwd[key] = val

haveRes = False
ctr = 0

while not haveRes and ctr < 5:
    ctr += 1
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


    #populate the form, may need to click elements to trigger the javascript

    #date first makes it easier
    bookDate = date.today() + timedelta(days=8)
    testDate = "09/29/2021"
    wait = WebDriverWait(driver, 10)
    dateBox = wait.until(EC.element_to_be_clickable((By.ID, 'date')))
    dateBox.clear()
    #dateBox.send_keys(bookDate.strftime("%m/%d/%Y"))
    dateBox.send_keys(bookDate)
    duration = driver.find_elements_by_xpath('//div[@class="ca-switcher switcher-interval"]/div/*')
    durChosen = "90 Min"
    for d in duration:
        if d.text == durChosen:
            d.click()

    #tennis dropdown is simple
    box1 = driver.find_element_by_id("component")
    #box1.click()
    Select(box1).select_by_visible_text("Tennis")


    #pickleball choice isn't a regular select box
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

    time.sleep(5)
    subButton = driver.find_element_by_xpath("//button[@id='reserve-court-search']")
    subButton.click()

    go = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'td-blue')))
    times = driver.find_elements_by_xpath("//td[@class='td-blue']/a")
    desired_times = ["10:30am", "9:30am", "10:00am"]
    if times:
        for d in desired_times:
            if haveRes:
                break
            for t in times:
                print(t.text)
                if t.text == d:
                    t.click()
                    time.sleep(2)
                    driver.find_element_by_xpath("//button[@id='confirm']").click()
                    haveRes = True
                    break
    else:
        print("no times available " + str(ctr))

    driver.close()
    time.sleep(20)







#dateBox.clear()
#dateBox.send_keys(dummyDate)




#Select(box2).select_by_visible_text("Pickleball / Mini Tennis")
#driver.close()