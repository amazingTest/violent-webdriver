from violent_webdriver import Chrome

# the value of executable_path should be your own path
dr = Chrome.violent_chromedriver(executable_path='C://MyDownloads/Download/chrome-win32/chromedriver.exe')
dr.get('https://www.baidu.com')
dr.implicitly_wait(30)
trigger = dr.find_element_by_name('tj_trtieba')
dr.v_send_keys(locate_rule={'tag': 'input', 'class': 's_ipt'}, message='test')
dr.v_click(locate_rule={'tag': 'input', 'value': '百度一下'})
print(dr.is_page_refreshed(trigger))
