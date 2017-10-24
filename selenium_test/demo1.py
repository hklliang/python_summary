from selenium import webdriver
browser=webdriver.Chrome()
browser.get('http://www.baidu.com')
print(browser.current_url)
print(browser.title)
ele=browser.find_element_by_id('kw')
#find_element_by_name name属性
# browser.find_element_by_class_name()
# browser.find_element_by_tag_name()
#browser.maximize_window()窗口最大化
# ele.send_keys('hello')
map=browser.find_element_by_link_text('地图')#text
browser.find_element_by_partial_link_text('地')

map.click()
print(map)
# browser.back()
