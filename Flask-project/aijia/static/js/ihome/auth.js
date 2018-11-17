function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$.get('/user/auths/', function (data) {
    $('#real-name').val(data.id_name);
    $('#id-card').val(data.id_card);
    if (data.id_name != null && data.id_name != '') {
        $('#real-name').attr('readonly', 'readonly');
        $('#id-card').attr('readonly', 'readonly');

        $('.btn-success').hide();
    }
});


$('#form-auth').submit(function () {
    var real_name = $('#real-name').val();
    var id_card = $('#id-card').val();
    $.ajax({
        url: '/user/auth/',
        type: 'PUT',
        dataType: 'json',
        data: {'real_name': real_name, 'id_card': id_card},
        success: function (data) {
            if (data.code == '200') {
                $('.btn-success').hide();
                $('.error-msg').hide();
            }
            else {
                $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + data.msg);
                $('.error-msg').show();
            }
        },
        error: function (data) {
            alert('实名认证失败')
        }
    });
    return false
});
