from selenium import webdriver
import time
from selenium.webdriver import ActionChains
browser=webdriver.Firefox()
browser.get('https://www.taobao.com')
input=browser.find_element_by_xpath('//*[@id="q"]')
input.send_keys('Iphone')
input.send_keys('Iphone')
print(input.size)
button=browser.find_element_by_class_name('btn-search')
button.click()