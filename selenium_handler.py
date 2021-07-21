from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import logging
import traceback
import os, time, random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing as mp

from xpaths import xpaths
SELENIUM_EXE_PATH = xpaths.driver


class SeleniumHandler:
    def __init__(self, **kwargs):
        executable_path = SELENIUM_EXE_PATH
        #if "profile_path" not in kwargs:
        #    raise Exception("Nu a fost furnizat profilul firefox pt acest spider")
        #firefox_profile = webdriver.FirefoxProfile(kwargs["profile_path"])
        options = webdriver.chrome.options.Options()

        if "headless" in kwargs and int(kwargs["headless"]) > 0:
            options.add_argument("--headless")

       # firefox_profile.DEFAULT_PREFERENCES['frozen']['extensions.autoDisableScopes'] = 0
       # firefox_profile.set_preference('extensions.enabledScopes', 15)
       #  self.driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=executable_path,
       #                                  options=options)
        self.driver = webdriver.Chrome(executable_path=executable_path,
                                    options=options)

    def close_driver(self):
        self.driver.quit()

    def wait_for_element(self, awaited_elem_xpath):
        awaited_elem = None
        while (awaited_elem is None or self.__is_element_stale(awaited_elem)):
            try:
                awaited_elem = self.driver.find_element_by_xpath(awaited_elem_xpath)
                with mp.Lock():
                    logging.debug("element appeared")
                return True
            except (NoSuchElementException, StaleElementReferenceException):
                awaited_elem = None
                track = traceback.format_exc()
                with mp.Lock():
                    logging.debug(track)

    def wait_for_at_least_one_element(self, awaited_1_xpath, awaited_2_xpath):
        awaited_1 = None
        awaited_2 = None
        while (awaited_1 is None or self.__is_element_stale(awaited_1)
               or (awaited_2 is None or self.__is_element_stale(awaited_2))):
            try:
                awaited_1 = self.driver.find_element_by_xpath(awaited_1_xpath)
                with mp.Lock():
                    logging.debug("element 1 appeared")
                return "awaited_1"
            except (NoSuchElementException, StaleElementReferenceException):
                awaited_1 = None
                try:
                    awaited_2 = self.driver.find_element_by_xpath(awaited_2_xpath)
                    with mp.Lock():
                        logging.debug("element 2 appeared")
                    return "awaited_2"
                except (NoSuchElementException, StaleElementReferenceException):
                    awaited_2 = None
                    track = traceback.format_exc()
                    with mp.Lock():
                        logging.debug(track)
                track = traceback.format_exc()
                with mp.Lock():
                    logging.debug(track)

    def EC_wait_for_the_visibility_of_element(self, awaited_elem_xpath):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, awaited_elem_xpath))
            )
        except:
            track = traceback.format_exc()
            with mp.Lock():
                logging.debug(track)

    def EC_wait_for_element_to_be_clickable(self, awaited_elem_xpath):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, awaited_elem_xpath))
            )
        except:
            track = traceback.format_exc()
            with mp.Lock():
                logging.debug(track)

    def wait_for_element_by_action(self, awaited_elem_xpath):
        awaited_elem = None
        while (awaited_elem is None or self.__is_element_stale(awaited_elem)):
            try:
                self.press_down()
                # time.sleep(0.2)
                awaited_elem = self.driver.find_element_by_xpath(awaited_elem_xpath)
                with mp.Lock():
                    logging.debug("element appeared")
                return awaited_elem
            except (NoSuchElementException, StaleElementReferenceException):
                awaited_elem = None
                track = traceback.format_exc()
                with mp.Lock():
                    logging.debug(track)

    def __is_element_stale(self, webelement):
        """
        Checks if a webelement is stale.
        @param webelement: A selenium webdriver webelement
        """
        try:
            elem = webelement.tag_name
            with mp.Lock():
                logging.debug(elem)
            return False
        except StaleElementReferenceException:
            return True
        except:
            raise

    def _get_friends_list(self):
        return self.driver.find_elements_by_css_selector(".friendBrowserNameTitle > a")

    def get_friends(self):
        # navigate to "friends" page
        self.driver.find_element_by_css_selector("a#findFriendsNav").click()

        # continuous scroll until no more new friends loaded
        num_of_loaded_friends = len(self._get_friends_list())
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: len(self._get_friends_list()) > num_of_loaded_friends)
                num_of_loaded_friends = len(self._get_friends_list())
            except TimeoutException:
                break  # no more friends loaded

        return [friend.text for friend in self._get_friends_list()]

    def open_tab(self, url="about:blank"):
        js = f"window.open('{url}','_blank');"
        self.driver.execute_script(js)

    def open_tabs(self, href_list):
        for href in href_list:
            self.open_tab(href)
            time.sleep(random.uniform(0.5, 2))

    def download_imgs(self, imgs, folder_path, img_name):
        images_path_list = []
        for img in imgs:
            try:
                # crt_time = time.time()
                img_path = os.path.join(folder_path, f'{img_name}.png')
                images_path_list.append(img_path)
                with open(img_path, 'wb') as file:
                    file.write(img.screenshot_as_png)
                # img_to_idx = {"checksum":"","path":img_path,"url":img.get_attribute('src')}
                # images_list.append(img_to_idx)
            except:
                track = traceback.format_exc()
                with mp.Lock():
                    logging.error(track)
        return images_path_list

    def press_down(self):
        return self.driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)

    def remove_element(self, element):
        try:
            self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
        except:
            track = traceback.format_exc()
            with mp.Lock():
                logging.error(track)

    def scroll_element(self, scrollable_element):
        # scrollable = self.driver.find_element_by_xpath(scrollable_xpath)
        js = '''
            let kill_ID_EVENT = null;
            let scrollable = document.getElementById(arguments[0]);
            let delay_EVENT = 800;
            let MAX_COUNT = 5;
            kill_ID_EVENT = setInterval(() => { 
                if (typeof scrollable === 'undefined') {
                    scrollHeightEventLast = -1;
                    window.clearInterval(kill_ID_EVENT);
                } else {
                    console.log(scrollHeightEventLast + " -- " + scrollable.scrollHeight);
                    let length = document.getElementById(arguments[0]).length;
                    console.log("length --- " + length);
                    LAST_LENGTH = length;
                    if (scrollHeightEventLast === scrollable.scrollHeight && LAST_LENGTH === length) {
                        localCounter++;
                        console.log("localCounter -- " + localCounter);
                        if (localCounter === MAX_COUNT) {
                            LAST_LENGTH = -1;
                            console.log("bottom elem!");
                            scrollHeightEventLast = -1;
                            window.clearInterval(kill_ID_EVENT);
                        }
                    } else {
                        localCounter = 0;
                        scrollHeightEventLast = scrollable.scrollHeight;
                        scrollable.scrollTop = scrollable.scrollHeight;
                    }
                }
            }, delay_EVENT);
            '''
        self.driver.execute_script(js, scrollable_element)

    def move_to_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)