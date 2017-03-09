#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.
from datetime import datetime
from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold, route_menu, route_with, route, settings
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from ..models.user_shop_point_model import UserShopPointModel


class Form(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        pagination_actions = ('list',)
        pagination_limit = 50
        default_view = 'json'
        Model = UserShopPointModel

    class Scaffold:
        display_in_form = ('name', 'account', 'is_enable', 'sort', 'created', 'modified')
        display_in_list = ('name', 'account')

    @route
    @add_authorizations(auth.check_user)
    @route_with(name='form:user:use_shop_point')
    def use_shop_point(self):
        u = self.params.get_integer('use')
        m = self.meta.Model.get_or_create(self.application_user)
        if 0 <= u <= m.point:
            self.session['shop_point_use'] = u
            self.context['data'] = {'result': 'success', 'point': u, 'point_max': m.point}
            self.context['message'] = u'將使用購物金 %s 元' % u
        if u > m.point:
            self.session['shop_point_use'] = m.point
            self.context['message'] = u'購物金不足'
            self.context['data'] = {'result': 'failure', 'point': m.point, 'point_max': m.point}
        if u < 0:
            self.session['shop_point_use'] = 0
            self.context['message'] = u'購物金金額有誤'
            self.context['data'] = {'result': 'failure', 'point': 0, 'point_max': m.point}
