#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt


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

    def _init_plot(self):
        fig, axes = plt.subplots(self.row, self.col)
        self._axl = axes.flat

    def run(self, sample_list, show=False):
        show and self._init_plot()
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
            show and self._draw(i)
        show and self._show()

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

    def _draw(self, time):
        ax = self._axl[time]
        xtext = [i[0] for i in self._ktext_list]
        ytext = [i[1] for i in self._ktext_list]
        xother = [i[0] for i in self._kother_list]
        yother = [i[1] for i in self._kother_list]
        ax.plot(xtext, ytext, 'gs', alpha=0.75)
        ax.plot(xother, yother, 'yo', alpha=0.75)
        ax.plot([self._ktext[0]], [self._ktext[1]], 'r^')
        ax.plot([self._kother[0]], [self._ktext[1]], 'b^')
        ax.set_title('%sth' % (time+1))

    def _show(self):
        plt.show()
