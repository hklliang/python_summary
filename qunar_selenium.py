from selenium import webdriver
import time
from scrapy.selector import Selector
chromedriver = r"E:\pkfare\testselenium\chromedriver.exe"
chrome_opt=webdriver.ChromeOptions()
prefs={"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs",prefs)
chrome_opt.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')

cookie_dict={'name':'JSESSIONID','value':'DB12ADD8EAC1C55DB55A42BBAEA25C44'}

browser=webdriver.Chrome(chromedriver,chrome_options=chrome_opt)

# url='http://hotel.qunar.com/city/singapore_city/dt-1790/?_=1#tag=singapore_city&fromDate=2017-05-11&toDate=2017-05-12&q=&from=globalhotelpages&fromFocusList=0&filterid=dc144154-9087-424e-8421-f2418c9cd687_A&showMap=0&qptype=&QHFP=ZSS_A1924EF5&cityurl=singapore_city&HotelSEQ=singapore_city_1790&rnd=1493198736702&sgroup=-1&roomNum=1'
url='http://hotel.qunar.com/city/cebu_city/dt-51/?tag=cebu_city#fromDate=2017-11-04&toDate=2017-11-05&from=globalhotelsearch&showMap=0&QHFP=GHL__6700B46'
# browser.set_page_load_timeout(12)

try:
    browser.get(url)

except Exception as e:
    print(e)

# browser.add_cookie(cookie_dict)
#
# browser.find_element_by_xpath('//div[@class="more-room-wraper-ct"]/a').click()
#
# t_selector=Selector(text=browser.page_source)
#
# room_types = t_selector.xpath('//div[contains(@class,"room-item-wrapper")]')
# handles=browser.window_handles

browser.find_element_by_xpath("//table[contains(@onclick,'hta1023i85i')]//div[contains(text(), '超豪华房')]").click()


# js="""
# $('.tbl-room-quote a[title="超豪华房"]').parents('tr').find("table[onclick*='hta1023i85i']").find('div:contains("超豪华房")').first().click()
# """
# # js='window.open("https://www.sogou.com");'
# browser.execute_script(js)

print(browser.current_url)
#关闭窗口
browser.close()
print(browser.window_handles)
#切换窗口
browser.switch_to.window(browser.window_handles[0])



# print(browser.close())

browser.get(url)
browser.find_element_by_xpath("//table[contains(@onclick,'hta1023i85i')]//div[contains(text(), '超豪华房')]").click()
# browser.get(url)
#
# for handle in handles:# 切换窗口（切换到搜狗）
#     if handle!=browser.current_window_handle:
#         print('switch to ',handle)
#         browser.switch_to_window(handle)
#         print(browser.current_window_handle) # 输出当前窗口句柄（搜狗）
#         break
# browser.get('http://www.baidu.com')
# for room_type in room_types:
#     suppliers = room_type.xpath('div//div[contains(@class,"room-type-default")]')
#     room_type_name=room_type.xpath('div//div[@class="rtype"]/h2/a/text()').extract_first()
#     for supplier in suppliers:
#         supplier_name = supplier.xpath('table/tbody/tr/td[@class="e1 js-logo"]/div/img/@alt').extract_first()
#         supplier_room_type = supplier.xpath('table/tbody/tr/td[@class="e2"]/div/div/text()').extract_first()
#         supplier_room_breadfast = supplier.xpath('table/tbody/tr/td[@class="e4"]/p/text()').extract_first()
#         supplier_room_privacy = supplier.xpath('table/tbody/tr/td[@class="e5"]/div/em/text()').extract_first()
#
#         supplier_room_price = supplier.xpath('table//span[@class="sprice"]').xpath('string(.)').extract_first()
#         print(room_type_name,supplier_name, supplier_room_type, supplier_room_breadfast, supplier_room_privacy,
#               supplier_room_price)# tbodys=t_selector.xpath('//div[@class="agent-pic js-logo-img"]')


# browser.quit()
# print(address)`