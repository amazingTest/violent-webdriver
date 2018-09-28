from violent_webdriver import Chrome

# the value of executable_path should be your own path
dr = Chrome.violent_chromedriver(executable_path='C://MyDownloads/Download/chrome-win32/chromedriver.exe')
dr.get('https://www.baidu.com')
print('no ignore list:' + dr.v_get_text(locate_rule={'tag name': 'a', 'href': 'http://www.baidu.com/more/'}))
print('add ignore list: ' + dr.v_get_text(locate_rule={'tag name': 'a', 'href': 'http://www.baidu.com/more/'},
                                          ignore_text_list=['更多产品']))
