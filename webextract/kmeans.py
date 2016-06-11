#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math


class KMeans(object):
    """
    kmeans
    """
    row = 2
    col = 3
    time = row*col

    def __init__(self):
        self._ktext = [0, 0]
        self._kother = [0, 0]
        self._ktext_list = []
        self._kother_list = []

    def run(self, sample_list):
        self._sample_list = sample_list
        self.init()
        for i in range(self.time):
            self._ktext_list = []
            self._kother_list = []
            for dot in self._sample_list:
                to_text = self._get_distance(self._ktext, dot)
                to_other = self._get_distance(self._kother, dot)
                if to_text < to_other:
                    self._ktext_list.append(dot)
                else:
                    self._kother_list.append(dot)
            self._kupdate()

    def get_res(self):
        res = {}
        res['text'] = self._ktext_list
        res['other'] = self._kother_list
        return res

    def init(self):
        for dot in self._sample_list:
            if dot[0] > self._ktext[0]:
                self._ktext[0] = dot[0]
            if dot[1] > self._ktext[1]:
                self._ktext[1] = dot[1]

    def _kupdate(self):
        if self._ktext_list:
            x = 0
            y = 0
            for dot in self._ktext_list:
                x += dot[0]
                y += dot[1]
            x = x/len(self._ktext_list)
            y = y/len(self._ktext_list)
            self._ktext = [x, y]
        if self._kother_list:
            x = 0
            y = 0
            for dot in self._kother_list:
                x += dot[0]
                y += dot[1]
            x = x/len(self._kother_list)
            y = y/len(self._kother_list)
            self._kother = [x, y]

    def _get_distance(self, dot0, dot1):
        return math.sqrt(math.pow(dot0[0] - dot1[0], 2) +
                         math.pow(dot0[1] - dot1[1], 2))
