#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta, datetime, time as dtime
import time
import send_email

#import login info
userPwd = {}
with open("loginInfo.txt") as f:
    for line in f:
        (key, val) = line.split()
        userPwd[key] = val

haveRes = False
ctr = 0
loginCtr = 0
haveLogin = False
emailBodList = ["PickeBot Ran!"]

while not haveLogin and loginCtr < 5:
    loginCtr += 1
    try:
        driver = webdriver.Chrome()
        driver.get("https://gtc.clubautomation.com/")
        login = driver.find_element_by_name("login")
        login.clear()
        login.send_keys(userPwd["user"])
        login.send_keys(Keys.TAB)
        # login.send_keys(Keys.TAB)
        pwd = driver.find_element_by_name("password")
        pwd.send_keys(userPwd["pwd"])
        pwd.send_keys(Keys.RETURN)
        haveLogin = True
        emailBodList.append("Login successful on try "+str(loginCtr) + " at " + str(datetime.now().time()))
    except:
        driver.close()
        time.sleep(5)

#have now separated the login process




while not haveRes and ctr < 10:
    ctr += 1
    try:
        '''driver = webdriver.Chrome()
        driver.get("https://gtc.clubautomation.com/")
        login = driver.find_element_by_name("login")
        login.clear()
        login.send_keys(userPwd["user"])
        login.send_keys(Keys.TAB)
        #login.send_keys(Keys.TAB)
        pwd = driver.find_element_by_name("pass")
        pwd.send_keys(userPwd["pwd"])
        pwd.send_keys(Keys.RETURN)'''

        #click through to reservations
        driver.find_element_by_link_text("Reserve a Court").click()

        #click on each div maybe?


        #populate the form, may need to click elements to trigger the javascript

        #date first makes it easier
        bookDate = date.today() + timedelta(days=8)
        testDate = "10/13/2021"
        wait = WebDriverWait(driver, 10)
        dateBox = wait.until(EC.element_to_be_clickable((By.ID, 'date')))
        dateBox.clear()
        dateBox.send_keys(bookDate.strftime("%m/%d/%Y"))
        #dateBox.send_keys(testDate)
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

        time.sleep(1)
        # wait until after 12:30
        while (datetime.now().time() < dtime(12, 30)):
            time.sleep(0.5)
        subButton = driver.find_element_by_xpath("//button[@id='reserve-court-search']")
        subButton.click()
        emailBodList.append("attempt " + str(ctr) + " made at " + str(datetime.now().time()))

        #go = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'td-blue')))
        time.sleep(0.5)
        times = driver.find_elements_by_xpath("//td[@class='td-blue']/a")
        if bookDate.weekday() == 6: #booking on Sunday
            desired_times = ["10:00am", "11:00am", "10:30am"]
        elif bookDate.weekday() == 4: #booking on Friday
            desired_times = ["3:00pm", "2:00pm", "1:00pm"]
        else:
            desired_times = ["10:00am", "11:00am", "10:30am"]
        if times:
            print("times available round " + str(ctr))
            emailBodList.append("times available round " + str(ctr))
            for d in desired_times:
                if haveRes:
                    break
                for t in times:
                    print(t.text)
                    emailBodList.append(t.text)
                    if t.text == d:
                        t.click()
                        time.sleep(0.5)
                        driver.find_element_by_xpath("//button[@id='confirm']").click()
                        haveRes = True
                        #time.sleep(2)
                        break
        else:
            print("no times available " + str(ctr))
            emailBodList.append("no times available " + str(ctr))


    except:
        print("something went wrong with attempt " + str(ctr))
        emailBodList.append("something went wrong with attempt " + str(ctr))
    finally:
        time.sleep(10)


driver.quit()
send_email.sendMail(['jmmarkman@gmail.com'],'PickleBot Ran',"\n".join(emailBodList))




#dateBox.clear()
#dateBox.send_keys(dummyDate)




#Select(box2).select_by_visible_text("Pickleball / Mini Tennis")
#driver.close()