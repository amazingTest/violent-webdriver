from selenium import webdriver
from selenium.common.exceptions import WebDriverException, InvalidElementStateException
from selenium.webdriver.common.touch_actions import TouchActions
import time
import warnings
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


class violent_chromedriver(webdriver.Chrome):

    """
    Controls the violent ChromeDriver and allows you to drive the browser.

    """
    def __init__(self, executable_path="chromedriver", port=0, use_mobile_emulation=False,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=Options()):
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

    def v_click(self, locate_rule, attempt_num=60, attempt_interval=0.5, use_double_click=False):

        """
           Post-packaging the [click] function of selenium webdriver
           this function can ignore the exceptions while clicking(tap if use mobile emulation)
           and it will keep clicking(taping if use mobile emulation) until the click operation
           succeed or the attempt_num has been using up

           :Args:
            - attempt_num <int>- the num of click you want to attempt, default num is 60
            - attempt_interval <int>- the time interval of each attempt in second, default interval is 0.5s
            - locate_rule <dict> - the rule that use to locate the web element you want to operate
            - use_double_click <boolean> - whether use double click

                for single-locate strategy , support : [id] , [xpath] , [link text] [partial link text]
                                                      [name] , [tag name] , [class name] [css selector]
                           eg {'id': 'some_id'} , {'xpath': 'some_xpath'} , {'name': 'some_name'}
                           ,  {'class name': 'some_class_name'}

                for multi-locate strategy , support : [one_of_eight_locate_method -> text] ,
                                                     [one_of_eight_locate_method -> attribute]

                           eg {'tag name': 'span', 'text': 'login'}
                             {'tag name': 'input', 'placeholder': 'only num'}
                             {'class name': 'c-tips-container', 'text': 'login'}
                             {'class name': 's_form', 'placeholder': 'only num'}

        """

        if locate_rule.items().__len__() == 1:
            for key, value in locate_rule.items():
                for i in range(0, attempt_num):
                    try:
                        if self.use_mobile_emulation:
                            if use_double_click:
                                TouchActions(self).double_tap(self.find_element(key, value)).perform()
                            else:
                                TouchActions(self).tap(self.find_element(key, value)).perform()
                        else:
                            if use_double_click:
                                ActionChains(self).double_click(self.find_element(key, value)).perform()
                            else:
                                self.find_element(key, value).click()
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
        if locate_rule.items().__len__() == 2:
            key_list = []
            for key in locate_rule.keys():
                key_list.append(key)
            if key_list[1] == 'text':
                for i in range(0, attempt_num):
                    try:
                        elements = self.find_elements(key_list[0], locate_rule[key_list[0]])
                        i = 0
                        for element in elements:
                            if element.text == locate_rule[key_list[1]]:
                                if self.use_mobile_emulation:
                                    if use_double_click:
                                        TouchActions(self).double_tap(element).perform()
                                    else:
                                        TouchActions(self).tap(element).perform()
                                else:
                                    if use_double_click:
                                        ActionChains(self).double_click(element).perform()
                                    else:
                                        element.click()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
            else:
                for i in range(0, attempt_num):
                    try:
                        elements = self.find_elements(key_list[0], locate_rule[key_list[0]])
                        i = 0
                        for element in elements:
                            if element.get_attribute(key_list[1]) == locate_rule[key_list[1]]:
                                if self.use_mobile_emulation:
                                    if use_double_click:
                                        TouchActions(self).double_tap(element).perform()
                                    else:
                                        TouchActions(self).tap(element).perform()
                                else:
                                    if use_double_click:
                                        ActionChains(self).double_click(element).perform()
                                    else:
                                        element.click()
                                i += 1
                                break
                        if i == 0:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue

    def v_send_keys(self, locate_rule, message, attempt_num=60, attempt_interval=0.5, use_clear_before=True):

        """
               Post-packaging the [send_keys] function of selenium webdriver
               this function can ignore the exceptions while sending keys
               and it will keep sending until the operation
               succeed or the attempt_num has been using up

               :Args:
                - message(string)- the message that you want to send
                - attempt_num (int)- the num of click you want to attempt, default num is 60
                - attempt_interval (int)- the time interval of each attempt in second, default interval is 0.5 second
                - locate_rule (dict) - the rule that use to locate the web element you want to operate

                    for single-locate strategy , support : [id] , [xpath] , [link text] [partial link text]
                                                          [name] , [tag name] , [class name] [css selector]
                               eg {'id': 'some_id'} , {'xpath': 'some_xpath'} , {'name': 'some_name'}
                               ,  {'class name': 'some_class_name'}

                    for multi-locate strategy , support : [one_of_eight_locate_method -> text] ,
                                                         [one_of_eight_locate_method -> attribute]

                               eg {'tag name': 'span', 'text': 'login'}
                                 {'tag name': 'input', 'placeholder': 'only num'}
                                 {'class name': 'c-tips-container', 'text': 'login'}
                                 {'class name': 's_form', 'placeholder': 'only num'}
        """

        if locate_rule.items().__len__() == 1:
            for key, value in locate_rule.items():
                for i in range(0, attempt_num):
                    try:
                        self.find_element(key, value).clear() if use_clear_before else None
                    except WebDriverException:
                        pass
                    try:
                        if not self.find_element(key, value).get_attribute('value').strip() == '':
                            time.sleep(attempt_interval)
                    except BaseException:
                        continue
                    try:
                        self.find_element(key, value).send_keys(message)
                        if not self.find_element(key, value).get_attribute('value') == message:
                            continue
                        break
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
        if locate_rule.items().__len__() == 2:
            key_list = []
            for key in locate_rule.keys():
                key_list.append(key)
            for i in range(0, attempt_num):
                try:
                    elements = self.find_elements(key_list[0], locate_rule[key_list[0]])
                    i = 0
                    for element in elements:
                        if element.get_attribute(key_list[1]) == locate_rule[key_list[1]]:
                            try:
                                element.clear() if use_clear_before else None
                            except WebDriverException:
                                pass
                            if not element.get_attribute('value').strip() == '':
                                time.sleep(attempt_interval)
                                break
                            element.send_keys(message)
                            if not element.get_attribute('value') == message:
                                pass
                            else:
                                i += 1
                            break
                    if i == 0:
                        continue
                    break
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue

    def v_get_text(self, locate_rule, attempt_num=60, attempt_interval=0.5, ignore_text_list=None):

        """
        Post-packaging the [text] function , this function will keep getting text until the text is not empty
        or the attempt_num has been using up , while there is no more attempt , this function may return a empty
        text

        :param locate_rule:  rule that locate the web element <dict>
        :param attempt_num:  num of attempt to get text until get a non empty text , default is 60 <int>
        :param attempt_interval:  interval of attempt in sec , default is 0.5 sec <int>
        :param ignore_text_list: if text is in this list, it will ignore it(not return it) and continue attempting <list>
        :return: the text of the web element find by locate_rule, default is '' <string>

        """
        if ignore_text_list is None:
            ignore_text_list = []
        if locate_rule.items().__len__() == 1:
            for key, value in locate_rule.items():
                for i in range(0, attempt_num + 1):
                    if i == attempt_num:
                        return ''
                    try:
                        text = self.find_element(key, value).text
                        if not text.strip() == '' and text.strip() not in ignore_text_list:
                            return text
                        else:
                            continue
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
        if locate_rule.items().__len__() == 2:
            key_list = []
            for key in locate_rule.keys():
                key_list.append(key)
            for i in range(0, attempt_num + 1):
                if i == attempt_num:
                    return ''
                try:
                    elements = self.find_elements(key_list[0], locate_rule[key_list[0]])
                    for element in elements:
                        if element.get_attribute(key_list[1]) == locate_rule[key_list[1]]:
                            text = element.text
                            if not text.strip() == '' and text.strip() not in ignore_text_list:
                                return text
                            else:
                                raise WebDriverException
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue

    def v_get_attribute(self, locate_rule, attribute, attempt_num=60, attempt_interval=0.5, ignore_attribute_list=None):

        if ignore_attribute_list is None:
            ignore_attribute_list = []
        if locate_rule.items().__len__() == 1:
            for key, value in locate_rule.items():
                for i in range(0, attempt_num + 1):
                    if i == attempt_num:
                        return ''
                    try:
                        attribute = self.find_element(key, value).get_attribute(attribute)
                        if not attribute.strip() == '' and attribute.strip() not in ignore_attribute_list:
                            return attribute
                        else:
                            continue
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
        if locate_rule.items().__len__() == 2:
            key_list = []
            for key in locate_rule.keys():
                key_list.append(key)
            for i in range(0, attempt_num + 1):
                if i == attempt_num:
                    return ''
                try:
                    elements = self.find_elements(key_list[0], locate_rule[key_list[0]])
                    for element in elements:
                        if element.get_attribute(key_list[1]) == locate_rule[key_list[1]]:
                            attribute = element.get_attribute(attribute)
                            if not attribute.strip() == '' and text.strip() not in ignore_attribute_list:
                                return attribute
                            else:
                                raise WebDriverException
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue

    def v_get_value(self, locate_rule, attempt_num=60, attempt_interval=0.5, ignore_text_list=None):

        """
        Post-packaging the [get_attribute('value')] function , this function will keep getting value until the value is
        not empty or the attempt_num has been using up , while there is no more attempt , this function may return
        a empty value

        :param locate_rule:  rule that locate the web element <dict>
        :param attempt_num:  num of attempt to get text until get a non empty text , default is 60 <int>
        :param attempt_interval:  interval of attempt in sec , default is 0.5 sec <int>
        :param ignore_text_list: if text is in this list, it will ignore it(not return it) and continue attempting <list>
        :return: the value of the web element find by locate_rule, default is '' <string>

        """
        if ignore_text_list is None:
            ignore_text_list = []
        if locate_rule.items().__len__() == 1:
            for key, value in locate_rule.items():
                for i in range(0, attempt_num + 1):
                    if i == attempt_num:
                        return ''
                    try:
                        text = self.find_element(key, value).get_attribute('value')
                        if not text.strip() == '' and text.strip() not in ignore_text_list:
                            return text
                        else:
                            continue
                    except WebDriverException:
                        time.sleep(attempt_interval)
                        continue
        if locate_rule.items().__len__() == 2:
            key_list = []
            for key in locate_rule.keys():
                key_list.append(key)
            for i in range(0, attempt_num + 1):
                if i == attempt_num:
                    return ''
                try:
                    elements = self.find_elements(key_list[0], locate_rule[key_list[0]])
                    for element in elements:
                        if element.get_attribute(key_list[1]) == locate_rule[key_list[1]]:
                            text = element.get_attribute('value')
                            if not text.strip() == '' and text.strip() not in ignore_text_list:
                                return text
                            else:
                                raise WebDriverException
                except WebDriverException:
                    time.sleep(attempt_interval)
                    continue

    def is_page_refreshed(self, trigger, wait_time=60, detect_interval=0.5):

        """
        to see whether the web page refreshed in certain time

        :param trigger: the web element that ONLY!!! exist in the last page and it is clickable <webelement>
        :param wait_time: the time(in sec) that wait until the page refreshed, default is 60 <int>
        :param detect_interval: time interval that detect whether page is refreshed
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
                time.sleep(detect_interval)
        except WebDriverException:
            is_refreshed = True
            print("Page refresh time is:" + str(refresh_time * detect_interval) + " seconds!")
            return is_refreshed
        print("Page didn't refresh in " + str(wait_time * detect_interval) + " seconds!")
        return is_refreshed

    def is_url_changed(self, current_url, wait_time=60, detect_interval=0.5):

        """
        to see whether the url changed in certain time

        :param current_url: current url <str>
        :param wait_time: the time(in sec) that wait until the url changed, default is 60 <int>
        :param detect_interval: time interval that detect whether url is changed
        :return: True if url is changed in wait_time ,
                  False if url is not changed in wait_time
        """

        changed_time = 0
        is_changed = False
        for i in range(0, wait_time):
            if not str(self.current_url) == str(current_url):
                is_changed = True
                print("Url changed time is:" + str(changed_time * detect_interval) + " seconds!")
                return is_changed
            changed_time = i
            time.sleep(detect_interval)
        if not is_changed:
            print("Url didn't changed in " + str(wait_time * detect_interval) + " seconds!")
            return is_changed

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
            print("window didn't open in " + str(wait_time) + " seconds!")
            return is_opened

