from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC 
import sys,time
from pynput import keyboard
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

rooms = ["5a9ad72f581d6c093735a997c661c507",
        "f43a7cc36ba4b3717b5858a6abe4232f",
        "ed4a3e32343e377c816fc005068e8b7b",
        "70711c8e0b05769ea0ea4a88a67f7790",
        "8998bd3d9d9a9593a14f0916c0602306",
        "dc8da3baddd275ed2967937e772e6c2e"]
"""
/html/body/div[3]/div[3]/div[2]/div[3]/a
/html/body/div[3]/div[3]/div[3]/div[3]/a
/html/body/div[3]/div[3]/div[4]/div[3]/a
...
/html/body/div[3]/div[3]/div[7]/div[3]/a
"""


driver = webdriver.Firefox()
driver.get("http://orkis.skdev.me/play")

name = "a"
room = int(sys.argv[1])

driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[%i]/div[3]/a'%(room+1)).click()
driver.find_element_by_xpath('/html/body/div[3]/div[5]/form/input[3]').click()

inGame = False
canvas = '/html/body/div[1]/div[1]/div/div[2]/canvas'
#actions = ActionChains(driver)

class MyException(Exception): pass

def on_press(key):
    
    global driver
    global inGame

    if key == keyboard.Key.esc:
        raise MyException(key)
    else:
        if key == keyboard.KeyCode.from_char('s'):
            driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[3]/div/input[1]').click()
            print "in game true"
            inGame = True
        print key
        if  not inGame:
            return
        if key == keyboard.Key.up:
            driver.find_element_by_xpath(canvas).send_keys(Keys.ARROW_UP)
            return
        elif key == keyboard.Key.down:
            driver.find_element_by_xpath(canvas).send_keys(Keys.ARROW_DOWN)  
            return
        elif key == keyboard.Key.right:
            driver.find_element_by_xpath(canvas).send_keys(Keys.ARROW_RIGHT)
            return
        elif key == keyboard.Key.left:
            driver.find_element_by_xpath(canvas).send_keys(Keys.ARROW_LEFT)
            return
        elif key == keyboard.Key.space:
            driver.find_element_by_xpath(canvas).send_keys(Keys.SPACE) 
            return
        elif key == keyboard.KeyCode.from_char('q'):
            driver.find_element_by_xpath(canvas).send_keys('q')  
            return
        if key == keyboard.KeyCode.from_char('e'):
            inGame = False
            print "game ended"

# Collect events until released
with keyboard.Listener(
        on_press=on_press) as listener:
    try:
        listener.join()
    except MyException as e:
        print('{0} was pressed'.format(e.args[0]))

