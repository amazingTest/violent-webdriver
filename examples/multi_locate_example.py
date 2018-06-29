from violent_webdriver import Chrome

# the value of executable_path should be your own path
dr = Chrome.violent_chromedriver(executable_path='C://MyDownloads/Download/chrome-win32/chromedriver.exe')
dr.get('https://www.baidu.com')
dr.v_send_keys(locate_rule={'tag name': 'input', 'class': 's_ipt'}, message='test')
dr.v_click(locate_rule={'tag name': 'input', 'value': '百度一下'})
