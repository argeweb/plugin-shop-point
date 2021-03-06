#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route_menu, route


class Config(Controller):
    class Scaffold:
        display_in_list = ['is_enable', 'category']
        hidden_in_form = ['name', 'title', 'use']

    @staticmethod
    def change_config(controller, item, *args, **kwargs):
        if item.can_buy is True:
            controller.fire(
                event_name='update_payment_type',
                name='user_shop_point',
                is_enable=True,
            )
        else:
            controller.fire(
                event_name='update_payment_type',
                name='user_shop_point',
                is_enable=False,
            )

    @route
    @route_menu(list_name=u'system', group=u'購物金', text=u'購物金設定', sort=809)
    def admin_config(self):
        config_record = self.meta.Model.get_config()
        self.events.scaffold_after_save += self.change_config
        return scaffold.edit(self, config_record.key)
