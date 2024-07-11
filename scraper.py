from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from openpyxl.workbook import Workbook
from webdriver_manager.chrome import ChromeDriverManager

def main(query,n):
    query = query.split()
    query = "+".join(query)
    print(query)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    List = {
        "AdText":[],
        "Advertiser":[],
        "Location":[]
    }
    for i in range(n):
        print(f"Page No: {i+1}")
        if i!=0:
            url = f"https://www.google.com/search?q={query}&start={i}0"
        else:
            url = f"https://www.google.com/search?q={query}&start=0"
        driver.get(url) 
        time.sleep(2)
        adBox = driver.find_elements(By.CLASS_NAME,"uEierd")
        print(len(adBox))
        j = 0
        for ad in adBox:
            adtext = ad.text
            clickable = ad.find_element(By.XPATH,'.//div[@title="Why this ad?" and @aria-label="Why this ad?" and @role="button"]')
            driver.execute_script("arguments[0].click();", clickable)
            time.sleep(2)
            AdvertiserLoc = driver.find_elements(By.CLASS_NAME,"xZhkSd")
            AdvertiserName = AdvertiserLoc[0].text
            Location = AdvertiserLoc[1].text
            List["AdText"].append(adtext)
            List["Advertiser"].append(AdvertiserName)
            List["Location"].append(Location)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            print(f"Completed AdDiv {j+1}")
            j += 1
    driver.quit()
    df = pd.DataFrame(List)
    df.to_excel(f'{query}+Ad+Advertiser.xlsx', index=False)

start = time.time()
main("Properties in thane",10)
print("total time:", time.time() - start)