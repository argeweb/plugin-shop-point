#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/24.

from argeweb import ViewDatastore
from .models.user_shop_point_model import UserShopPointModel
from .models.user_shop_point_history_model import UserShopPointHistoryModel

ViewDatastore.register('shop_point', UserShopPointModel.get_or_create)
ViewDatastore.register('shop_point_history', UserShopPointHistoryModel.all_enable)

plugins_helper = {
    'title': u'使用者的購物金',
    'desc': u'擴展網站使用者的購物金功能',
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
        'user_shop_point_config': {
            'group': u'購物金設定',
            'actions': [
                {'action': 'config', 'name': u'購物金設定'},
            ]
        }
    },
    'install_uri': 'user_shop_point:user_shop_point:after_install'
}
