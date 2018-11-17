function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    //轮播动画
    // var mySwiper = new Swiper('.swiper-container', {
    //     loop: true,
    //     autoplay: 2000,
    //     autoplayDisableOnInteraction: false,
    //     pagination: '.swiper-pagination',
    //     paginationType: 'fraction'
    // });
    $(".book-house").show();
});

$.get('/house/detail/', function (data) {
    // alert('这个页面来了?');
    //获取到?后面的内容
    var search = document.location.search;
    id = search.split('=')[1];
    // alert(id );
    $.get('/house/detail/' + id + '/', function (data) {
        var banner_image = '';
        // alert(data.house.images[0]);
        for (var i = 0; i < data.house.images.length; i++) {
            banner_li = '<li class="swiper-slide"><img src="' + data.house.images[i] + '"></li>';
            banner_image += banner_li

        }
        $('.swiper-wrapper').html(banner_image);
        // $('.swiper-wrapper').append(banner_image);

        //添加轮播效果
        var mySwiper = new Swiper('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
        });


        $('.house-price').html('￥<span>' + data.house.price + '</span>/晚');
        //房东图片
        $('.landlord-pic').html('<img src="' + data.house.user_avatar + '">');
        //房东姓名
        $('.landlord-name').html('房东：<span>' + data.house.user_name + '</span>');

        $('.text-center').html('<li>' + data.house.address + '</li>');


        $('.house-type-datail').html('<h3>出租' + data.house.room_count + '间</h3><p>房屋面积:' + data.house.acreage + '平米</p><p>房屋户型:' + data.house.unit + '</p>');
        $('.house-capacity').html('<h3>' + data.house.capacity + '</h3>');
        $('.house-bed').html('<h3>卧床配置</h3><p>' + data.house.beds + '</p>');

        $('.house-info-style').html('<li>收取押金<span>' + data.house.deposit + '</span></li><li>最少入住天数<span>' + data.house.min_days + '</span></li><li>最多入住天数<span>' + data.house.max_days + '</span></li>');
        var facilities = '';
        for (var i = 0; i < data.house.facilities.length; i++) {
            facilities += '<li><span class="' + data.house.facilities[i].css + '"></span>' + data.house.facilities[i].name + '</li>';
        }
        $('.house-facility-list').html(facilities);
        // 评价信息
        // $('.house-comment-list')

        $('.book-house').attr('href', '/house/booking/?id=' + data.house.id);

        //    判断是否显示预定按钮
        if (data.booking == 1) {
            $('.book-house').show();
        }
        else {
            $('.book-house').hide();
        }

    })
});
