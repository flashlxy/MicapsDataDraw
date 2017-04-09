# -*- coding: utf-8 -*-
#     MicapsData基类
#     Author:     Liu xianyao
#     Email:      flashlxy@qq.com
#     Update:     2017-04-06
#     Copyright:  ©江西省气象台 2017
#     Version:    1.1.20170406
from __future__ import print_function
from __future__ import print_function

import sys

import MicapsFile
from Map import Map
from Picture import Picture

reload(sys)
sys.setdefaultencoding('utf-8')

# matplotlib.use('Agg')
from pylab import *
from matplotlib.transforms import Bbox
import os
import numpy as np
import matplotlib.pyplot as plt
import nclcmaps

matplotlib.rcParams["figure.subplot.top"] = 1
matplotlib.rcParams["figure.subplot.bottom"] = 0
matplotlib.rcParams["figure.subplot.left"] = 0
matplotlib.rcParams["figure.subplot.right"] = 1
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体 SimHei
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
matplotlib.rcParams["savefig.dpi"] = 72


class Micaps:
    def __init__(self, filename):
        self.filename = filename
        self.dataflag = None
        self.style = None
        self.title = None
        self.yy = None
        self.mm = None
        self.dd = None
        self.hh = None
        self.forehh = None
        self.level = None
        self.deltalon = None
        self.deltalat = None
        self.beginlon = None
        self.endlon = None
        self.beginlat = None
        self.endlat = None
        self.beginlon = None
        self.endlon = None
        self.sumlon = None
        self.sumlat = None
        self.distance = None
        self.min = None
        self.max = None
        self.def1 = None
        self.def2 = None
        self.X = None
        self.Y = None
        self.Z = None
        self.outPath = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def UpdatePath(path, projection):
        """
        根据投影对象更新path
        :param path: 路径对象
        :param projection: 投影类型
        :return: 
        """
        if path is None:
            return
        for point in path.vertices:
            point[0], point[1] = projection(point[0], point[1])

    @staticmethod
    def Update(products, projection):
        """
        根据投影类型和更新产品对象中的path对象
        :param products: 产品参数
        :param projection: 投影类型
        :return: 
        """

        Micaps.UpdatePath(products.map.clipborders[0].path, projection)

        for area in products.map.borders:
            Micaps.UpdatePath(area.path, projection)

    @staticmethod
    def UpdateXY(projection, x, y):
        return projection(x, y)

    def UpdateExtents(self, products):
        """
        更新产品参数的extents
        :param products: 产品参数对象
        :return: 
        """
        if products.picture.extents is None:
            maxlon = max(self.endlon, self.beginlon)
            minlon = min(self.endlon, self.beginlon)
            maxlat = max(self.endlat, self.beginlat)
            minlat = min(self.endlat, self.beginlat)
            margin = products.picture.margin
            xmax = maxlon + margin if maxlon + margin <= 180 else 180
            xmin = minlon - margin if minlon - margin >= -180 else -180
            ymax = maxlat + margin if maxlat + margin <= 90 else 90
            ymin = minlat - margin if minlat - margin >= -90 else -90
            products.picture.extents = Bbox.from_extents(xmin, ymin, xmax, ymax)

    def UpdateData(self, products):
        self.UpdateExtents(products)

    def GetExtend(self):
        if self.title.find(u'降水') >= 0 or self.title.find(u'雨'):
            extend = 'max'
        else:
            extend = 'neither'
        return extend

    def Draw(self, products, debug=True):
        """
        根据产品参数绘制图像
        :param debug: 
        :param products: 
        :return: 产品参数
        """
        # 图例的延展类型
        extend = self.GetExtend()

        # 更新绘图矩形区域
        # self.UpdateExtents(products)
        self.UpdateData(products)
        extents = products.picture.extents
        xmax = extents.xmax
        xmin = extents.xmin
        ymax = extents.ymax
        ymin = extents.ymin

        # 设置绘图画板的宽和高 单位：英寸
        h = products.picture.height
        if products.map.projection.name == 'sall':  # 等经纬度投影时不用配置本身的宽度，直接根据宽高比得到
            w = h * np.math.fabs((xmax - xmin) / (ymax - ymin)) * products.picture.widthshrink
        else:
            w = products.picture.width

        # 创建画布
        fig = plt.figure(figsize=(w, h), dpi=products.picture.dpi, facecolor="white")  # 必须在前面
        # ax = fig.add_subplot(111)
        # 设置绘图区域
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)

        # 背景透明
        fig.patch.set_alpha(products.picture.opacity)

        # 坐标系统尽可能靠近绘图区边界
        fig.tight_layout(pad=products.picture.pad)

        # 获得产品投影
        from Projection import Projection
        m = Projection.GetProjection(products)
        if m is not plt:
            # 用投影更新经纬度数据
            self.X, self.Y = Micaps.UpdateXY(m, self.X, self.Y)
            # 用投影更新产品参数中涉及经纬度的数据
            Micaps.Update(products, m)
            # 画世界底图
            Map.DrawWorld(products, m)

        # draw parallels and meridians.
        Map.DrawGridLine(products, m)

        # 绘制裁切区域边界
        patch = Map.DrawClipBorders(products.map.clipborders)

        # 绘制地图
        Map.DrawBorders(m, products)

        micapsfile = products.micapsfiles[0]

        cmap = nclcmaps.cmaps(micapsfile.legend.micapslegendcolor)  # cm.jet  temp_diff_18lev
        vmax = math.ceil(self.max)
        vmin = math.floor(self.min)
        levels = arange(vmin - self.distance, vmax + self.distance + 0.1, self.distance)

        if micapsfile.legend.micapslegendvalue:
            level = levels
        else:
            level = micapsfile.legend.legendvalue

        # 绘制等值线 ------ 等值线和标注是一体的
        c = micapsfile.contour
        clipborder = products.map.clipborders[0]
        Map.DrawContourAndMark(contour=c, x=self.X, y=self.Y, z=self.Z,
                               level=level, clipborder=clipborder, patch=patch, m=m)

        cf = micapsfile.contour
        cbar = micapsfile.legend

        # 绘制色斑图 ------ 色版图、图例、裁切是一体的
        Map.DrawContourfAndLegend(contourf=cf, legend=cbar, clipborder=clipborder,
                                  patch=patch, cmap=cmap, levels=levels,
                                  extend=extend, extents=extents, x=self.X, y=self.Y, z=self.Z, m=m)

        # 绘制描述文本
        MicapsFile.MicapsFile.DrawTitle(m, micapsfile.title, self.title)

        # 存图
        Picture.savePicture(fig, products.picture.picfile)

        print(products.picture.picfile + u'存图成功!')
        if debug:
            plt.show()
