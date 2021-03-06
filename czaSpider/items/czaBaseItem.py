from czaSpider.czaTools import *


class czaBaseItem(scrapy.Item):
    spiderName = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    parse_time = scrapy.Field()
    more = scrapy.Field()


def process_base_item(**kwargs):
    info = {}
    info["spiderName"] = kwargs.pop('spiderName', "IOCO")
    info["author"] = kwargs.pop('author', "czaOrz")
    info["url"] = kwargs.pop('url', 'www.czaOrz.xyz')
    info["parse_time"] = kwargs.pop('parse_time', None)
    info["more"] = kwargs
    return info


def publicItem(spider, **kwargs):
    res = dict()
    if spider.clean_item:
        res.update(kwargs)
    else:
        res.update(process_base_item(**kwargs))
    return res
