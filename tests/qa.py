import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
from pyshadow.main import Shadow

driver.get("http://staging-app.frevvo.com/")
driver.maximize_window()
shadow = Shadow(driver)
title = driver.title
print(title)
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_id("login-button").click()
time.sleep(6)
driver.find_element_by_xpath("//div[@class='_hj-widget-container _hj-widget-theme-dark']/div/div/button/span").click()
driver.find_element_by_xpath("//div[@id='center-content']/ul/a[4]").click()
driver.find_element_by_xpath("//*[@id='project-new-menu']/div/paper-listbox/a[2]/paper-icon-item").click()
shadow.set_implicit_wait(3)
time.sleep(3)
shadow.find_element("frevvo-ui-wizard-dialog#workflow-wizard>frevvo-ui-workflow-wizard>frevvo-ui-project-action-screen#project-action-screen>div#projectTypeScreen>paper-button.select-button.button").click()
shadow.set_implicit_wait(1)
time.sleep(3)
shadow.find_element("frevvo-ui-wizard-dialog#workflow-wizard>frevvo-ui-workflow-wizard>paper-input-container#container>iron-input.input-element>input").send_keys("NewProject1")

def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("border: 2px solid red;")
    time.sleep(5)
    apply_style(original_style)

time.sleep(1)
shadow.find_element("frevvo-ui-wizard-dialog#workflow-wizard>paper-button#nextButton").click()
shadow.find_element("frevvo-ui-wizard-dialog#workflow-wizard>frevvo-ui-workflow-wizard>iron-input#input-4>input").send_keys("Workflow1")
shadow.find_element("frevvo-ui-wizard-dialog#workflow-wizard>paper-button#nextButton").click()
k = shadow.find_element("frevvo-ui-wizard-dialog#workflow-wizard>paper-icon-button#add-steps-icon>iron-icon#icon")
time.sleep(2)
k.click()

elm = shadow.find_elements("frevvo-ui-wizard-dialog#workflow-wizard>paper-button")

highlight(elm[0])
elm[0].click()
