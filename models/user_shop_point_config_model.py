#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import BasicModel
from argeweb import Fields


class UserShopPointConfigModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(default=u'購物金設定', verbose_name=u'服務名稱')
    max_use_point_for_order = Fields.FloatProperty(default=0.05, verbose_name=u'每訂單最大可用購物金')
    available_point = Fields.FloatProperty(default=0.005, verbose_name=u'每訂單可獲得的購物金')
    discount_ratio = Fields.FloatProperty(default=100, verbose_name=u'折換比率')
    is_must_use = Fields.BooleanProperty(default=False, verbose_name=u'強制使用')
