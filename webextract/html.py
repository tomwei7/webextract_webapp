#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import chardet
from bs4 import BeautifulSoup, Comment


class HtmlProcess(object):
    """
    HtmlProcess
    """
    del_tag = ('style', 'script')
    clear_reg = re.compile('<.*?>')
    symbol_list = ('，', '。', '；', '‘', '“', '’', '”', '：',
                   '、', ',', '.', ';', "'", '"', ':')

    def __init__(self, url):
        self._url = url
        self._requests()
        self._filter_html()
        self._clear_html()
        self._generator_feature()

    def _requests(self):
        response = requests.get(self._url)
        content = response.content
        result = chardet.detect(content)
        if result['confidence'] > 0.6:
            self._encoding = result['encoding']
            self._content = content.decode(self._encoding, 'ignore')
        else:
            self._encoding = "utf-8"
            self._content = content.decode(self._encoding, 'ignore')

    def _clear_html(self):
        text = self.clear_reg.sub('', self._fhtml)
        self._text_list = text.split('\n')

    def _filter_html(self):
        self._content = self._content.replace('{', '{{').replace('}', '}}')
        soup = BeautifulSoup(self._content, 'html.parser')
        for tag_name in self.del_tag:
            for tag in soup.find_all(tag_name):
                tag.extract()
        for element in soup(text=lambda text: isinstance(text, Comment)):
                element.extract()
        unformatted_tag_list = []
        for i, tag in enumerate(soup.find_all(['span', 'a', 'img'])):
            unformatted_tag_list.append(str(tag))
            tag.replace_with('{' + 'unformatted_tag_list[{0}]'.format(i) + '}')
        self._fhtml = soup.prettify().format(
                unformatted_tag_list=unformatted_tag_list)
        self._fhtml_list = self._fhtml.split('\n')

    def _generator_feature(self):
        self._feature = []
        for idx, line in enumerate(self._text_list):
            if not line.strip():
                continue
            text_len = len(line)
            symbol_len = 0
            for char in line:
                symbol_len += 1 if char in self.symbol_list else 0
            self._feature.append((text_len, symbol_len, idx))

    def get_feature(self):
        return self._feature

    def get_text_list(self):
        return self._text_list

    def get_html_list(self):
        return self._fhtml_list
