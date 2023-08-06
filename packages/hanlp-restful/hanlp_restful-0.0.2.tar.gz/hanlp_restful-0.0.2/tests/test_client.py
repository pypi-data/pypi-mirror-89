# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2020-12-20 16:12
from hanlp_restful import HanLPClient


def main():
    HanLP = HanLPClient('https://hanlp.hankcs.com/api', auth=None)  # Fill in your auth
    doc = HanLP.parse('2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。阿婆主来到北京立方庭参观自然语义科技公司。')
    print(doc)
    # doc.pretty_print(ner='ner/msra')
    # _test_raw_text()
    # _test_sents()
    # _test_tokens()


def _test_raw_text():
    HanLP = HanLPClient('https://hanlp.hankcs.com/api')
    text = ' '
    doc = HanLP.parse(text)
    print(doc)
    doc.pretty_print(ner='ner/pku')


def _test_sents():
    text = ['2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。',
            '英首相与特朗普通电话讨论华为与苹果公司。']
    nlp = HanLPClient('http://0.0.0.0:8666')
    doc = nlp(text)
    print(doc)
    doc.pretty_print()


def _test_tokens():
    tokens = [
        ["2021年", "HanLPv2.1", "为", "生产", "环境", "带来", "次", "世代", "最", "先进", "的", "多语种", "NLP", "技术", "。"],
        ["英", "首相", "与", "特朗普", "通", "电话", "讨论", "华为", "与", "苹果", "公司", "。"]
    ]
    nlp = HanLPClient('http://0.0.0.0:8666')
    doc = nlp(tokens=tokens, tasks=['ner*', 'srl', 'dep'])
    print(doc)
    doc.pretty_print()


if __name__ == '__main__':
    main()
