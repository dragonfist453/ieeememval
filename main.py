from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.support.ui import WebDriverWait
import requests
import traceback
import pandas as pd
import argparse

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(options=option)

parser = argparse.ArgumentParser()
parser.add_argument('--colname', action='store', type=str, required=True)
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--output', action='store', type=str, default='./output.xlsx')
parser.add_argument('--errors', action='store', type=str, default='./errors.xlsx')
args = parser.parse_args()

try:
    # Navigate to url
    driver.get("https://services20.ieee.org/membership-validator.html")

    print("Enter the following details of the IEEE Execom: ")

    emailID = input("Email ID: ")
    password = input("Password: ")

    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element_by_name("pf.username"))
    driver.find_element_by_name("pf.username").send_keys(emailID + Keys.TAB + password + Keys.ENTER)

    input_df = pd.read_csv(args.input)
    input_df[[args.colname]] = input_df[[args.colname]].fillna(value="12345678")
    output_list = []
    errors_list = []

    for row in input_df.itertuples():
        print(getattr(row, 'Index'), end='')
        ID = getattr(row, args.colname)
        cookies = driver.get_cookies()
        s = requests.Session()
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        r = s.get("https://services20.ieee.org/bin/svc/ieee-webapps/membership-validator.validate-member.json?memberNumber="+ID)
        if(r.json()['success']):
            print(' is good')
            output_list.append(row)
        else:
            print(' is bad')
            errors_list.append(row)
        driver.refresh()
        
    pd.DataFrame(data=output_list).to_excel(args.output)
    pd.DataFrame(data=errors_list).to_excel(args.errors)

except Exception:
    traceback.print_exc()
finally:
    driver.close()