# pyshadow
Selenium plugin to manage multi level shadow DOM elements on web page.

[![Build Status](https://travis-ci.com/sukgu/pyshadow.svg?branch=master)](https://travis-ci.com/sukgu/pyshadow "Travis CI")
[![codecov](https://codecov.io/gh/sukgu/pyshadow/branch/master/graph/badge.svg)](https://codecov.io/gh/sukgu/pyshadow)
[![PyPI version shields.io](https://img.shields.io/pypi/v/pyshadow.svg)](https://pypi.python.org/pypi/pyshadow)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Shadow DOM:
Shadow DOM is a web standard that offers component style and markup encapsulation. It is a critically important piece of the Web Components story as it ensures that a component will work in any environment even if other CSS or JavaScript is at play on the page.

## Custom HTML Tags:
Custom HTML tags can't be directly identified with selenium tools. Using this plugin you can handle any custom HTML tags.

## Problem Statement:
- You have already developed your web-based automation framework in java selenium. Your frontend application uses Polymer that uses shadow dom. Selenium doesn't provide any way to deal with shadow-dom elements.
- Your application page contains custom HTML tags that can't be identified directly using selenium.

## Solution:
You can use this plugin by adding jar file or by including maven dependency in your java selenium project.

## How it works:

## Methods:
  `find_element(str css_selector)` : use this method if want single element from DOM

  `find_elements(str css_selector)` : use this if you want to find all elements from DOM
  
  `find_element(object parent, str css_selector)` : use this if you want to find a single elements from parent object DOM
  
  `find_elements(object parent, str css_selector)` : use this if you want to find all elements from parent object DOM
  
  `set_implicit_wait(int seconds)` : use this method for implicit wait
    
  `set_explicit_wait(int seconds, int polling_time) raise Exception` : use this method for explicit wait
  
  `get_shadow_element(object parent,str css_selector)` : use this if you want to find a single element from parent DOM
  
  `get_all_shadow_element(object parent, str css_selector)` : use this if you want to find all elements from parent DOM
  
  `get_parent_element(object element)` : use this to get the parent element if web element.
  
  `get_child_elements(object parent)` : use this to get all the child elements of parent element.
  
  `get_sibling_elements(object element)` : use this to get all adjacent (sibling) elements.
  
  `get_sibling_element(object element, str css_selector)` : use this to get adjacent(sibling) element using css selector.
  
  `get_next_sibling_element(object element)` : use this to get next adjacent(sibling) element.
  
  `get_previous_sibling_element(object element)` : use this to get previous adjacent(sibling) element..
  
  `is_visible(object element)` : use this if you want to find visibility of element
  
  `is_checked(object element)` : use this if you want to check if checkbox is selected 
  
  `is_disabled(object element)` : use this if you want to check if element is disabled
  
  `get_attribute(object element, str attribute)` : use this if you want to get attribute like aria-selected and other custom attributes of elements.
  
  `select_checkbox(str label)` : use this to select checkbox element using label.
  
  `select_checkbox(object parent, str label)` : use this to select checkbox element using label.
  
  `select_radio(str label)` : use this to select radio element using label.
  
  `select_radio(object parent, str label)` : use this to select radio element from parent DOM using label.
  
  `select_dropdown(str label)` : use this to select dropdown list item using label (use this if only one dropdown is present or loaded on UI).
  
  `select_dropdown(object parent, str label)` : use this to select dropdown list item from parent DOM using label.
  
  `scroll_to(object element)` : use this to scroll to web element.
  
###### How to use this plugin:
  You will have to install this plugin from PyPi.
  
  **Maven**
  ```
  pip install pyshadow
  ```
  
## Selector:
  ###### Examples: 
  for html tag ``` <paper-tab title="Settings"> ```
  You can use this code in your framework to grab the paper-tab element Object.
  ```python
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
shadow = Shadow(driver)
element = shadow.find_element("paper-tab[title='Settings']")
elements = shadow.find_elements("paper-tab[title='Settings']")
text = element.text
  ```
  for html tag that resides under a shadow-root dom element ``` <input title="The name of the employee"> ```
  You can use this code in your framework to grab the paper-tab element Object.
  ```python
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
shadow = Shadow(driver)
element = shadow.find_element("input[title='The name of the employee']")
text = element.text
  ```
  for html tag that resides under a shadow-root dom element 
  ```html 
<properties-page id="settingsPage"> 
    <textarea id="textarea">
</properties-page>
  ```
  You can use this code in your framework to grab the textarea element Object.
  ```python
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
shadow = Shadow(driver)
element = shadow.find_element("properties-page#settingsPage>textarea#textarea")
text = element.text
  ```
  
  ## Wait: Implicit and Explicit
If you want to use wait to synchronize your scripts then you should use the implicit or explicit wait feature.

* For Implicit wait, you can use **shadow.set_implicit_wait(int seconds)** method.
* For Explicit wait, you can use **shadow.set_explicit_wait(int seconds, int pollingTime)** method.

* In Implicit wait, the driver will wait for at least n seconds as set in **shadow.set_implicit_wait(n)**.
* In Explicit wait, the driver will wait for at max n seconds as set in **shadow.set_implicit_wait(n,m)**. In between driver will check for presence of WebElement every m seconds.
  
  ###### Note: > is used to combine multi level dom structure. So you can combine 5 levels of dom. If you want some more level modify the script and ready to rock.
  
  **Documentation** [Link](https://github.com/sukgu/pyshadow/wiki)
  
