# -*- coding: utf-8 -*-
from flask import  jsonify
from hdfs import InsecureClient
from pyhive import hive

import jieba
import jieba.analyse
import re
import string

class JiebaUtil():
    # 删除停用词，标点符号，url等
    remove_spl_char_regex = re.compile('[%s！“￥‘，。、（）：；《》？【】……——]'.decode('utf-8') % re.escape(string.punctuation))  # regex to remove special characters

    @staticmethod
    def loadUserDic(dicts, stops):
        # jieba.load_userdict("/storeage/glzheng/qingbaodata/positive.txt")
        # jieba.load_userdict("/storeage/glzheng/qingbaodata/negative.txt")
        # jieba.analyse.set_stop_words("/storeage/glzheng/qingbaodata/jieba_stops.txt")
        for dic in dicts:
            jieba.load_userdict(dic)
        for dic in stops:
            jieba.analyse.set_stop_words(dic)

    @staticmethod
    def tokenizewithjieba(text):

        # text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',text)  # to replace url with ''
        # text = JiebaUtil.remove_spl_char_regex.sub(" ", text)  # Remove special characters
        # text = re.sub('^(\s{1,})|(\s{1,})$', '',text.decode('utf-8'))#remove prefix and suffix blank
        # text = text.lower()
        # res = jieba.cut(text)  # 默认是精确模式
        # tokens = re.split('\s{1,}', re.sub('^(\s{1,})|(\s{1,})$', '',text ))
        # return " ".join(res)

        text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',text)
        text = JiebaUtil.remove_spl_char_regex.sub(" ", text.decode("utf8"))  # Remove special characters
        text = re.sub('^(\s{1,})|(\s{1,})$', '',text)#remove prefix and suffix blank
        text = text.lower()
        res = jieba.cut(text)  # 默认是精确模式
        tokens = re.split('\s{1,}', re.sub('^(\s{1,})|(\s{1,})$', '',text ))
        return " ".join(res)