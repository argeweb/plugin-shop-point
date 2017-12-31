#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import BasicConfigModel
from argeweb import Fields


class ConfigModel(BasicConfigModel):
    class Meta:
        tab_pages = [u'購物時折抵', u'購物時獲得', u'點數購買']

    title = Fields.HiddenProperty(verbose_name=u'設定名稱', default=u'購物金設定')
    max_use_point_for_order = Fields.RangeProperty(verbose_name=u'每筆訂單可折抵最大購物金', unit='%', default=5, step=0.1, multiple=True)
    discount_ratio = Fields.RangeProperty(verbose_name=u'貨幣折換比率', unit='%', default=100, step=0.1)
    is_must_use = Fields.BooleanProperty(verbose_name=u'強制使用', default=False)
    min_amount = Fields.FloatProperty(verbose_name=u'金額閥值', default=0.0)
    available_point = Fields.RangeProperty(verbose_name=u'每訂單可獲得的購物金', tab_page=1, unit='%', default=0.5, step=0.1)
    can_buy = Fields.BooleanProperty(verbose_name=u'是否可以直接購買點數', default=False, tab_page=2)
    give_time = Fields.StringProperty(verbose_name=u'發放時間', default=u'after_order_checkout', choices=[
        'after_order_checkout', 'after_order_close',
    ], choices_text={
        'after_order_checkout': u'訂單建立後',
        'after_order_close': u'訂單完成後',
    })
