from django.conf.urls import url

from cart import views

urlpatterns = [
    # 添加到购物车
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    # 购物车页面
    url(r'^cart/', views.cart, name='cart'),
    # 刷新价格
    url(r'^f_price/', views.f_price, name='f_price'),

    # 当前购物车总商品数量
    url(r'^f_acount/', views.f_acount, name='f_acount'),

    # 改变商品选择/数量
    url(r'^change_goods_num/', views.change_goods_num, name='change_goods_num'),

    # 改变所有商品的选择状态
    url(r'^change_goods_status/', views.change_goods_status, name='change_goods_status'),
    # 手写商品数量
    url(r'^write_change_goods_num/', views.write_change_goods_num, name='write_change_goods_num'),
    # 移除商品
    url(r'^remove_goods/',views.remove_goods,name='remove_goods')

]
