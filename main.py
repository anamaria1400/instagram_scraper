import time

from model_es import model_es
from selenium_handler.selenium_handler import SeleniumHandler
from xpaths import xpaths
from selenium.webdriver.common.keys import Keys
import json
from model_es import *

selenium_handler_instance = SeleniumHandler()

dictionary_followers = {
    "cont": [],
    "link": [],
    "name": []
}
dictionary_following = {
    "cont": [],
    "link": [],
    "name": []
}

def scrape_list(nr):
    fBody = selenium_handler_instance.driver.find_element_by_xpath(xpaths.b_1)
    scroll = 0
    while scroll < 50:  # scroll 50 times
        selenium_handler_instance.driver.execute_script(xpaths.b_2, fBody)
        time.sleep(2)
        scroll += 1
        fList = selenium_handler_instance.driver.find_elements_by_xpath(xpaths.b_3)
        if len(fList) == nr:
            break

def open_page(x):
    btn = selenium_handler_instance.wait_for_element(x)
    if (btn == True):
        selenium_handler_instance.driver.find_element_by_xpath(x).click()
        print("Open all followers")
    else:
        print("Eroare open all followers")
    time.sleep(2)

while True:
    try:
        # se deschide pagina
        selenium_handler_instance.driver.get(xpaths.pagina)
        print("Opened facebook")

        # se accepta cookie-urile
        btn_accept_cookies = selenium_handler_instance.wait_for_element(xpaths.accept_cookie)
        if(btn_accept_cookies == True):
            selenium_handler_instance.driver.find_element_by_xpath(xpaths.accept_cookie).click()
            print("S-au acceptat cookie")
        else:
            print("problema buton cookie")
        time.sleep(3)

        # conectarea cu un cont Instagram
        username_box = selenium_handler_instance.driver.find_element_by_name('username')
        username_box.send_keys(xpaths.usr)
        print("Username entered")

        password_box = selenium_handler_instance.driver.find_element_by_name('password')
        password_box.send_keys(xpaths.parola)
        print("Password entered")
        time.sleep(2)
        password_box.send_keys(Keys.ENTER)

        # login info + notif
        btn_login_info = selenium_handler_instance.wait_for_element(xpaths.info)
        if (btn_login_info == True):
            selenium_handler_instance.driver.find_element_by_xpath(xpaths.info).click()
        btn_notif = selenium_handler_instance.wait_for_element(xpaths.info)
        if (btn_notif == True):
            selenium_handler_instance.driver.find_element_by_xpath(xpaths.info).click()
        time.sleep(2)

        #search
        search_box = selenium_handler_instance.driver.find_element_by_xpath(xpaths.search)
        search_box.send_keys(xpaths.caut)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        search_box.send_keys(Keys.ENTER)

        #deschidem lista de urmaritori
        open_page(xpaths.followers)
        #incarcam toata lista
        scrape_list(xpaths.nr_urmaritori)

        # contul + link
        cont = selenium_handler_instance.driver.find_elements_by_xpath(xpaths.cont)

        # numele
        nume = selenium_handler_instance.driver.find_elements_by_xpath(xpaths.nume)

        for i in cont:
            dictionary_followers["cont"].append(i.text)
            dictionary_followers["link"].append(i.get_attribute('href'))

        for i in nume:
            dictionary_followers["name"].append(i.text)

        selenium_handler_instance.driver.find_element_by_xpath(xpaths.button_x).click()

        # deschidem lista de urmariti
        open_page(xpaths.following)
        #incarcam lista
        scrape_list(xpaths.nr_urmariti)

        # contul + link
        cont = selenium_handler_instance.driver.find_elements_by_xpath(xpaths.cont)

        # numele
        nume = selenium_handler_instance.driver.find_elements_by_xpath(xpaths.nume)

        for i in cont:
            dictionary_following["cont"].append(i.text)
            dictionary_following["link"].append(i.get_attribute('href'))

        for i in nume:
            dictionary_following["name"].append(i.text)

        selenium_handler_instance.close_driver()

        print("\n\n--------------------------DICTIONARY---------------------------\n\n")
        print(dictionary_followers)
        print(dictionary_following)

        a = json.dumps(dictionary_followers, indent=5)
        print(a)
        b = json.dumps(dictionary_followers, indent=5)
        print(b)

        # with open("urmaritori.json", "w") as outfile:
        #     json.dump(dictionary_followers, outfile, indent=5)
        model_es.send_json_to_es(dictionary_followers)


        # with open("urmariti.json", "w") as outfile:
        #     json.dump(dictionary_following, outfile, indent=5)
        model_es.send_json_to_es(dictionary_following)

        break

    except ValueError:
        print("failed")

    finally:
        if time.perf_counter() > 1000:
            print("verifica conexiunea")
        else:
            print("Conectare reusita")
