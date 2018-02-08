# -*- coding: utf-8 -*-

"""
    在线社区留言板词条分类功能:
    准备六个句子并人为分类攻击和非攻击性，
    计算得到由这些句子中构建的词汇表中每个单词分别属于攻击和非攻击的概率【两个向量】
    然后给定新的句子，判断该句子是否具有攻击性【新的句子中单词不得超出词汇表范围】
"""


# a 准备数据，构建词条向量
def loadDataSet():
    # 真实的词条 共六条
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    # 对上述词条进行人工标注【攻击性、非攻击性】
    classVec = [0, 1, 0, 1, 0, 1]   # 1 is abusive 0 not
    return postingList, classVec


# 创建词汇表:返回包含所有词条中出现过的单词组成的不重复的词汇表
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)     # union of the two set

    return list(vocabSet)



