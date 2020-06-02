import unittest
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os


class TestShadowFeatures(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--allow-file-access-from-files")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

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

    def test_explicit_wait(self):
        pass

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
