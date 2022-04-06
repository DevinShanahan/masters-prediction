import os
import sys
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


ignore_exceptions = (StaleElementReferenceException, TimeoutException)

def table_load(d):
    return d.find_element_by_class_name("player-name")

def write_csv(driver, year):
    breadcrumbs = driver.find_element_by_class_name('breadcrumbs')
    _, _, stat_a = breadcrumbs.find_elements_by_tag_name('a')
    stat_name = stat_a.text.replace(' - ', '-').replace(': ', ':').replace(' ', '_')
    stat_path = os.path.join(stat_name)
    if not os.path.exists(stat_path):
        os.mkdir(stat_path)
    df = pd.read_html(driver.page_source)[1].iloc[:, 2:]
    if not df.empty:
        filename = os.path.join(stat_path, str(year)) + '.csv'
        df.to_csv(filename, index=False)

def get_stats(stat, year):
    driver = webdriver.Chrome()
    url = f'https://www.pgatour.com/stats/stat.{stat}'

    if year == datetime.now().year:
        try:
            stat_year = url + '.html'
            driver.get(stat_year)
            time.sleep(5) # time for updated info to load after click
            WebDriverWait(driver, 5).until(table_load)
            write_csv(driver, year)
            driver.close()
        except ignore_exceptions as e:
            print('exception', e)
        return

    if year == datetime.now().year:
        stat_year = url + '.html'
    else:
        stat_year = url + f'.y{year}.html'
    driver.get(stat_year)
    try:
        WebDriverWait(driver, 5).until(table_load)
        el = driver.find_elements_by_class_name('statistics-details-select')[4]
        options = el.find_elements_by_tag_name('option')
        select_next = False
        count = 0
        for i, option in enumerate(options):
            opt_text = option.text
            if select_next: # and count == 4 for 5 tournaments previous
                option.click()
                time.sleep(5) # time for updated info to load after click
                WebDriverWait(driver, 5).until(table_load)
                write_csv(driver, year)
                if year != 2021:
                    break
                select_next = False
                el2 = driver.find_elements_by_class_name('statistics-details-select')[4]
                options2 = el2.find_elements_by_tag_name('option')
                year = 2020
                for option in options2[i:]:
                    opt_text = option.text
                    if select_next:
                        option.click()
                        time.sleep(5) # time for updated info to load after click
                        WebDriverWait(driver, 5).until(table_load)
                        write_csv(driver, year)
                        break
                    elif 'Masters' in opt_text:
                        select_next = True
                        count += 1
                break

            elif 'Masters' in opt_text or year == 2022:
                select_next = True
                count += 1
            elif count:
                count += 1

    except ignore_exceptions as e:
        print('exception', e)

    driver.close()

if __name__ == '__main__':
    args = sys.argv
    year_start, year_end = sys.argv[1:3]
    stats = sys.argv[3:]
    for stat in stats:
        for year in range(int(year_start), int(year_end) + 1):
            get_stats(stat, year)
