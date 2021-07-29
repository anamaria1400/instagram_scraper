import time
from selenium_handler.selenium_handler import SeleniumHandler
from xpaths import xpaths
from selenium.webdriver.common.keys import Keys

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
        btn_followers = selenium_handler_instance.wait_for_element(xpaths.followers)
        if (btn_followers == True):
            selenium_handler_instance.driver.find_element_by_xpath(xpaths.followers).click()
            print("Open all followers")
        else:
            print("Eroare open all followers")
        time.sleep(2)

        # scoatem lista cu numele prietenilor
        # get followers count
        followers_count = xpaths.followers

        #selenium_handler_instance.driver.execute_script()

        lenOfPage = selenium_handler_instance.driver.execute_script('''
                        var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                        fDialog.scrollTop = fDialog.scrollHeight
                    ''')
        match = False
        while (match == False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = selenium_handler_instance.driver.execute_script('''
                        var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                        fDialog.scrollTop = fDialog.scrollHeight
                    ''')
            if lastCount == lenOfPage:
                match = True
        list_of_followers = selenium_handler_instance.driver.find_elements_by_xpath('//div[@class="PZuss"]/li/div / div / div[2] / div / span / a')

        #new_list_of_followers = []
        #for i in list_of_followers:
        #    new_list_of_followers.append(i.text)
        #    print(i.text)

        break
    except ValueError:
        print("failed")

    finally:
        if time.perf_counter() > 1000:
            print("verifica conexiunea")
        else:
            print("Conectare reusita")
