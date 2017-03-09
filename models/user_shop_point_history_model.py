#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import BasicModel
from argeweb import Fields
from user_shop_point_model import UserShopPointModel


class UserShopPointHistoryModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'系統編號')
    shop_point_target = Fields.KeyProperty(verbose_name=u'所屬單位', kind=UserShopPointModel)
    order_no = Fields.StringProperty(verbose_name=u'訂單編號', default=u'')
    order_amount = Fields.StringProperty(verbose_name=u'訂單金額', default=u'')
    decrease_point = Fields.IntegerProperty(verbose_name=u'點數减少', default=0)
    increase_point = Fields.IntegerProperty(verbose_name=u'點數增加', default=0)
    point = Fields.IntegerProperty(verbose_name=u'剩餘點數', default=0)
    remark = Fields.TextProperty(verbose_name=u'說明', default=u'')

    @classmethod
    def all_enable(cls, target=None, *args, **kwargs):
        if target:
            return cls.query(cls.shop_point_target == target.key).order(-cls.sort)
        return cls.query().order(-cls.sort)