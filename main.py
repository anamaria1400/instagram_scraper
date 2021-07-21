import itertools
import time
from selenium_handler.selenium_handler import SeleniumHandler
from xpaths import xpaths
from selenium.webdriver.common.keys import Keys
from explicit import waiter, XPATH

selenium_handler_instance = SeleniumHandler()

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
        time.sleep(5)

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
        time.sleep(2)
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
        btn_followers = selenium_handler_instance.wait_for_element(xpaths.followers)
        if (btn_followers == True):
            selenium_handler_instance.driver.find_element_by_xpath(xpaths.followers).click()
            print("Open all friends")
        else:
            print("Eroare open all friends")
        time.sleep(5)

        # scoatem lista cu numele prietenilor


        time.sleep(2)

        # get followers count
        followers_count = 25

        while True:
            selenium_handler_instance.driver.execute_script('''
                        var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                        fDialog.scrollTop = fDialog.scrollHeight
                    ''')
            list_of_followers = selenium_handler_instance.driver.find_elements_by_xpath('//div[@class="PZuss"]/li/div / div / div[2] / div / span / a')
            list_of_followers_count = len(list_of_followers)
            if list_of_followers_count == followers_count:
                break

        new_list_of_followers = []
        for i in list_of_followers:
            new_list_of_followers.append(i.text)
            print(i.text)

        break
    except ValueError:
        print("failed")

    finally:
        if time.perf_counter() > 1000:
            print("verifica conexiunea")
        else:
            print("Conectare reusita")
