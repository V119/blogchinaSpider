#!/usr/bin python3
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from thrift import Thrift

from blogchinaSpider.DBUtils.db_save import *
from hbase import THBaseService
from hbase.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol


from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from blogchinaSpider.items import BlogItem, AuthorItem, CommentItem


class SaveHBasePipeline(object):
    def __init__(self, settings):
        self.DB_URI = settings['HBASE_URI']
        self.DB_PORT = settings['HBASE_PORT']
        self.TB_INFO = settings['TB_INFO'].encode()
        self.TB_AUTHOR = settings['TB_AUTHOR'].encode()
        self.TB_BLOG = settings['TB_BLOG'].encode()
        self.TB_COMMENT = settings['TB_COMMENT'].encode()

        # 连接数据库表
        socket = TSocket.TSocket(self.DB_URI, self.DB_PORT)
        self.transport = TTransport.TFramedTransport(socket)
        protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.client = THBaseService.Client(protocol)

        self.transport.open()
        # 将爬虫开始的信息存入数据库
        self.spider_info_row_key, start_put = gen_start_spider_info()
        self.client.put(self.TB_INFO, start_put)
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.spider.settings
        return cls(settings=settings)

    def close_spider(self, spider):
        # 存储爬虫结束的信息
        stop_put = gen_stop_spider_info(self.spider_info_row_key)
        try:
            self.client.put(self.TB_INFO, stop_put)
        except:
            self.transport.close()
            self.transport.open()
            self.client.put(self.TB_INFO, stop_put)
        self.transport.close()

    def process_item(self, item, spider):
        if isinstance(item, BlogItem):
            _, item_put = gen_blog_put(item)
            try:
                self.client.put(self.TB_BLOG, item_put)
            except:
                self.transport.close()
                self.transport.open()
                self.client.put(self.TB_BLOG, item_put)
        elif isinstance(item, AuthorItem):
            _, item_put = gen_author_put(item)
            try:
                self.client.put(self.TB_AUTHOR, item_put)
            except:
                self.transport.close()
                self.transport.open()
                self.client.put(self.TB_AUTHOR, item_put)
        elif isinstance(item, CommentItem):
            _, item_put = gen_comment_put(item)
            try:
                self.client.put(self.TB_COMMENT, item_put)
            except:
                self.transport.close()
                self.transport.open()
                self.client.put(self.TB_COMMENT, item_put)

        return item


class ImageSavePipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        global store_uri
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        if isinstance(item, BlogItem):
            for image_url in item['pictures']:
                yield Request(image_url)

        if isinstance(item, AuthorItem):
            if item['image']:
                yield Request(item['image'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        # 将图片转化为二进制形式
        if isinstance(item, BlogItem):
            item['b_pictures'] = []
            for image_path in image_paths:
                try:
                    fin = open(store_uri + image_path, mode='br')
                    img = fin.read()
                    item['b_pictures'].append(img)
                    fin.close()
                except IOError as e:
                    print(e)

        elif isinstance(item, AuthorItem):
            item['b_image'] = b''
            try:
                fin = open(store_uri + image_paths[0], mode='br')
                img = fin.read()
                item['b_image'] = img
                fin.close()
            except IOError as e:
                print(e)

        return item
