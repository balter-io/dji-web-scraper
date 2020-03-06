#!/usr/bin/env python3
""" A Python program that scrapes the DJI website looking for an updated version of the Phantom 4 User Manual.
Currently only tested and working on Linux.

Usage:

    pip install -r requirements.txt

    Download the Chrome webdriver for your current version of Chrome.

    Create 'published_date.txt' within your source directory.

    Create a config.py file and save the following variables:
        - source_directory = 'location_on_your_computer'
        - text_file = 'published_date.txt'
        - maintenance_manual_location = 'the_location_to_save_the_new_user_manual'
        - chrome_webdriver = '/usr/local/bin/chromedriver'

    python main.py
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config


def main():
    """ Navigates to the DJI website and checks the current date of the published manual, then compares the date to
    your current manual. If the dates are different, the program will scrape the new date and download the new manual.
    """

    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': config.maintenance_manual_location,  # default downloads dir
        'plugins.always_open_pdf_externally': True
    })  # download pdf instead of opening it

    driver = webdriver.Chrome(executable_path=config.chrome_webdriver,
                              chrome_options=chrome_options)    # sets chrome as the webdriver

    with open('published_date.txt', 'r') as old_date:

        for line in old_date.readlines():

            published_date = line.strip('\n')

        driver.get('https://www.dji.com/au/phantom-4/info#downloads')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="modal-discontinue"]/div/div/div[1]/button').click()

        element_date = driver.find_element_by_xpath('//*[@id="phantom-4-download"]'
                                                    '/div/div[1]/ul[1]/li[2]/div[1]/div[2]')
        current_date = element_date.text

        if published_date != current_date:
            print(f'Collecting new manual version....')
            driver.find_element_by_xpath('//*[@id="phantom-4-download"]/div/div[1]/ul[1]/li[2]/div[2]/div/a').click()

            time.sleep(7)
            driver.close()

            os.remove(config.text_file)

            with open('published_date.txt', 'w') as new_date:
                new_date.write(current_date)
                print('Your Phantom 4 User Manual is now up-to-date.')
                print()
        else:
            print(f'Your Phantom 4 User Manual is already up-to-date.')
            print()


if __name__ == '__main__':
    main()
