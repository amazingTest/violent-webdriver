from violent_webdriver import Chrome

# the value of executable_path should be your own path
dr = Chrome.violent_chromedriver(executable_path='C://MyDownloads/Download/chrome-win32/chromedriver.exe')
dr.get('https://www.baidu.com')
dr.v_send_keys(locate_rule={'tag name': 'input', 'class': 's_ipt'}, message='test')
dr.v_click(locate_rule={'tag name': 'input', 'value': '百度一下'})
dr.v_click(locate_rule={'tag name': 'em', 'text': 'test'})
print(dr.is_opened_new_window())

# use origin method by contrast

# dr.find_element_by_css_selector('input[class=\'s_ipt\']').send_keys('test')
# dr.find_element_by_css_selector('input[value=\'百度一下\']').click()
# em_list = dr.find_elements_by_tag_name('em')
# for em in em_list:
#     if em.text == 'test':
#         em.click()
#         break


