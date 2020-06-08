from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.ie.webdriver import WebDriver as InternetExplorerDriver
from selenium.webdriver.remote import webdriver as remote_web_driver
from selenium.webdriver.support.ui import WebDriverWait
from io import StringIO
from multipledispatch import dispatch
import time
import os


class Shadow:
    @staticmethod
    def convert_js_to_text():
        text = StringIO()
        cwd = os.path.dirname(os.path.realpath(__file__))
        file_location = os.path.join(cwd, "resources", "querySelector.js")
        file = open(file_location, 'r')
        lines = file.readlines()
        for line in lines:
            text.write(line)
        return text.getvalue()

    javascript_library = convert_js_to_text.__func__()

    def __init__(self, driver):
        if isinstance(driver, ChromeDriver):
            self.session_id = driver.session_id
            self.chrome_driver = driver
        elif isinstance(driver, FirefoxDriver):
            self.session_id = driver.session_id
            self.firefox_driver = driver
        elif isinstance(driver, InternetExplorerDriver):
            self.session_id = driver.session_id
            self.ie_driver = driver
        elif isinstance(driver, remote_web_driver):
            self.session_id = driver.session_id
            self.remote_driver = driver
        self.driver = driver
        self.exception = WebDriverException()
        self.__implicit_wait = 0
        self.__explicit_wait = 0
        self.__polling_time = 1

    def set_implicit_wait(self, seconds):
        if seconds > 0:
            self.__implicit_wait = seconds

    def set_explicit_wait(self, seconds, polling):
        if seconds <= polling and not seconds < 0:
            raise Exception("polling time can't be greater than wait time")
        if seconds > 0:
            self.__explicit_wait = seconds
            self.__polling_time = polling

    def wait_for_page_loaded(self):
        try:
            WebDriverWait(self.driver, 30).until(DocumentIsReady)
        finally:
            pass

    @dispatch(str)
    def inject_shadow_executor(self, javascript):
        self.wait_for_page_loaded()
        return self.driver.execute_script(javascript)

    @dispatch(str, object)
    def inject_shadow_executor(self, javascript, element):
        self.wait_for_page_loaded()
        return self.driver.execute_script(javascript, element)

    @dispatch(str)
    def executor_get_object(self, script):
        javascript = Shadow.javascript_library
        javascript += script
        return self.inject_shadow_executor(javascript)

    @dispatch(str, object)
    def executor_get_object(self, script, element):
        javascript = Shadow.javascript_library
        javascript += script
        return self.inject_shadow_executor(javascript, element)

    @dispatch(str)
    def find_element(self, css_selector):
        element = None
        command = "return getObject('{attr}');".format(attr=css_selector)
        if self.__implicit_wait > 0:
            time.sleep(self.__implicit_wait)
            element = self.executor_get_object(command)

        if self.__explicit_wait > 0:
            element = self.executor_get_object(command)
            count = 0
            while count < self.__explicit_wait and element is None:
                time.sleep(self.__polling_time)
                element = self.executor_get_object(command)
                count = count + 1

        if self.__implicit_wait == 0 and self.__implicit_wait == 0:
            element = self.executor_get_object(command)

        if element is None or self.is_present(element) is False:
            raise ElementNotVisibleException("Element with CSS " + css_selector + " is not present on screen")

        return element

    @dispatch(object, str)
    def find_element(self, parent, css_selector):
        element = None
        command = "return getObject('{attr}', arguments[0]);".format(attr=css_selector)
        if self.__implicit_wait > 0:
            print(element)
            time.sleep(self.__implicit_wait)
            element = self.executor_get_object(command, parent)

        if self.__explicit_wait > 0:
            element = self.executor_get_object(command, parent)
            print(element)
            count = 0
            while count < self.__explicit_wait and element is None:
                time.sleep(self.__polling_time)
                element = self.executor_get_object(command, parent)
                count = count + 1

        if self.__implicit_wait == 0 and self.__implicit_wait == 0:
            element = self.executor_get_object(command, parent)

        if element is None or self.is_present(element) is False:
            raise ElementNotVisibleException("Element with CSS " + css_selector + " is not present on screen")

        return element

    @dispatch(str)
    def find_elements(self, css_selector):
        element = None
        command = "return getAllObject('{attr}');".format(attr=css_selector)
        if self.__implicit_wait > 0:
            time.sleep(self.__implicit_wait)
            element = self.executor_get_object(command)

        if self.__explicit_wait > 0:
            element = self.executor_get_object(command)
            count = 0
            while count < self.__explicit_wait and element is None:
                time.sleep(self.__polling_time)
                element = self.executor_get_object(command)
                count = count + 1

        if self.__implicit_wait == 0 and self.__implicit_wait == 0:
            element = self.executor_get_object(command)

        if element is None:
            raise ElementNotVisibleException("Element with CSS " + css_selector + " is not present on screen")

        return element

    @dispatch(object, str)
    def find_elements(self, parent, css_selector):
        element = None
        command = "return getAllObject('{attr}', arguments[0]);".format(attr=css_selector)
        if self.__implicit_wait > 0:
            print(element)
            time.sleep(self.__implicit_wait)
            element = self.executor_get_object(command, parent)

        if self.__explicit_wait > 0:
            element = self.executor_get_object(command, parent)
            print(element)
            count = 0
            while count < self.__explicit_wait and element is None:
                time.sleep(self.__polling_time)
                element = self.executor_get_object(command, parent)
                count = count + 1

        if self.__implicit_wait == 0 and self.__implicit_wait == 0:
            element = self.executor_get_object(command, parent)

        if element is None:
            raise ElementNotVisibleException("Element with CSS " + css_selector + " is not present on screen")

        return element

    def get_attribute(self, element, attribute):
        command = "return arguments[0].getAttribute('{attr}');".format(attr=attribute)
        print(command)
        return self.executor_get_object(command, element)

    def get_shadow_element(self, element, selector):
        command = "return getShadowElement(arguments[0], '{attr}');".format(attr=selector)
        return self.executor_get_object(command, element)

    def get_all_shadow_element(self, element, selector):
        command = "return getAllShadowElement(arguments[0], '{attr}');".format(attr=selector)
        return self.executor_get_object(command, element)

    def get_parent_element(self, element):
        command = "return getParentElement(arguments[0]);"
        return self.executor_get_object(command, element)

    def get_child_elements(self, element):
        command = "return getChildElements(arguments[0]);"
        return self.executor_get_object(command, element)

    def get_all_sibling_element(self, element, selector):
        command = "return getSiblingElements(arguments[0], '{attr}');".format(attr=selector)
        return self.executor_get_object(command, element)

    def get_sibling_element(self, element):
        command = "return getSiblingElement(arguments[0]);"
        return self.executor_get_object(command, element)

    def get_next_sibling_element(self, element):
        command = "return getNextSiblingElement(arguments[0]);"
        return self.executor_get_object(command, element)

    def get_previous_sibling_element(self, element):
        command = "return getNextSiblingElement(arguments[0]);"
        return self.executor_get_object(command, element)

    def is_checked(self, element):
        command = "return isChecked(arguments[0]);"
        return self.executor_get_object(command, element)

    def is_disabled(self, element):
        command = "return isDisabled(arguments[0]);"
        return self.executor_get_object(command, element)

    def is_visible(self, element):
        command = "return isVisible(arguments[0]);"
        return self.executor_get_object(command, element)

    def is_present(self, element):
        present = self.executor_get_object("return isVisible(arguments[0]);", element)
        print("QA--QAQA "+ str(present))
        return present

    @dispatch(str)
    def select_checkbox(self, label):
        command = "return selectCheckbox('{attr}');".format(attr=label)
        return self.executor_get_object(command)

    @dispatch(object, str)
    def select_checkbox(self, parent, label):
        command = "return selectCheckbox('{attr}',arguments[0]);".format(attr=label)
        return self.executor_get_object(command, parent)

    @dispatch(str)
    def select_radio(self, label):
        command = "return selectRadio('{attr}');".format(attr=label)
        return self.executor_get_object(command)

    @dispatch(object, str)
    def select_radio(self, parent, label):
        command = "return selectRadio('{attr}',arguments[0]);".format(attr=label)
        return self.executor_get_object(command, parent)

    def scroll_to(self, element):
        command = "return scrollTo(arguments[0]);"
        return self.executor_get_object(command, element)


class DocumentIsReady:
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, driver):
        try:
            ready = driver.execute_script("return document.readyState;") == "complete"
            return ready
        finally:
            pass
