#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from .html import HtmlProcess
from .kmeans import KMeans


def max_sublist(text_list):
    max_line = max(text_list)
    min_line = min(text_list)
    tem_list = [-1]*(max_line-min_line+1)
    for idx in text_list:
        tem_list[idx-min_line] = 10
    ostart = 0
    start = 0
    end = 0
    max_here = max_num = tem_list[0]
    for i, v in enumerate(tem_list):
        if max_here <= 0:
            ostart = i
            max_here = v
        else:
            max_here += v
        if max_num < max_here:
            max_num = max_here
            start = ostart
            end = i
    return start+min_line, end+min_line, max_num


def help():
    print("usage:%s url" % sys.argv[0])


def count_blank(str):
    count = 0
    for char in str:
        if char == ' ':
            count += 1
        else:
            break
    return count


def expand_text(start, end, blank_list):
    max_error = 2
    tem_list = blank_list[start:end+1]
    tem_list.sort()
    center = tem_list[int(len(tem_list)/2)]
    n_start = start
    n_end = end
    for i in range(start, 0, -1):
        if abs(center - blank_list[i]) > max_error:
            n_start = i
            break
    for i in range(end, len(blank_list)):
        if abs(center - blank_list[i]) > max_error:
            n_end = i
            break
    return n_start, n_end


def extract(url, show_type="text"):
    hp = HtmlProcess(url)
    feature = hp.get_feature()
    text_list = hp.get_text_list()
    html_list = hp.get_html_list()
    blank_list = list(map(count_blank, text_list))
    km = KMeans()
    km.run(feature)
    res = km.get_res()
    text = res['text']
    text_line = [i[2] for i in text]
    start, end, max_num = max_sublist(text_line)
    start, end = expand_text(start, end, blank_list)
    if show_type == "text":
        text_list = text_list[start:end]
        text_list = filter(lambda x: x.strip(), text_list)
        ret = '\n'.join(text_list)
    else:
        text_list = html_list[start:end]
        ret = ''.join(text_list)
    return ret


def save_res(url, res_file):
    try:
        dat = extract(url)
    except Exception as e:
        print(e)
        dat = str(e)
    res_file.write(url + '\n')
    res_file.write(dat + '\n')
    res_file.write('\n\n\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
        sys.exit(1)
    if len(sys.argv) == 2:
        print(extract(sys.argv[1]))
        sys.exit(0)
    if sys.argv[1] != '-f':
        help()
        sys.exit(1)
    fp = open(sys.argv[2], 'r')
    res_file = open(sys.argv[2].split('.')[0]+'res.txt', 'w')
    for url in fp.readlines():
        url = url.strip()
        print('read url:%s' % url)
        save_res(url, res_file)
        time.sleep(3)
        print('ok..')
    res_file.close()
