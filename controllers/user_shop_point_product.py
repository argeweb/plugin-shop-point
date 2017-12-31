#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import Controller, scaffold, route_menu


class UserShopPointProduct(Controller):
    @route_menu(list_name=u'system', group=u'購物金', text=u'販售的購物金', sort=815)
    def admin_list(self):
        return scaffold.list(self)

