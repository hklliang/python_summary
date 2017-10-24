from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time





# a=browser.find_element_by_css_selector('table[onclick*="hta1023i85i"] div[textContent="超豪华房"]')



# js="""
# $('.tbl-room-quote a[title="超豪华房"]').parents('tr').find("table[onclick*='hta1023i85i']").find('div:contains("超豪华房")').first().click()
# """
# # js='window.open("https://www.sogou.com");'
# browser.execute_script(js)



class QunarRate:

    def __init__(self,check_in,check_out,timeout=30):
        self.check_in = check_in
        self.check_out = check_out
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_opt.add_experimental_option("prefs", prefs)
        chrome_opt.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
        self.browser = webdriver.Chrome(chrome_options=chrome_opt)
        self.browser.set_page_load_timeout(timeout)

    def get_rate(self,seq,room_type):
        position = seq.rindex('_')
        city = seq[:position]
        dt = seq[position + 1:]
        url = 'http://hotel.qunar.com/city/{city}/dt-{dt}/?tag={city}#fromDate={check_in}' \
              '&toDate={check_out}'.format(city=city, dt=dt, check_in=self.check_in, check_out=self.check_out)

        try:
            self.browser.get(url)
        except NoSuchElementException as e:
            print(e)

        xpath_str = "//table[contains(@onclick,'hta1023i85i')]//div[text()='{room_style}']".format(
            room_style=room_type)
        try:
            self.browser.find_element_by_xpath(xpath_str).click()
        except NoSuchElementException as e:
            print(e)
            try:
                xpath_str = "//table[contains(@onclick,'hta1023i85i')]"
                self.browser.find_element_by_xpath(xpath_str).click()
            except TimeoutException as e:
                print(e)

        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def __del__(self):
        time.sleep(5)
        self.browser.close()
        self.browser.quit()

if __name__ == '__main__':
    t1=time.time()
    qunarRate=QunarRate(check_in='2017-11-04',check_out='2017-11-05')
    room_list =[('cebu_city_51','超豪华房'),('cebu_city_51','豪华客房'),
                ('cebu_city_51','超豪华房'),('cebu_city_51','豪华客房'),
                ('cebu_city_51', '超豪华房'), ('cebu_city_51', '豪华客房'),
                ('cebu_city_51', '超豪华房'), ('cebu_city_51', '豪华客房'),
                ('cebu_city_51', '超豪华房'), ('cebu_city_51', '豪华客房'),
                ]
    for room in room_list:
        qunarRate.get_rate(*room)

    print(time.time()-t1)
