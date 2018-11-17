function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
});

//获取地区/设施信息
$.get('/house/area_facility/', function (data) {
    // alert('获取城区、设施成功')
    var area_html = '';
    for (var i = 0; i < data.area.length; i++) {
        area_html += '<option value="' + data.area[i].id + '">' + data.area[i].name + '</option>'
    }
    $('#area-id').html(area_html);

    var facility_html_list = '';
    for (var i = 0; i < data.facility.length; i++) {
        var facility_html = '<li><div class="checkbox"><label><input type="checkbox" name="facility"';

        facility_html += ' value="' + data.facility[i].id + '">' + data.facility[i].name;

        facility_html += '</label></div></li>';

        facility_html_list += facility_html
    }
    $('.house-facility-list').html(facility_html_list)
});

//提交房屋
$('#form-house-info').submit(function () {
    // alert('aaa');
    $('.error-msg text-center').hide();
    //验证内容是否填写
    // alert($(this).serialize());
    $.post('/house/newhouse/', $(this).serialize(), function (data) {
        if (data.code == '200') {
            $('#form-house-info').hide();
            $('#form-house-image').show();
            //给隐藏的标签传递房屋id
            $('#house-id').val(data.house_id);
        } else {
            $('.error-msg').show().find('span').html(ret_map[data.code]);
        }
    });
    return false;
});


//为图片表单绑定事件
$('#form-house-image').submit(function () {
    // alert('123');
    $(this).ajaxSubmit({
        url: "/house/image/",
        type: "POST",
        dataType: "json",
        success: function (data) {
            if (data.code == '200') {
                $('.house-image-cons').append('<img src="' + data.url + '"/>');
            }
        }
    });
    return false;
});