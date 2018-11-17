from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from goods.models import Goods
from cart.models import ShoppingCart
from orders.models import OrderInfo
# Create your views here.
from django.urls import reverse


def add_cart(request):
    if request.method == 'POST':
        # 添加到session中的数据格式为:
        # key:goods
        # value:[[id1,num,1],[id2,num,1],[id3,num,1]...]

        # 1. 没有登陆的情况
        # 1.1 添加到购物车的数据，其实就是添加到session中
        # 1.2 如果商品已经加入到session中，则修改session中商品的个数
        # 1.3如果商品没有添加到session中，则添加

        # 获取从ajax中传递的商品的id和商品的个数
        goods_id = request.POST.get('goods_id')  # 从网页中获取的数据
        goods_num = int(request.POST.get('goods_num'))  # 从网页中获取的数据

        goods_list = [goods_id, goods_num, 1]  # 放进列表中
        # user_id = request.session.get('user_id')
        if request.session.get('goods'):  # 得到value的的值[ [] [] [] ]
            # 说明购物车中已经存储有商品
            flag = 0  # 如果购物车中已经存在了该商品,则修改flag为1，则否flag为0
            # flag默认为0，默认购物车中没有该商品
            session_goods = request.session['goods']  # 得到value [[] [] []]
            for goods in session_goods:  # 遍历value列表中的小列表[id1,num]
                if goods_id == goods[0]:
                    goods[1] = goods[1] + goods_num
                    flag = 1
            if not flag:  # 此时已经遍历完value，若还是为0  表示添加到session中的商品之前并没有添加
                session_goods.append(goods_list)  # [  ].append([])

            # 修改成功session中商品的信息
            request.session['goods'] = session_goods  # [[] [] []]
            # cart_count = len(session_goods)

            f_acount = 0  # 商品总数
            for good_category in session_goods:
                f_acount += int(good_category[1])
        else:
            # 说明购物车中还没有存储商品信息
            data = []
            data.append(goods_list)  # [[] [] []]
            request.session['goods'] = data  # [[] [] []]
            cart_count = 1

            f_acount = 0  # 商品总数
            for good_category in request.session['goods']:
                f_acount += int(good_category[1])
        return JsonResponse({'code': 200, 'f_acount': f_acount})
        # return HttpResponseRedirect(reverse('home:index'))


def cart(request):
    if request.method == 'GET':
        # 需要判断用户是否登录， session['user_id']
        # 1. 如果登录，则购物车中展示当前登录用户的购物车表中的数据
        # 2. 如果没有登录，则购物车页面中展示session中的数据
        user_id = request.session.get('user_id')
        if user_id:
            # 登录系统用户, 获取购物车中的商品信息
            shop_cart = ShoppingCart.objects.filter(user_id=user_id)
            goods_all = [(cart.goods, cart.nums, cart.is_select) for cart in shop_cart]

            return render(request, 'cart.html', {'goods_all': goods_all})
        else:
            # 没有登录
            session_goods = request.session.get('goods')
            # 拿到session中所有的商品id值
            if session_goods:
                # [商品对象,商品的数量,是否选择商品]
                goods_all = [(Goods.objects.get(pk=good[0]), good[1], good[2])
                             for good in session_goods]
            else:
                goods_all = ''
            return render(request, 'cart.html', {'goods_all': goods_all})


def f_price(request):
    """
    返回购物车或session中商品的价格，和总价
    {key:  [ [id1, price1],[id2, price2] ],   key2: total_price}
    """
    user_id = request.session.get('user_id')
    if user_id:  # 登录情况下
        carts = ShoppingCart.objects.filter(user_id=user_id)
        cart_data = {}
        cart_data['goods_price'] = [(cart.goods_id, cart.nums * cart.goods.shop_price) for cart in carts]
        acount = 0  # 新增第三个栏位放合计的商品数量
        all_price = 0
        # 总的价格
        for cart in carts:
            if cart.is_select:  # 勾选的才计算合计价格
                all_price += cart.nums * cart.goods.shop_price
                acount += cart.nums
        cart_data['all_price'] = all_price
        cart_data['acount'] = acount

    else:  # 未登录情况下
        # 拿到session中所有的商品信息
        session_goods = request.session.get('goods')  # [ [id ,num ,is_select ,] [ , , ,] [ , , ,] ]
        cart_data = {}
        data_all = []  # [ [id1, price1],[id2, price2] ]
        all_price = 0
        acount = 0  # 新增第三个栏位放合计的商品数量
        for goods in session_goods:
            data = []  # [id1, price1]
            data.append(goods[0])
            g = Goods.objects.get(pk=goods[0])
            data.append(int(goods[1]) * g.shop_price)  # 这里装的是小计
            data_all.append(data)
            if goods[2]:  # 勾选的才计算合计价格
                all_price += int(goods[1]) * g.shop_price
                acount += int(goods[1])
        cart_data['goods_price'] = data_all
        cart_data['all_price'] = all_price
        cart_data['acount'] = acount
    return JsonResponse({'code': 200, 'cart_data': cart_data})


def f_acount(request):
    """
    返回购物车的总数
    """
    user_id = request.session.get('user_id')
    if user_id:
        """登录情况下"""
        carts = ShoppingCart.objects.filter(user_id=user_id)
        f_acount = 0  # 新增第三个栏位放购物车总商品数(不管是否选择)
        for cart in carts:
            f_acount += cart.nums

    else:
        """未登录情况下"""
        # 拿到session中所有的商品信息
        session_goods = request.session.get('goods')  # [ [id ,num ,is_select ,] [ , , ,] [ , , ,] ]
        f_acount = 0  # 新增第三个栏位放购物车总商品数(不管是否选择)
        for goods in session_goods:
            f_acount += int(goods[1])
    return JsonResponse({'code': 200, 'f_acount': f_acount})


def change_goods_num(request):
    if request.method == 'POST':
        # 修改购物车中商品的个数
        # 1. 先判断用户登录与否，如果用户没有登录，则修改session中商品的个数
        # 2. 如果用户登录，需要判断当前修改的商品是否存在于session中，如果存在，则修改session。如果不存在则修改购物车的表
        # 获取修改的商品id，商品个数，商品选择状态
        goods_id = request.POST.get('goods_id')
        goods_num = int(request.POST.get('goods_num'))
        is_select = request.POST.get('is_select')

        user_id = request.session.get('user_id')

        # 先判断要修改的商品是否存在于session中，如果存在则修改session中的商品个数和选择状态
        session_goods = request.session.get('goods')
        # goods的结构为: [id1, num, is_select]
        if session_goods:
            if goods_id:
                for goods in session_goods:
                    if goods[0] == goods_id:
                        # 修改session中商品的个数和选择状态
                        goods[1] = goods_num
                        goods[2] = is_select
            request.session['goods'] = session_goods

        # 如果用户登录了，则需要在修改购物车中数据，因为session中的商品有可能并不在购物车表中
        if user_id:
            # 修改购物车中商品个数
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).update(nums=goods_num,
                                                                                   is_select=is_select)
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def change_goods_status(request):
    if request.method == 'POST':
        # 1. 先判断用户登录与否，如果用户没有登录，则修改session中商品的个数
        # 2. 如果用户登录，需要判断当前修改的商品是否存在于session中，如果存在，则修改session。如果不存在则修改购物车的表
        status = request.POST.get('status')
        user_id = request.session.get('user_id')

        # 先判断要修改的商品是否存在于session中，如果存在则修改session中的商品个数和选择状态
        session_goods = request.session.get('goods')
        # goods的结构为: [id1, num, is_select]
        if session_goods:
            if status == 'true':
                for goods in session_goods:
                    goods[2] = 1
            if status == 'false':
                for goods in session_goods:
                    goods[2] = 0
        request.session['goods'] = session_goods

        # 如果用户登录了，则需要在修改购物车中数据，因为session中的商品有可能并不在购物车表中
        if user_id:
            # 修改购物车中商品个数
            if status == 'true':
                ShoppingCart.objects.filter(user_id=user_id).update(is_select=1)
            if status == 'false':
                ShoppingCart.objects.filter(user_id=user_id).update(is_select=0)

        return JsonResponse({'code': 200, 'msg': '请求成功'})


def write_change_goods_num(request):
    if request.method == 'POST':
        # 获取从页面手写的商品id,数量
        goods_id = request.POST.get('goods_id')
        good_current_num = int(request.POST.get('goods_current_num'))
        user_id = request.session.get('user_id')

        # 先判断要修改的商品是否存在于session中，如果存在则修改session中的商品个数和选择状态
        session_goods = request.session.get('goods')
        # goods的结构为: [id1, num, is_select]
        if session_goods:
            if goods_id:
                for goods in session_goods:
                    if goods[0] == goods_id:
                        # 修改session中商品的个数和选择状态
                        goods[1] = good_current_num
            request.session['goods'] = session_goods

        # 如果用户登录了，则需要在修改购物车中数据，因为session中的商品有可能并不在购物车表中
        if user_id:
            # 修改购物车中商品个数
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).update(nums=good_current_num)

        return JsonResponse({'code': 200, 'msg': '请求成功'})


def remove_goods(request):
    if request.method == 'POST':
        # 获取从页面手写的商品id,数量
        goods_id = request.POST.get('goods_id')
        user_id = request.session.get('user_id')

        # 先判断要修改的商品是否存在于session中，如果存在则修改session中的商品个数和选择状态
        session_goods = request.session.get('goods')
        # goods的结构为: [id1, num, is_select]
        if session_goods:
            if goods_id:
                for goods in session_goods[:]:
                    if goods[0] == goods_id:
                        # 移除该商品
                        session_goods.remove(goods)
            request.session['goods'] = session_goods

        # 如果用户登录了，则需要在修改购物车中数据，因为session中的商品有可能并不在购物车表中
        if user_id:
            # 修改购物车中商品个数
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).first().delete()

        return JsonResponse({'code': 200, 'msg': '请求成功'})
