#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.
from datetime import datetime
from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from ..models.user_shop_point_model import UserShopPointModel


class Form(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        default_view = 'json'
        Model = UserShopPointModel

    class Scaffold:
        display_in_form = ['name', 'account', 'is_enable', 'sort', 'created', 'modified']
        display_in_list = ['name', 'account']

    @route
    @add_authorizations(auth.check_user)
    @route_with(name='form:user:use_shop_point')
    def use_shop_point(self):
        u = self.params.get_float('use')
        u2 = 0.0
        try:
            from plugins.currency.models.currency_model import CurrencyModel
            cu = CurrencyModel.get_current_or_main_currency_with_controller(self)
            u2 = cu.calc(u)
        except:
            pass
        m = self.meta.Model.get_or_create(self.application_user)
        if 0 <= u <= m.point:
            self.session['shop_point_use'] = u
            self.session['shop_point_use_in_currency'] = u2
            self.context['data'] = {'result': 'success', 'shop_point_use': u, 'shop_point_use_in_currency': u2}
            self.context['message'] = u'將使用購物金 %s 元' % u
            return
        if u > m.point:
            self.context['message'] = u'購物金不足'
        if u < 0:
            self.context['message'] = u'購物金金額有誤'
        self.session['shop_point_use'] = 0.0
        self.session['shop_point_use_in_currency'] = 0.0
        self.context['data'] = {'result': 'failure', 'shop_point_use': 0.0, 'shop_point_use_in_currency': 0.0}
