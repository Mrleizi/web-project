from django.conf.urls import url

from users import views

urlpatterns = [
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 注销
    url(r'^logout/', views.logout, name='logout'),
    # 获取登录系统的用户
    url(r'^is_login/', views.is_login, name='is_login'),
    # 个人信息中心
    url(r'^user_center_info/', views.user_center_info, name='user_center_info'),
    # 收货地址
    url(r'^user_center_site/', views.user_center_site, name='user_center_site'),
    # 设置默认收货地址
    url(r'^set_default_adress/', views.set_default_adress, name='set_default_adress'),
    # 删除收货地址
    url(r'^delete_user_address/', views.delete_user_address, name='delete_user_address')
]
