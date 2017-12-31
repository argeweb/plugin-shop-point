#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.
import time

from argeweb import ViewDatastore
from argeweb.core.events import on
from .models.user_shop_point_model import UserShopPointModel
from .models.user_shop_point_order_model import UserShopPointOrderModel
from .models.user_shop_point_history_model import UserShopPointHistoryModel
from .models.user_shop_point_product_model import UserShopPointProductModel


@on('after_user_delete')
def after_user_delete(controller, key, *args, **kwargs):
    data_list = UserShopPointModel.query(UserShopPointModel.user==key).fetch()
    for data in data_list:
        data_list_2 = UserShopPointHistoryModel.query(UserShopPointHistoryModel.shop_point_target==data.key).fetch()
        for data_2 in data_list_2:
            data_2.delete()
        data.delete()


@on('buy_user_shop_point')
def buy_user_shop_point(controller, user, point_product_name, payment_type, callback_uri='', *args, **kwargs):
    if payment_type.name == 'user_shop_point':
        return None
    product = UserShopPointProductModel.get_by_name(point_product_name)
    if product is None or user is None:
        return None
    order = UserShopPointOrderModel.gen_order(product=product, payment_type=payment_type)
    controller.fire(
        event_name='create_payment',
        title=u'購買 %s' % order.product_title,
        detail=u'支付訂單 %s 使用 %s ' % (order.order_no, payment_type.title),
        amount=order.need_pay_amount,
        source=order,
        source_params={'order_no': order.order_no, 'callback_uri': callback_uri, 'point': product.point},
        source_callback_uri='user_shop_point:user_shop_point:after_pay_buy_point',
        payment_type=payment_type,
        user=user,
        status='pending_payment',
    )
    return controller.payment_record


@on('after_order_checkout')
def after_order_checkout(controller, order_list, user, *args, **kwargs):
    session = controller.session
    shopping_cash = 0.0
    if 'shop_point_use' in session:
        shopping_cash = session['shop_point_use']

    controller.logging.info(shopping_cash)
    total_amount_for_all_order = 0.0
    for order in order_list:
        total_amount_for_all_order = total_amount_for_all_order + order.total_amount

    user_point_item = UserShopPointModel.get_or_create(order.user.get())
    ds = shopping_cash
    n = 0
    from models.config_model import ConfigModel
    config = ConfigModel.get_config()
    for order in order_list:
        n += 1
        p = order.total_amount / total_amount_for_all_order
        s = shopping_cash * p // 1.0
        if s > 0 and ds - s >= 0:
            ds = ds - s
            if len(order_list) == n and ds >= 0:
                s = s + ds
            controller.logging.info(s)
            order.add_discount(u'購物金折抵', s)
            order.total_discount_amount = s
            order.currency_total_discount_amount = s
            user_point_item.decrease_point(
                order.total_discount_amount, u'由訂單 %s 扣除' % order.order_no,
                order.order_no, order.total_amount)
            user_point_item.put()
            order.need_pay_amount = float(order.total_amount) - float(order.total_discount_amount)
        if config.give_time == u'after_order_checkout':
            user_point_item.increase_point(
                order.total_amount * config.available_point / 100.0,
                u'由訂單 %s 增加' % order.order_no,
                order.order_no, order.total_amount
            )
            user_point_item.put()
    session['shop_point_use'] = 0.0
    return


@on('after_order_close')
def after_order_close(controller, *args, **kwargs):
    # 訂單完成後
    order = None
    if 'order' in kwargs:
        order = kwargs['order']
    if order is None:
        return

    user_point_item = UserShopPointModel.get_or_create(order.user.get())
    from models.config_model import ConfigModel
    config = ConfigModel.get_config()
    if config.give_time == u'after_order_close':
        user_point_item.increase_point(
            order.total_amount * config.available_point / 100.0,
            u'由訂單(完成) %s 增加' % order.order_no,
            order.order_no, order.total_amount
        )
        user_point_item.put()

ViewDatastore.register('shop_point', UserShopPointModel.get_or_create)
ViewDatastore.register('shop_point_history', UserShopPointHistoryModel.all_enable)
ViewDatastore.register('shop_point_product', UserShopPointProductModel.all_enable)


plugins_helper = {
    'title': u'購物金',
    'desc': u'擴展網站的購物金功能，用於購買後的贈送點數',
    'controllers': {
        'user_shop_point': {
            'group': u'購物金',
            'actions': [
                {'action': 'list', 'name': u'購物金管理'},
                {'action': 'edit', 'name': u'編輯購物金'},
                {'action': 'view', 'name': u'檢視購物金'},
                {'action': 'delete', 'name': u'刪除購物金'},
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
            ]
        },
        'user_shop_point_product': {
            'group': u'購物金產品',
            'actions': [
                {'action': 'add', 'name': u'新增購物金產品'},
                {'action': 'list', 'name': u'購物金產品管理'},
                {'action': 'edit', 'name': u'編輯購物金產品'},
                {'action': 'view', 'name': u'檢視購物金產品'},
                {'action': 'delete', 'name': u'刪除購物金產品'},
            ]
        },
        'config': {
            'group': u'購物金設定',
            'actions': [
                {'action': 'config', 'name': u'購物金設定'},
            ]
        }
    }
}
