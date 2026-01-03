import unittest
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import time


class TestShadowFeatures(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--allow-file-access-from-files")
        ChromeDriverManager().install()
        self.driver = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()

    def test_shadow_object_not_none(self):
        shadow = Shadow(self.driver)
        assert shadow is not None

    def test_shadow(self):
        self.driver.get(TestShadowFeatures.get_page_location("index.html"))
        shadow = Shadow(self.driver)
        shadow.set_explicit_wait(10, 2)
        ele = shadow.find_element("div#container>h2#inside")
        assert ele is not None
        assert ele.text == "Inside Shadow DOM"

    def test_normal_web_element(self):
        self.driver.get(TestShadowFeatures.get_page_location("index.html"))
        shadow = Shadow(self.driver)
        shadow.set_explicit_wait(10, 2)
        ele = shadow.find_element("h3")
        assert ele is not None
        assert ele.text == "some DOM element"

    def test_get_all_shadow_element(self):
        self.driver.get(TestShadowFeatures.get_page_location("index.html"))
        shadow = Shadow(self.driver)
        ele = shadow.find_element("#container")
        ele1 = shadow.find_elements(ele, "inside1111111")
        assert len(ele1) == 0

    def test_find_elements_with_incorrect_selector2levels(self):
        self.driver.get(TestShadowFeatures.get_page_location("index.html"))
        shadow = Shadow(self.driver)
        ele1 = shadow.find_elements("#container>#inside1111111")
        assert len(ele1) == 0

    def test_2(self):
        self.driver.get(TestShadowFeatures.get_page_location("button.html"))
        shadow = Shadow(self.driver)
        ele = shadow.find_elements("button")
        shadow.scroll_to(ele[0])
        assert ele[0] is not None
        ele[0].click()
        time.sleep(2)
        ele1 = shadow.find_element("div#divid>div#node>p")
        child = shadow.get_child_elements(ele1)
        assert child is not None

    def test_3(self):
        self.driver.get(TestShadowFeatures.get_page_location("button.html"))
        shadow = Shadow(self.driver)
        parent = shadow.find_elements("body")
        assert parent is not None
        child = shadow.get_shadow_element(parent[0], "button")
        assert child is not None

    def test_get_element_by_xpath(self):
        self.driver.get(TestShadowFeatures.get_page_location("index.html"))
        shadow = Shadow(self.driver)
        parent = shadow.find_element_by_xpath('//body')
        assert parent is not None

    def test_get_element_by_xpath_with_parent(self):
        self.driver.get(TestShadowFeatures.get_page_location("button.html"))
        shadow = Shadow(self.driver)
        parent = shadow.find_element_by_xpath('//button')
        shadow.scroll_to(parent)
        assert parent is not None
        parent.click()
        time.sleep(2)
        child = shadow.find_element_by_xpath(parent, '//div[@id="divid"]', True)
        sub_child = shadow.find_element_by_xpath(child, '//div[@id="node"]//p', True)
        assert sub_child is not None

    def test_css_with_double_quote_with_single_quote_inside(self):
        self.driver.get(TestShadowFeatures.get_page_location("button.html"))
        shadow = Shadow(self.driver)
        parent = shadow.find_element('body')
        shadow.scroll_to(parent)
        assert parent is not None
        parent.click()
        time.sleep(2)
        child = shadow.find_element(parent, "div[id='divid']", True)
        assert child is not None

    def test_get_elements_by_xpath_with_parent(self):
        self.driver.get(TestShadowFeatures.get_page_location("button.html"))
        shadow = Shadow(self.driver)
        parent = shadow.find_element_by_xpath('//button')
        shadow.scroll_to(parent)
        assert parent is not None
        parent.click()
        time.sleep(2)
        child = shadow.find_element_by_xpath(parent, '//div[@id="divid"]', True)
        sub_child = shadow.find_elements_by_xpath(child, '//div[@id="node"]//p', True)
        assert sub_child.pop(0) is not None

    @staticmethod
    def get_page_location(page_name):
        cwd = os.getcwd()
        #cwd = os.path.dirname(os.path.realpath(__file__))
        print("cwd path is " + cwd)
        test_file_location = os.path.join(cwd, "pyshadow/resources/test", page_name)
        print("test_file_location is "+test_file_location)
        return "file:///"+test_file_location


if __name__ == '__main__':
    unittest.main()
