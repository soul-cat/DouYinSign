# DouYinSign
web版抖音采集的一种解决方案，通过这种方法生成的签名可以百分百拿到数据。

# 目的

> 批量采集抖音数据

# 原理

> 通过Flask搭建起一个Web服务，在里面维护一个Selenium进程，让抖音网页帮我们生成_signature签名

# 获取浏览器ua

> http://service.spiritsoft.cn/ua.html

# 坑点

> 抖音网页端会检测浏览器环境(具体是检测什么并不太清楚，我试了用特殊方法使chrome的```webdriver=undefine```并不能解决问题)，被检测的结果就是拿不到数据，可以不设置无头浏览器看一下。

- 解决方案

> 使用firefox56版本配合geckodriver，可能其他版本也可以不过我没试，因为我电脑上正好有56版
