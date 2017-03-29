#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import Controller, scaffold, route_menu, route_with, route, settings
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

    @route_menu(list_name=u'backend', text=u'購物金', sort=9803, icon='users', group=u'帳號管理', need_hr_parent=True)
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
        return self.json({'result': 'success'})