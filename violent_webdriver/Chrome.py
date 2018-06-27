from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.touch_actions import TouchActions
import time
import warnings
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class violent_chromedriver(webdriver.Chrome):

    """
    Controls the violent ChromeDriver and allows you to drive the browser.

    """
    def __init__(self, executable_path="chromedriver", port=0, use_mobile_emulation=False,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None):
        self.use_mobile_emulation = use_mobile_emulation

        """
           Creates a new instance of the violent chrome driver.

           Starts the service and then creates new instance of chrome driver.

           :Args:
            - executable_path - path to the executable. If the default is used it assumes the executable is in the $PATH
            - port - port you would like the service to run, if left as 0, a free port will be found.
            - desired_capabilities: Dictionary object with non-browser specific
              capabilities only, such as "proxy" or "loggingPref".
            - options: this takes an instance of ChromeOptions
            - use_mobile_emulation: whether use mobile emulation or not , default is False
        """

        if use_mobile_emulation:
            mobile_emulation = {
                "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
            chrome_options = Options()
            chrome_options.add_argument('disable-infobars')
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        if chrome_options:
            warnings.warn('use options instead of chrome_options', DeprecationWarning)
            options = chrome_options

        if options is None:
            # desired_capabilities stays as passed in
            if desired_capabilities is None:
                desired_capabilities = self.create_options().to_capabilities()
        else:
            if desired_capabilities is None:
                desired_capabilities = options.to_capabilities()
            else:
                desired_capabilities.update(options.to_capabilities())

        self.service = Service(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=ChromeRemoteConnection(
                    remote_server_addr=self.service.service_url),
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise
        self._is_remote = False

    def v_click(self, locate_rule, attempt_num=60, attempt_interval=1):

        """
           Post-packaging the [click] function of selenium webdriver
           this function can ignore the exceptions while clicking(tap if use mobile emulation)
           and it will keep clicking(taping if use mobile emulation) until the click operation
           succeed or the attempt_num has been using up

           :Args:
            - attempt_num <int>- the num of click you want to attempt, default num is 60
            - attempt_interval <int>- the time interval of each attempt in second, default interval is 1s
            - locate_rule <two-dimention array> - the rule that use to locate the webelement you want to operate

                for single-locate strategy , support : [id] , [xpath] , [name]
                           eg [['id', 'some_id']] , [['xpath', 'some_xpath']] , [['name', 'some_name']]

                for multi-locate strategy , support : [tag -> text] , [tag -> attribute] ,
                                                      [class -> text] , [class -> attribute]

                           eg [['tag', 'span'], ['text', 'login']]
                              [['tag', 'input'], ['placeholder', 'only num']]
                              [['class', 'c-tips-container'], ['text', 'login']]
                              [['class', 's_form'], ['placeholder', 'only num']]
        """
        if self.use_mobile_emulation:
            if locate_rule[0][0] == 'id':
                for i in range(0, attempt_num):
                    try:
                        TouchActions(self).tap(self.find_element_by_id(locate_rule[0][1])).perform()
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'xpath':
                for i in range(0, attempt_num):
                    try:
                        TouchActions(self).tap(self.find_element_by_xpath(locate_rule[0][1])).perform()
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'name':
                for i in range(0, attempt_num):
                    try:
                        TouchActions(self).tap(self.find_element_by_name(locate_rule[0][1])).perform()
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'tag' and locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        tag_list = self.find_elements_by_tag_name(locate_rule[0][1])
                        i = 0
                        for tag in tag_list:
                            if tag.text == locate_rule[1][1]:
                                TouchActions(self).tap(tag).perform()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'tag' and not locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        tag_list = self.find_elements_by_tag_name(locate_rule[0][1])
                        i = 0
                        for tag in tag_list:
                            if tag.get_attribute(locate_rule[1][0]) == locate_rule[1][1]:
                                TouchActions(self).tap(tag).perform()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'class' and locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        div_list = self.find_elements_by_class_name(locate_rule[0][1])
                        i = 0
                        for div in div_list:
                            if div.text == locate_rule[1][1]:
                                TouchActions(self).tap(div).perform()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'class' and not locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        div_list = self.find_elements_by_class_name(locate_rule[0][1])
                        i = 0
                        for div in div_list:
                            if div.get_attribute(locate_rule[1][0]) == locate_rule[1][1]:
                                TouchActions(self).tap(div).perform()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
        if not self.use_mobile_emulation:
            if locate_rule[0][0] == 'id':
                for i in range(0, attempt_num):
                    try:
                        self.find_element_by_id(locate_rule[0][1]).click()
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'xpath':
                for i in range(0, attempt_num):
                    try:
                        self.find_element_by_xpath(locate_rule[0][1]).click()
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'name':
                for i in range(0, attempt_num):
                    try:
                        self.find_element_by_name(locate_rule[0][1]).click()
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'tag' and locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        tag_list = self.find_elements_by_tag_name(locate_rule[0][1])
                        i = 0
                        for tag in tag_list:
                            if tag.text == locate_rule[1][1]:
                                tag.click()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'tag' and not locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        tag_list = self.find_elements_by_tag_name(locate_rule[0][1])
                        i = 0
                        for tag in tag_list:
                            if tag.get_attribute(locate_rule[1][0]) == locate_rule[1][1]:
                                tag.click()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'class' and locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        div_list = self.find_elements_by_class_name(locate_rule[0][1])
                        i = 0
                        for div in div_list:
                            if div.text == locate_rule[1][1]:
                                div.click()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            if locate_rule[0][0] == 'class' and not locate_rule[1][0] == 'text':
                for i in range(0, attempt_num):
                    try:
                        div_list = self.find_elements_by_class_name(locate_rule[0][1])
                        i = 0
                        for div in div_list:
                            if div.get_attribute(locate_rule[1][0]) == locate_rule[1][1]:
                                div.click()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue

    def v_send_keys(self, locate_rule, message, attempt_num=60, attempt_interval=1):

        """
               Post-packaging the [send_keys] function of selenium webdriver
               this function can ignore the exceptions while sending keys
               and it will keep sending until the operation
               succeed or the attempt_num has been using up

               :Args:
                - message(string)- the message that you want to send
                - attempt_num (int)- the num of click you want to attempt, default num is 60
                - attempt_interval (int)- the time interval of each attempt in second, default interval is 1 second
                - locate_rule (two-dimention array) - the rule that use to locate the webelement you want to operate

                    for single-locate strategy , support : [id] , [xpath] , [name]
                               eg [['id', 'some_id']] , [['xpath', 'some_xpath']] , [['name', 'some_name']]

                    for multi-locate strategy , support : [tag -> text] , [tag -> attribute] ,
                                                          [class -> text] , [class -> attribute]

                               eg [['tag', 'span'], ['text', 'login']]
                                  [['tag', 'input'], ['placeholder', 'only num']]
                                  [['class', 'c-tips-container'], ['text', 'login']]
                                  [['class', 's_form'], ['placeholder', 'only num']]
        """

        if locate_rule[0][0] == 'id':
            for i in range(0, attempt_num):
                try:
                    self.find_element_by_id(locate_rule[0][1]).clear()
                    if not self.find_element_by_id(locate_rule[0][1]).get_attribute('value').strip() == '':
                        time.sleep(attempt_interval)
                        continue
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
                try:
                    self.find_element_by_id(locate_rule[0][1]).send_keys(message)
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'xpath':
            for i in range(0, attempt_num):
                try:
                    self.find_element_by_xpath(locate_rule[0][1]).clear()
                    if not self.find_element_by_xpath(locate_rule[0][1]).get_attribute('value').strip() == '':
                        time.sleep(attempt_interval)
                        continue
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
                try:
                    self.find_element_by_xpath(locate_rule[0][1]).send_keys(message)
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'name':
            for i in range(0, attempt_num):
                try:
                    self.find_element_by_name(locate_rule[0][1]).clear()
                    if not self.find_element_by_name(locate_rule[0][1]).get_attribute('value').strip() == '':
                        time.sleep(attempt_interval)
                        continue
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
                try:
                    self.find_element_by_name(locate_rule[0][1]).send_keys(message)
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'tag' and locate_rule[1][0] == 'text':
            for i in range(0, attempt_num):
                try:
                    tag_list = self.find_elements_by_tag_name(locate_rule[0][1])
                    i = 0
                    for tag in tag_list:
                        if tag.text == locate_rule[1][1]:
                            tag.clear()
                            if not tag.get_attribute('value').strip() == '':
                                time.sleep(attempt_interval)
                                break
                            tag.send_keys(message)
                            i += 1
                            break
                    if i == 0:
                        continue
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'tag' and not locate_rule[1][0] == 'text':
            for i in range(0, attempt_num):
                try:
                    tag_list = self.find_elements_by_tag_name(locate_rule[0][1])
                    i = 0
                    for tag in tag_list:
                        if tag.get_attribute(locate_rule[1][0]) == locate_rule[1][1]:
                            tag.clear()
                            if not tag.get_attribute('value').strip() == '':
                                time.sleep(attempt_interval)
                                break
                            tag.send_keys(message)
                            i += 1
                            break
                    if i == 0:
                        continue
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'class' and locate_rule[1][0] == 'text':
            for i in range(0, attempt_num):
                try:
                    div_list = self.find_elements_by_class_name(locate_rule[0][1])
                    i = 0
                    for div in div_list:
                        if div.text == locate_rule[1][1]:
                            div.clear()
                            if not div.get_attribute('value').strip() == '':
                                time.sleep(attempt_interval)
                                break
                            div.send_keys(message)
                            i += 1
                            break
                    if i == 0:
                        continue
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'class' and not locate_rule[1][0] == 'text':
            for i in range(0, attempt_num):
                try:
                    div_list = self.find_elements_by_class_name(locate_rule[0][1])
                    i = 0
                    for div in div_list:
                        if div.get_attribute(locate_rule[1][0]) == locate_rule[1][1]:
                            div.clear()
                            if not div.get_attribute('value').strip() == '':
                                time.sleep(attempt_interval)
                                break
                            div.send_keys(message)
                            i += 1
                            break
                    if i == 0:
                        continue
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue

    def v_get_text(self, locate_rule, attempt_num=60, attempt_interval=1):
        """
        Post-packaging the [.text] function , this function will keep getting text until the text is not empty
        or the attempt_num has been using up , while there is no more attempt , this function may return a empty
        text

        :param locate_rule:  rule that locate the web element <two-dimension-array>
        :param attempt_num:  num of attempt to get text until get a non empty text  <int>
        :param attempt_interval:  interval of attempt in sec <int>
        :return: the text of the web element find by locate_rule <string>
        """
        if locate_rule[0][0] == 'id':
            for i in range(0, attempt_num):
                try:
                    text = self.find_element_by_id(locate_rule[0][1]).text
                    if not text.strip() == '':
                        return text
                    else:
                        continue
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'xpath':
            for i in range(0, attempt_num):
                try:
                    text = self.find_element_by_xpath(locate_rule[0][1]).text
                    if not text.strip() == '':
                        return text
                    else:
                        continue
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'name':
            for i in range(0, attempt_num):
                try:
                    text = self.find_element_by_name(locate_rule[0][1]).text
                    if not text.strip() == '':
                        return text
                    else:
                        continue
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'tag' and not locate_rule[1][0] == 'text':
            for i in range(0, attempt_num):
                try:
                    tag_list = self.find_elements_by_tag_name(locate_rule[0][1])
                    for tag in tag_list:
                        if tag.get_attribute(locate_rule[1][0]) == locate_rule[1][1]:
                            text = tag.text
                            if not text.strip() == '':
                                return text
                            else:
                                raise WebDriverException
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue
        if locate_rule[0][0] == 'class' and not locate_rule[1][0] == 'text':
            for i in range(0, attempt_num):
                try:
                    div_list = self.find_elements_by_class_name(locate_rule[0][1])
                    for div in div_list:
                        text = div.text
                        if not text.strip() == '':
                            return text
                        else:
                            raise WebDriverException
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue


    def is_page_refreshed(self, trigger, wait_time=60):
        """
        to see whether the web page refreshed in certain time

        :param trigger: the web element that ONLY!!! exist in the last page and it is clickable <webelement>
        :param wait_time: the time(in sec) that wait until the page refreshed, default is 60 <int>
        :return: True if page is refreshed in wait_time ,
                  False if page is not refreshed in wait_time
        """

        global refresh_time
        global is_refreshed
        try:
            is_refreshed = False
            for i in range(0, wait_time):
                refresh_time = i
                if self.use_mobile_emulation:
                    TouchActions(self).tap(trigger).perform()
                else:
                    trigger.click()
                time.sleep(1)
        except WebDriverException:
            is_refreshed = True
            print("Page refresh time is:" + str(refresh_time) + " seconds!")
            return is_refreshed
        print("Page didn't refresh in 60 seconds!")
        return is_refreshed

    def is_opened_new_window(self, wait_time=60):
        """
        to see whether new window opened in certain time

        :param wait_time: the time(in sec) that wait until the page refreshed, default is 60 <int>
        :return: True if new window is opened in wait_time ,
                  False if new window is not opened in wait_time
        """
        is_opened = False
        open_time = 0
        for i in range(0, wait_time):
            handles = self.window_handles
            if handles.__len__() > 1:
                is_opened = True
                print("Open new window time is:" + str(open_time) + " seconds!")
                return is_opened
            open_time = i
            time.sleep(1)
        if not is_opened:
            print("window didn't open in 60 seconds!")
            return is_opened
