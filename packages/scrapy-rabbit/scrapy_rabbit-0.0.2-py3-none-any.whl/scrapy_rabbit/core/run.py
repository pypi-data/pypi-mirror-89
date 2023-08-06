# -*- coding: utf-8 -*-
import sys
import os
from importlib import import_module
import datetime
import logging
from scrapy_rabbit.Lib.loadspider import SpiderLoader
sys.path.append(os.path.abspath('..'))

try:
    sys.path.append(os.path.abspath('../..'))
    import settings
except ModuleNotFoundError:
    sys.path.append(os.path.abspath('..'))
    import settings
import pipelines



config = dict()

logging.basicConfig(level=getattr(logging, getattr(settings, 'LOG_LEVEL', 'DEBUG')),
                    format='pid:%(process)d %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    # filename=getattr(logging, getattr(settings, 'LOG_FILE')),
                    # filemode='a'
                    )


def run(cmd: list = None) -> None:
    """手动启动方法"""
    base_path = 'spiders.'
    if not cmd:
        path = base_path + config['path']
        root_path = config['path']
        spider_name = config['name']
        queue_name = config['path']+'/'+spider_name
        way = config['way']
        async_num = config['async_num']
    else:
        try:
            path = base_path + cmd[0]
            root_path = cmd[0]
            spider_name = cmd[1]
            way = cmd[2]
            async_num = int(cmd[3])
            queue_name = cmd[0]+'/'+spider_name
        except Exception:
            logging.info("命令行格式错误")
            raise
    logging.info("爬虫启动时间：%s" % datetime.datetime.now())
    sl = SpiderLoader(type("settings", (object,), dict(getlist=lambda x: [path], getbool=lambda x: False)))
    spider_module = sl.load(spider_name)
    sp = spider_module(path=path, queue_name=queue_name, way=way, async_num=async_num)
    pipeline = import_module("pipelines")
    pipelineObj = getattr(pipeline, "%sPipeline" % root_path, getattr(pipeline, 'Pipeline'))()

    pipelineObj.open_spider(sp)
    setattr(sp, "pipelineObj", pipelineObj)
    sp.main()
    pipelineObj.close_spider(sp)
    logging.info("爬虫结束时间：%s" % datetime.datetime.now())
