from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.ie.webdriver import WebDriver as InternetExplorerDriver
from selenium.webdriver.remote import webdriver as remote_web_driver
from selenium.webdriver.support.ui import WebDriverWait
from io import StringIO
from multipledispatch import dispatch
import time
import re
import os


class Shadow:
    @staticmethod
    def __convert_js_to_text():
        text = StringIO()
        cwd = os.path.dirname(os.path.realpath(__file__))
        file_location = os.path.join(cwd, "resources", "querySelector.js")
        file = open(file_location, 'r')
        lines = file.readlines()
        for line in lines:
            text.write(line)
        return text.getvalue()

    javascript_library = __convert_js_to_text.__func__()

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
        elif isinstance(driver, remote_web_driver.WebDriver):
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
        if seconds < 0:
            raise Exception("polling time can't be lower than zero")
        self.__explicit_wait = seconds
        self.__polling_time = polling

    def wait_for_page_loaded(self):
        try:
            WebDriverWait(self.driver, 30).until(DocumentIsReady)
        finally:
            pass

    @staticmethod
    def __sanitize_quotes(script):
        regex = r"(')*(')"
        subst = "\""
        new_script, num = re.subn(regex, subst, script)
        return new_script

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
    
    def _get_element_object(self, command, parent=None):
        args = [command]
        if parent:
            args.append(parent)
        if self.__implicit_wait > 0:
            time.sleep(self.__implicit_wait)
            element = self.executor_get_object(*args)

        if self.__explicit_wait > 0:
            start_time = time.time()
            element = None
            while ( time.time() - start_time )  <= self.__explicit_wait and not element:
                time.sleep(self.__polling_time)
                element = self.executor_get_object(*args)

        if self.__implicit_wait == 0 and self.__explicit_wait == 0:
            element = self.executor_get_object(*args)
        return element
        
    def _validate_exception(self, selector, element, force_find=False, elem_type='xpath'):
        if force_find:
            return
        exception = ElementNotVisibleException
        if self.__explicit_wait:
            exception = TimeoutException
        if element is None or (type(element) != list and not self.is_present(element)):
            raise exception(f"Element with {elem_type} {selector} is not present")

    @dispatch(object, str, bool)
    def find_element(self, parent, css_selector, force_find):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getObject('{attr}', arguments[0]);".format(attr=css_selector)
        element = self._get_element_object(command, parent)
        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')        

        return element

    @dispatch(object, str)
    def find_element(self, parent, css_selector, force_find=False):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getObject('{attr}', arguments[0]);".format(attr=css_selector)
        element = self._get_element_object(command, parent)
        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')        

        return element

    @dispatch(str, bool)
    def find_element(self, css_selector, force_find):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getObject('{attr}');".format(attr=css_selector)
        element = self._get_element_object(command)

        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')

        return element


    @dispatch(str)
    def find_element(self, css_selector, force_find=False):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getObject('{attr}');".format(attr=css_selector)
        element = self._get_element_object(command)

        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')

        return element
    

    @dispatch(str, bool)
    def find_elements(self, css_selector, force_find):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getAllObject('{attr}');".format(attr=css_selector)
        element = self._get_element_object(command)

        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')

        return element
    
    @dispatch(str)
    def find_elements(self, css_selector, force_find=False):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getAllObject('{attr}');".format(attr=css_selector)
        element = self._get_element_object(command)

        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')

        return element

    @dispatch(object, str, bool)
    def find_elements(self, parent, css_selector, force_find):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getAllObject('{attr}', arguments[0]);".format(attr=css_selector)
        element = self._get_element_object(command, parent)

        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')

        return element
    
    @dispatch(object, str)
    def find_elements(self, parent, css_selector, force_find=False):
        element = None
        css_selector = self.__sanitize_quotes(css_selector)
        command = "return getAllObject('{attr}', arguments[0]);".format(attr=css_selector)
        element = self._get_element_object(command, parent)

        self._validate_exception(selector=css_selector, element=element, 
                                 force_find=force_find, elem_type='css')

        return element

    @dispatch(str, bool)
    def find_element_by_xpath(self, xpath, force_find):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathObject('{attr}');".format(attr=xpath)
        element = self._get_element_object(command)

        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')

        return element
    
    @dispatch(str)
    def find_element_by_xpath(self, xpath, force_find=False):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathObject('{attr}');".format(attr=xpath)
        element = self._get_element_object(command)

        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')

        return element

    @dispatch(object, str, bool)
    def find_element_by_xpath(self, parent, xpath, force_find):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathObject('{attr}', arguments[0]);".format(attr=xpath)
        element = self._get_element_object(command, parent)

        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')
    
        return element

    @dispatch(object, str)
    def find_element_by_xpath(self, parent, xpath, force_find=False):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathObject('{attr}', arguments[0]);".format(attr=xpath)
        element = self._get_element_object(command, parent)

        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')
    
        return element

    @dispatch(str, bool)
    def find_elements_by_xpath(self, xpath, force_find):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathAllObject('{attr}');".format(attr=xpath)
        element = self._get_element_object(command)
        
        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')
        
        return element
    
    @dispatch(str)
    def find_elements_by_xpath(self, xpath, force_find=False):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathAllObject('{attr}');".format(attr=xpath)
        element = self._get_element_object(command)
        
        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')
        
        return element

    @dispatch(object, str)
    def find_elements_by_xpath(self, parent, xpath, force_find):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathAllObject('{attr}', arguments[0]);".format(attr=xpath)
        element = self._get_element_object(command, parent)

        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')
        
        return element
    
    @dispatch(object, str, bool)
    def find_elements_by_xpath(self, parent, xpath, force_find=False):
        element = None
        xpath = self.__sanitize_quotes(xpath)
        command = "return getXPathAllObject('{attr}', arguments[0]);".format(attr=xpath)
        element = self._get_element_object(command, parent)

        self._validate_exception(selector=xpath, element=element, 
                                 force_find=force_find, elem_type='xpath')
        
        return element

    def get_attribute(self, element, attribute):
        command = "return arguments[0].getAttribute('{attr}');".format(attr=attribute)
        return self.executor_get_object(command, element)

    def get_shadow_element(self, element, selector):
        selector = self.__sanitize_quotes(selector)
        command = "return getShadowElement(arguments[0], '{attr}');".format(attr=selector)
        return self.executor_get_object(command, element)

    def get_all_shadow_element(self, element, selector):
        selector = self.__sanitize_quotes(selector)
        command = "return getAllShadowElement(arguments[0], '{attr}');".format(attr=selector)
        return self.executor_get_object(command, element)

    def get_parent_element(self, element):
        command = "return getParentElement(arguments[0]);"
        return self.executor_get_object(command, element)

    def get_child_elements(self, element):
        command = "return getChildElements(arguments[0]);"
        return self.executor_get_object(command, element)

    def get_all_sibling_element(self, element, selector):
        selector = self.__sanitize_quotes(selector)
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

    @dispatch(str)
    def select_dropdown(self, label):
        command = "return selectDropdown('{attr}');".format(attr=label)
        return self.executor_get_object(command)

    @dispatch(object, str)
    def select_dropdown(self, parent, label):
        command = "return selectDropdown('{attr}',arguments[0]);".format(attr=label)
        return self.executor_get_object(command, parent)

    def scroll_to(self, element):
        command = "return scrollTo(arguments[0]);"
        return self.executor_get_object(command, element)

    def highlight(self, element, color="red", time_in_mili_seconds=4000):
        border = "3"
        original_style = element.get_attribute("style")
        style = "border: {border}px solid {color};".format(border=border, color=color)
        self.driver.execute_script("arguments[0].setAttribute('style', '{attr}');".format(attr=style), element)
        time.sleep(time_in_mili_seconds)
        self.driver.execute_script("arguments[0].setAttribute('style', '{attr}');".format(attr=original_style), element)


class DocumentIsReady:
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, driver):
        try:
            ready = driver.execute_script("return document.readyState;") == "complete"
            return ready
        finally:
            pass
