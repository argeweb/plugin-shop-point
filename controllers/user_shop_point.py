#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import Controller, scaffold, route_menu, route
from argeweb import auth, add_authorizations
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from ..models.user_shop_point_history_model import UserShopPointHistoryModel as History


class UserShopPoint(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)

    class Scaffold:
        display_in_form = ['account', 'created', 'modified']
        hidden_in_form = ['name', 'is_enable']
        display_in_list = ['user_name_proxy', 'user_email_proxy', 'point', 'used_point', 'modified']

    @route
    @route_menu(list_name=u'system', group=u'購物金', text=u'串接測試', sort=811, target='_blank')
    def admin_test(self):
        from plugins.payment_middle_layer.models.payment_test_order_model import PaymentTestOrderModel
        from plugins.payment_middle_layer.models.payment_type_model import PaymentTypeModel
        payment_type = PaymentTypeModel.get_by_name('user_shop_point')
        order = PaymentTestOrderModel.gen_test_order('user_shop_point', payment_type)
        payment_record = self.fire(
            event_name='create_payment',
            title=u'測試訂單 %s' % order.order_no,
            detail=u'支付訂單 %s 使用 %s ' % (order.order_no, payment_type.title),
            amount=order.need_pay_amount,
            source=order,
            source_params={'order_no': order.order_no},
            source_callback_uri='admin:payment_middle_layer:payment_middle_layer:after_pay_for_test',
            payment_type=payment_type,
            user=self.application_user,
            status='pending_payment',
        )
        return self.redirect(payment_record.pay_url)

    @route_menu(list_name=u'backend', group=u'帳號管理', text=u'會員購物金', sort=9803, icon='users')
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
            self.context['message'] = u'點數餘額不足'
            payment_record.set_state('not_enough')
            payment_record.put()
            return
        point_record.decrease_point(payment_record.amount, payment_record.title, payment_record.order_no, payment_record.amount)
        point_record.put()
        payment_record.set_state('full_payment_with_point')
        payment_record.put()
        self.context['data'] = {'result': 'success', 'point_record': point_record}
        self.context['message'] = u'成功使用點數進行支付'
        return self.redirect(payment_record.return_rul)

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
