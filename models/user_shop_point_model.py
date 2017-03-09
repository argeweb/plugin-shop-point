#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import BasicModel
from argeweb import Fields
from argeweb.libs.bcrypt import bcrypt
from argeweb.libs.wtforms.validators import InputRequired
from plugins.application_user.models.application_user_model import ApplicationUserModel


class UserShopPointModel(BasicModel):
    class Meta:
        label_name = {
            'modified': u'最後變動時間',
        }
    name = Fields.StringProperty(verbose_name=u'系統編號')
    user = Fields.KeyProperty(verbose_name=u'使用者', kind=ApplicationUserModel)
    user_name_proxy = Fields.StringProperty(verbose_name=u'使用者名稱')
    user_email_proxy = Fields.StringProperty(verbose_name=u'E-Mail')
    point = Fields.IntegerProperty(verbose_name=u'現餘點數', default=0)
    used_point = Fields.IntegerProperty(verbose_name=u'已使用點數', default=0)

    @classmethod
    def get_or_create(cls, user):
        r = cls.query(cls.user==user.key).get()
        if r is None:
            r = cls(user=user.key)
            r._user = user
            r.user_name_proxy = r._user.name
            r.user_email_proxy = r._user.email
            r.put()
        r.user_name_proxy = user.name
        r.user_email_proxy = user.email
        return r

    @classmethod
    def after_get(cls, key, item):
        item._user = item.user.get()
        item.user_name_proxy = item._user.name
        item.user_email_proxy = item._user.email

    def increase_point(self, point, remark=u'', order_no=u'', order_amount=None):
        from user_shop_point_history_model import UserShopPointHistoryModel as History
        point = int(point)
        history = History()
        history.shop_point_target = self.key
        history.remark = remark
        history.increase_point = point
        history.order_no = order_no
        if order_amount is not None:
            history.order_amount = str(int(order_amount))
        history.point = int(self.point) + point
        history.put()
        self.point += point

    def decrease_point(self, point, remark, order_no=u'', order_amount=None):
        from user_shop_point_history_model import UserShopPointHistoryModel as History
        point = int(point)
        history = History()
        history.shop_point_target = self.key
        history.remark = remark
        history.decrease_point = point
        history.order_no = order_no
        if order_amount is not None:
            history.order_amount = str(int(order_amount))
        history.point = int(self.point) - point
        history.put()
        self.point -= point
        self.used_point += point

    def after_put(self, key):
        pass
