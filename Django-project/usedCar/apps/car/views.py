from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from apps.car.models import Carinfo, Brand
from apps.user.models import User
from utils.functions import is_login


def index(request):
    """首页、及展示"""
    if request.method == 'GET':
        # username = request.session.get('username')
        # user = User.objects.filter(username=username).first()
        cars = Carinfo.objects.filter(examine='2')
        return render(request, 'index.html', {'cars': cars})


@is_login
def info_message(request):
    """卖车"""
    if request.method == 'GET':
        brands = Brand.objects.all()
        return render(request, 'info-message.html', {'brands': brands})
    if request.method == 'POST':
        user = request.user
        realname = request.POST.get('realname')
        uidentity = request.POST.get('identity')
        address = request.POST.get('address')
        cellphone = request.POST.get('phone')
        sex = request.POST.get('gender')
        user.realname = realname
        user.uidentity = uidentity
        user.address = address
        user.cellphone = cellphone
        user.sex = sex
        user.save()  # 卖家:外键

        brands = request.POST.get('brands')
        carbrand = Brand.objects.filter(btitle=brands).first()  # 商标:外键

        picture = request.FILES.get('pic')
        model = request.POST.get('model')
        regist_date = request.POST.get('regist_date')
        engineNo = request.POST.get('engineNo')
        mileage = request.POST.get('mileage')
        isService = request.POST.get('isService')
        price = request.POST.get('price')
        newprice = request.POST.get('newprice')
        formalities = request.POST.get('formalities')
        isDebt = request.POST.get('isDebt')
        promise = request.POST.get('promise')

        car_dict = {'user': user, 'carbrand': carbrand,
                    'picture': picture,
                    'model': model, 'regist_date': regist_date, 'engineNo': engineNo,
                    'mileage': mileage, 'isService': isService, 'price': price,
                    'newprice': newprice, 'formalities': formalities, 'isDebt': isDebt, 'promise': promise}
        try:
            Carinfo.objects.create(**car_dict)
        except:
            return HttpResponse('提交的信息不满足基本要求，请重试')

        return JsonResponse({'code': 200})


def carlist(request):
    """车辆展示列表"""
    if request.method == 'GET':
        cars = Carinfo.objects.filter(examine='2', isDelete=False)
        return render(request, 'list.html', {'cars': cars})


def price0_10(request):
    if request.method == 'GET':
        cars = Carinfo.objects.filter(examine='2', isDelete=False, price__gte=0, price__lte=10)
        return render(request, 'list.html', {'cars': cars})


def price10_30(request):
    if request.method == 'GET':
        cars = Carinfo.objects.filter(examine='2', isDelete=False, price__gte=10, price__lte=30)
        return render(request, 'list.html', {'cars': cars})


def price30_80(request):
    if request.method == 'GET':
        cars = Carinfo.objects.filter(examine='2', isDelete=False, price__gte=30, price__lte=80)
        return render(request, 'list.html', {'cars': cars})


def price80_(request):
    if request.method == 'GET':
        cars = Carinfo.objects.filter(examine='2', isDelete=False, price__gte=80)
        return render(request, 'list.html', {'cars': cars})


def car_detail(request, id):
    """单个车辆描述"""
    if request.method == 'GET':
        car = Carinfo.objects.filter(id=id).first()
        return render(request, 'detail.html', {'car': car})


@is_login
def car_cancel(request, id):
    """卖家取消发布订单"""
    car = Carinfo.objects.filter(id=id).first()
    car.isDelete = True
    car.save()
    return HttpResponseRedirect(reverse('user:user_info'))


@is_login
def alterprice(request, id):
    if request.method == 'POST':
        car = Carinfo.objects.filter(id=id).first()
        try:
            price = float(request.POST.get('alterprice'))
        except:
            return HttpResponse('请输入合法数字!')
        car.price = price
        car.save()
        return HttpResponseRedirect(reverse('user:user_info'))
