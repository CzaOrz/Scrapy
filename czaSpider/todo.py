__FILE__ = "Unfinished Todo"

# todo
"""
2019.05.29 - 解析附件部分代码需要整理docx，excel
2019.06.02 - 爬虫框架中还有raise Exception模块需要写，对各种异常的定义，要个性化一点
2019.06.03 - Scrapy框架signal模块是个什么原理，怎么实际开发中还能用的到，怎么用，参考巨潮年报
2019.06.03 - 现在的框架不支持post请求下载，这个显然不太合理，可以研究研究怎么下载post请求的数据
2019.06.03 - md说明文件的编写规范与格式
2019.06.03 - redis集群，这个怎么玩啊
2019.06.03 - 附件转化，doc转docx，pdf转html，还有pdf的相关操作，这些我是不是写过啊，再整理一下吧
2019.06.04 - 百度那位小哥的代码，看看是不是可以加入Item组件，感觉很牛
2019.06.05 - 关于各高校高考分数的信息，可以做一个数据分析，这个就没必要做持续，因为每年就一次高考，或许可以提供某些服务。爬985高校，211高校
2019.06.05 - 前端那种折线图，动态展示是怎么做的啊，折线，柱状图，饼状图等等
2019.06.06 - 各高校的分数等情况，是时候提上日程了
2019.06.11 - 绘图软件SAI，怎么说
2019.06.13 - pdf2html这个处理下 https://blog.csdn.net/silentacit/article/details/80309929
2019.06.17 - 对scrapy的理解还是不深，很多都不会
2019.06.17 - 工作所需：scrapy基本原理、反爬知识（涉及js重定向，加密，投毒等）、爬虫selenium模块、后端aiohttp、flask、Django模块，前端js，Vue模块，简单的异步实现
2019.06.17 - 工作经历：
中软是测试，测GPS、充电、开关机，舆情日报，AndroidStudio。
数博科技：爬虫工程师，
2019.06.17 - 算法题，各种计算机基础（算法原理，计算机基础），太重要了把，你只会一些大家都有的东西有什么意义，Django，Flask等，都太普遍了，意义是找工作，而且也只能去打杂的工作！
2019.06.17 - bootstrap wysiwyg 富文本编辑器
2019.06.18 - 微信可以了解验证码，微博可以练selenium
2019.06.18 - scrapy.extensions.logstats，scrapt的extension快怎么使用
2019.06.18 - 普通用户管理界面的完善，博客如何添加其他字体或文本，富文本编辑器?
2019.06.18 - numberAnimate数字滚动插件, 动态折线图 https://www.html5tricks.com/html5-canvas-animated-line.html,  临时https://blog.csdn.net/vhwfr2u02q/article/details/79492303
2019.06.18 - 评论回复并拼接是如何实现的
"""

"""DONE!
2019.06.17 - 博客编辑页面，root管理博客页面，个人管理个人博客页面
2016.06.05 - bs还是需要重新再看一遍啊，这次只看那些细节，我发现似乎只需要name点东西就可以拼出我想要的，如首页三列，左边是章节内容栏，右边是导航栏目，侧滑菜单是大方向，中间是内容
2016.06.05 - 正则学习，零宽断言 -- re.compile("var\s+(rand\d+)\s*=\"(.+?)\";(?=[\s\S]+document\.write\(\"(.+?)：.+\"\+\\1\+)") 零宽断言，中间居然能隔这么远，这已经是扣了
2019.06.02 - BoopStrap/JavaScript插件
2019.05.30 - 用户注册和登陆模块，前端的编写，后端需要在整理整理，别的不说，起码把注册页面再次搞出来把
2016.06.11 - 百度地图模块
2016.06.12 - Vue的学习
2016.06.12 - Jquery学习
2016.06.11 - inspect模块害的再斟酌斟酌
2019.06.03 - scrapy如何增加日志模块，可以在下载中执行指令-s LOG_FILE= --loglevel=INFO来启动吗
2016.06.04 - 廖老师的git和sql还是要再看看啊，这玩意有用的很
2016.06.03 - 如何使用logging模块兵输出具体的文件 from logging.handlers import TimedRotatingFileHandler 模块
2019.06.02 - BoopStrap组件
2016.06.03 - window下如何开启定时任务
2019.06.03 - 百度那位小哥的模拟Scrapy框架，可以学习学习精髓，有点小经典
2019.06.02 - 爬虫框架解析部分多线程或者多进程跑。- 对每一个线程传入标记位，以id最后一位作为判断计算此任务属于哪个线程，从而人为分配任务而非操作系统分配
2019.06-02 - BoopStrap全局CSS样式
2019.05.29 - 中国裁判文书网，对key的获取，需要处理
2019.05.30 - scrapy的deffer，或者说twisted模块如何使用
2019.05.31 - Failure - 该框架，解析部分是否可以使用异步，下载部分是否有必要使用异步。异步是使用twisted还是使用简单的async，这两个那种好一点，可以先研究上面的twisted再下结论
2019.05.31 - 把相应的js反爬，写一个中间件可以，name每次只需要调用该中间件即可，而不是每个模块都去写一遍处理逻辑
2019.05.29 - 把对计算云的辅助操作单独写一个模块，包含压缩与推送
2019.05.30 - 对工具进行适当地整理，把不要的删除，或者重新命名整合下
2019.05.30 - scrapy中间件需要在写一个模块，用于熟悉与练习
2019.05.30 - 计算云中新建线上环境的git仓，用于部署，还有专门链接文件的仓。即一个专门接受文件，用于链接这里面的文件，来实现部署
"""

"""不错的学习平台
html学习平台        https://www.html5tricks.com/   
js转化平台          http://tool.oschina.net/codeformat/js    
"""

"""
You Are An Apple In My Eyes
Courage is not the absence of fear, but rather the judgment that something else is more important than fear.
"""
