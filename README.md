# violent-webdriver

violent-webdriver is created by post-packaging selenium webdriver,  violent-webdriver has many convinient functions
which can highly insure the browser operation, you don't need to worry about whether the element is really present
on current page or clickable at specific time while using violent-webdriver. it will handle this sort
of annoying problems

violent-webdriver 诞生于二次封装 selenium webdriver，内部封装了许多方法来确保浏览器操作的执行性，你不需要去担心定位到的元素是否存在
于当前页面或者是否在当前时刻处于可点击状态，报错重试机制可以帮你自动解决这些不必要的麻烦。


Find the latest version on github : https://github.com/amazingTest/violent-webdriver


## Installation
The last stable release is available on PyPI and can be installed with pip.
**make sure that Chrome has been installed and match the selenium version** 

    $ pip install selenium

    $ pip install violent-webdriver

## Best Practice
Firstly, create a python file: c:\folder\mytest.py

    # c:\folder\mytest.py
    from violent_webdriver import Chrome

    dr = Chrome.violent_chromedriver(executable_path=[CHROMEDRIVER_PATH], use_mobile_emulation=True)
    dr.get('http://www.baidu.com')
    dr.v_send_keys(locate_rule={'css selector': 'input[name=\'word\']'}, message='test')
    dr.v_click(locate_rule={'css selector': 'button[class=\'se-bn\']'})

then use your IDE to run this script or

    $ python c:\folder\mytest.py

if successful, you will see the search result of 'test' by a mobile emulated browser

For more code examples, please refer to the examples folder in source distribution or
visit https://github.com/amazingTest/violent-webdriver/tree/master/examples

## Contact me
For information and suggestions you can contact me at 523314409@qq.com

Finally, if you really find this lib useful，**donation** is welcome by using your phone to scann the two-dimensional 
code below
 
最后，如果你觉得这个库真的好用的话可以扫码给作者一些鼓励哦~

![image](https://github.com/amazingTest/violent-webdriver/blob/master/images/wechatDonation.jpg)


