from django.shortcuts import render

from goods.models import Goods, GoodsCategory


def goods_detail(request, id):
    if request.method == 'GET':
        # 获取某个商品对象
        goods = Goods.objects.filter(pk=id).first()
        # 获取所有商品的分类
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'detail.html', {'goods': goods, 'category_types': category_types})
