#coding:utf-8
from django.conf.urls import patterns, url
from shop import views

urlpatterns = patterns('',
        # 首页
        url('^$', views.list, name="index"),

        # 商品列表(戒指)
        url('^list/ring$', views.list, name="list"),
        
        # 商品列表(吊坠)
        url('^list/pendant$', views.list, name="list"),
        
        # 商品列表(耳坠)
        url('^list/earbob$', views.list, name="list"),
        
        # 商品列表(手链)
        url('^list/bracelet$', views.list, name="list"),

        # 商品列表(项链)
        url('^list/torque$', views.list, name="list"),

        # 商品列表(胸针)
        url('^list/brooch$', views.list, name="list"),

        # 商品详情页
        url('goods_detail', views.goods_detail, name="goods_detail"),

        # 首页按类型筛选，ajax
        url('filter-type', views.filter_type, name="filter_type"),
)

