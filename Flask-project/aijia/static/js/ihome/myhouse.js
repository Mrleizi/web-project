$(document).ready(function () {
    $.get('/house/auth_myhouse/', function (data) {
            if (data.code == '200') {
                //已完成实名认证
                $('.auth-warn').hide();
                $('#houses-list').show();
                for (var i = 0; i < data.hlist.length; i++) {
                    var new_house_image = '<li><a href="/house/detail/?id=' + data.hlist[i].id + '"><div class="house-title"><h3>房屋ID:' + data.hlist[i].id + '—— 房屋标题' + i + 1 + '</h3></div>';
                    new_house_image += '<div class="house-content">';
                    new_house_image += '<img src="' + data.hlist[i].image + '">' + '<div class="house-text"><ul>';
                    new_house_image += '<li>位于：' + data.hlist[i].area + '</li><li>价格：￥' + data.hlist[i].price + '/晚</li><li>发布时间：' + data.hlist[i].create_time + '</li>';
                    new_house_image += '</ul></div></div></a></li>';
                    $('#houses-list').append(new_house_image);
                }
            }

            else {
                //未实名认证
                $('#auth-warn').show();
                $('#houses-list').hide();

            }
        }
    );
});


