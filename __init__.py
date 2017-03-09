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
                {'action': 'list', 'name': u'資料管理'},
                {'action': 'edit', 'name': u'編輯資料'},
                {'action': 'view', 'name': u'檢視資料'},
                {'action': 'delete', 'name': u'刪除資料'},
            ]
        },
        'user_shop_point_config': {
            'group': u'購物金設定',
            'actions': [
                {'action': 'config', 'name': u'編輯資料'},
            ]
        }
    }
}
