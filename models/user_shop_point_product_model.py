#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import BasicModel
from argeweb import Fields


class UserShopPointProductModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(verbose_name=u'標題', default=u'50點')
    price = Fields.FloatProperty(verbose_name=u'價格', default=50.0)
    is_enable = Fields.BooleanProperty(verbose_name=u'啟用', default=True)
    remark = Fields.TextProperty(verbose_name=u'說明', default=u'')
