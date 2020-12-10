from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

import pandas as pd

def click(wd):
  try:
    element = WebDriverWait(wd, 10).until(
            lambda wd: wd.find_element_by_class_name("""select2-selection__rendered"""))
    print("element",element)
    element.click()
  except:
    print("fail click")
    return None

def fillIn(wd,inputText):
  try:
    search = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.XPATH, """/html/body/span/span/span[1]/input"""))
    )
    
  finally:
    search.send_keys(inputText)
    search.send_keys(Keys.RETURN)

def getText(wd):
    try:
        element = WebDriverWait(wd, 10).until(
            lambda wd: wd.find_element_by_class_name("""select2-selection__rendered"""))
        print("element",element)

        return element.text
    except:
        print("fail")
        return None

browser = webdriver.Chrome(executable_path = 'chromedriver.exe')
browser.get('https://diemthi.vnexpress.net/')
browser.execute_script("window.open()")
window_after = browser.window_handles[1]
browser.switch_to_window(window_after)
browser.get('https://www.google.com/maps/@9.779349,105.6189045,11z?hl=vi-VN')
window_before = browser.window_handles[0]
browser.switch_to_window(window_before)
time.sleep(3)


df = pd.DataFrame(columns = ['Region', 'Name',"Latitude","Longitude"])

for i in range(1,65):
  
  click(browser)
  if i < 10:
    fillIn(browser,"0"+str(i))
  else:
    fillIn(browser,str(i))
  des = getText(browser)
  des = des.split ("-")[1]
  
  url = 'https://maps.google.com/?q=' + des
  browser.switch_to_window(window_after)
  browser.get(url)
  time.sleep(3)

  element = browser.find_element_by_css_selector("head")
  element = WebDriverWait(browser, 10).until(
          EC.presence_of_element_located((By.XPATH, """/html/head/meta[8]"""))
      )
  url = element.get_attribute('content')
  
  for string in url.split("="):
    if "zoom" in string:
      coor = string

  temp_coor = ""
  

  for c in coor:
    if c.isdigit() or c == ".":
      temp_coor += c
    else:
      temp_coor += "!"

  count = 0
  for el in temp_coor.split("!"):
    if len(el) > 3:
      if count == 0:
        lang = el
        count += 1
      else:
        longi = el
        break
  data = [{"Region":i,"Name":des,"Latitude":lang,"Longitude":longi}]
  df_temp = pd.DataFrame(data)
  df = pd.concat([df,df_temp], axis = 0)
  print(df)
  browser.switch_to_window(window_before)


df.to_csv("..//Data//Coordinate.csv",encoding='utf-8-sig')



