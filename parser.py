from selenium import webdriver
import time
import os
from urllib.parse import urlparse, parse_qs
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# EXECUTABLE PATH FOR PHANTOMJS(HEADLESS BROWSER)
EXE_PHANTOM = os.path.join(BASE_DIR, 'webdrivers/phantomjs')


def get_params(url):
    """Return params from url"""
    return parse_qs(urlparse(url).query)


def get_sel(id, hl):
    """Return results using Selenium + PhantomJs"""
    url = 'https://play.google.com/store/apps/details?id=' + str(id) + '&hl=' + str(hl)
    driver = webdriver.PhantomJS(executable_path=EXE_PHANTOM)
    driver.get(url)
    path = '/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[3]/div/div[2]/div/c-wiz/div/span/div/span/div/a'
    view = driver.find_element_by_xpath(path)
    try:
        driver.execute_script("arguments[0].scrollIntoView();", view)
    except Exception as e:
        # Todo: implement logging functionality
        print(e)
    try:
        driver.execute_script("arguments[0].click()", view)
    except Exception as e:
        # Todo: implement logging functionality
        print(e)

    time.sleep(3)
    detail_path = '/html/body/div[4]/div/div[2]/content/c-wiz/div'
    detail = driver.find_element_by_xpath(detail_path)
    blocks = detail.find_elements_by_xpath('.//ul/..')

    results = {}
    for block in blocks:
        line = block.text.split('\n')
        results[line[0]] = line[1:]

    driver.quit()
    return results

if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser(description="Parse Google Play Store")
    arg_parser.add_argument("-id", "--id", required=True, help="Application ID")
    arg_parser.add_argument("-ln", "--language", help="Language")
    args = vars(arg_parser.parse_args())
    try:
        ln = args["language"]
    except KeyError:
        ln = "en"

    pprint(get_sel(args["id"], ln))
