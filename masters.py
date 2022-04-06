import os
import sys
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


ignore_exceptions = (StaleElementReferenceException, TimeoutException)

def table_load(d):
    return d.find_element_by_class_name("table-styled")

def get_results(year):

    driver = webdriver.Chrome()

    url = 'https://www.pgatour.com/tournaments/masters-tournament/past-results.html'
    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(table_load)
        el = driver.find_element_by_id('pastResultsYearSelector')
        for option in el.find_elements_by_tag_name('option')[1:]:
            if int(option.text) == int(year):
                opt = option.text
                option.click()
                time.sleep(2)
                WebDriverWait(driver, 5).until(table_load)
                df = pd.read_html(driver.page_source)[1]
                if not df.empty:
                    filename = f'masters_{opt}.csv'
                    df.to_csv(filename, index=False)
                break
    except ignore_exceptions as e:
        print('exception', e)

    driver.close()

if __name__ == '__main__':
    args = sys.argv
    years = sys.argv[1:]
    for year in years:
        get_results(year)
