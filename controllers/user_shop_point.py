#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import Controller, scaffold, route_menu, route_with, route, settings
from argeweb import auth, add_authorizations
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from ..models.user_shop_point_history_model import UserShopPointHistoryModel as History


class UserShopPoint(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)

    class Scaffold:
        display_in_form = ('account', 'created', 'modified')
        hidden_in_form = ('name', 'is_enable')
        display_in_list = ('user_name_proxy', 'user_email_proxy', 'point', 'used_point', 'modified')

    @route_menu(list_name=u'backend', text=u'會員點數', sort=9803, icon='users', group=u'帳號管理')
    def admin_list(self):
        scaffold.list(self)

    def admin_edit(self, key):
        scaffold.edit(self, key)
        item = self.context[self.scaffold.singular]
        self.context['history'] = History.query(History.shop_point_target==item.key).order(-History.sort)

    @route
    def admin_send_point(self):
        user_point_item = self.params.get_ndb_record('key')
        action = self.params.get_string('action')
        point = self.params.get_integer('point')
        remark = self.params.get_string('remark')
        if action == 'increase_point':
            user_point_item.increase_point(point, remark)
        if action == 'decrease_point':
            user_point_item.decrease_point(point, remark)
        user_point_item.put()
        return self.json({
            'message': u'完成',
            'data': {'result': 'success'}
        })

    @route
    @add_authorizations(auth.check_user)
    def pay_with_point(self):
        payment_record = self.params.get_ndb_record('payment_record')
        self.context['data'] = {'result': 'failure'}
        if payment_record is None:
            self.context['message'] = u'付款資訊不存在'
            return
        if self.application_user is None:
            self.context['message'] = u'使用者不存在，或尚未登入'
            return
        point_record = self.meta.Model.get_or_create(self.application_user)
        if point_record.point < payment_record.amount:
            self.context['message'] = u'點數餘額不足，請先儲值'
            return
        point_record.decrease_point(payment_record.amount, payment_record.title, payment_record.order_no, payment_record.amount)
        point_record.put()
        payment_record.set_state('full_payment_with_point')
        payment_record.put()
        self.context['data'] = {'result': 'success', 'point_record': point_record}
        self.context['message'] = u'成功使用點數進行支付'
        return self.redirect(payment_record.gen_result_url(self))

    @route
    def taskqueue_after_install(self):
        try:
            from plugins.payment_middle_layer.models.payment_type_model import PaymentTypeModel
            PaymentTypeModel.get_or_create(
                name='user_shop_point',
                title=u'點數支付',
                pay_uri='user_shop_point:user_shop_point:pay_with_point'
            )
            return 'done'
        except ImportError:
            self.logging.error(u'需要 "付款中間層"')
            return 'ImportError'
