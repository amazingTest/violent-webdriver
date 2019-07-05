from violent_webdriver import Chrome

# the value of executable_path should be your own path
dr = Chrome.violent_chromedriver(executable_path='C://MyDownloads/Download/chrome-win32/chromedriver.exe')
dr.get('https://www.baidu.com')
no_ignored_text = dr.v_get_text(locate_rule={'css selector': 'a[href=\'http://www.baidu.com/more/\']'},
                                attempt_num=10)
has_ignored_text = dr.v_get_text(locate_rule={'css selector': 'a[href=\'http://www.baidu.com/more/\']'},
                                 attempt_num=10,
                                 ignore_text_list=['更多产品'])
print('no ignore list: %s' % no_ignored_text)
print('add ignore list: %s' % has_ignored_text)
# dr.quit()
