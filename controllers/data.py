#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
from datetime import datetime
from argeweb import Controller, scaffold, route_menu, route_with, route, settings
from argeweb import auth, add_authorizations
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from plugins.mail import Mail
from ..models.user_shop_point_model import UserShopPointModel


class Data(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        pagination_actions = ('list',)
        pagination_limit = 50
        default_view = 'json'
        Model = UserShopPointModel

    @route
    @add_authorizations(auth.check_user)
    @route_with('/data/user/shop_point', name='data:user:shop_point')
    def shop_point(self):
        use = 0
        max = 0
        if self.application_user:
            m = self.meta.Model.get_or_create(self.application_user)
            if m:
                max = m.point
            if 'shop_point_use' in self.session:
                use = self.session['shop_point_use']

        from ..models.user_shop_point_config_model import UserShopPointConfigModel
        config = UserShopPointConfigModel.find_or_create_by_name(self.namespace)
        self.context['data'] = {
            'result': 'true', 'point': use, 'point_max': max, 'max_use_point_for_order': config.max_use_point_for_order,
            'available_point': config.available_point, 'discount_ratio': config.discount_ratio,
            'is_must_use': config.is_must_use
        }
