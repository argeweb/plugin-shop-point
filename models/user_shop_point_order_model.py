#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.
import time

from argeweb import Fields
from plugins.application_user.models.application_user_model import ApplicationUserModel
from plugins.payment_middle_layer.models.payment_type_model import PaymentTypeModel
from plugins.payment_middle_layer.models.payment_status_model import PaymentStatusModel
from plugins.payment_middle_layer.models.payment_record_model import PaymentRecordModel
from plugins.payment_middle_layer.models.payment_order_model import PaymentOrderModel


class UserShopPointOrderModel(PaymentOrderModel):
    @classmethod
    def gen_order(cls, name=None, product=None, payment_type=None):
        if name is None:
            name = str(int(time.time()))
        order = cls.get_or_create_by_name(name)
        order.product_title = product.title
        order.product_price = product.price
        order.order_no = str(int(time.time()))
        order.need_pay_amount = product.price

        order.payment_status_object = PaymentStatusModel.get_or_create_by_name('pending_payment').key
        if isinstance(payment_type, str):
            payment_type = PaymentTypeModel.get_by_name(payment_type)
        order.payment_type_object = payment_type.key
        return order
