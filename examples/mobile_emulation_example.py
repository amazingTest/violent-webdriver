from violent_webdriver import Chrome

# the value of executable_path should be your own path
dr = Chrome.violent_chromedriver(executable_path='C://MyDownloads/Download/chrome-win32/chromedriver.exe',
                                 use_mobile_emulation=True)
dr.get('https://www.baidu.com')



