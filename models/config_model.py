#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import BasicModel
from argeweb import Fields


class ConfigModel(BasicModel):
    class Meta:
        tab_pages = [u'購物時折抵', u'購物時獲得', u'點數購買']

    title = Fields.StringProperty(verbose_name=u'設定名稱', default=u'購物金設定')
    max_use_point_for_order = Fields.FloatProperty(verbose_name=u'每筆訂單可折抵最大購物金', default=0.05)
    discount_ratio = Fields.FloatProperty(verbose_name=u'折換比率', default=100)
    is_must_use = Fields.BooleanProperty(verbose_name=u'強制使用', default=False)
    available_point = Fields.FloatProperty(verbose_name=u'每訂單可獲得的購物金', tab_page=1, default=0.005)
    can_buy = Fields.BooleanProperty(verbose_name=u'是否可以直接購買點數', default=False, tab_page=2)
