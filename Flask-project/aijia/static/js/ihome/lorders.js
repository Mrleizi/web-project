//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);


    //获取租客的订单
    $.get('/order/lorders_list/', function (data) {
        var html = template('order_list', {olist: data.olist});
        $('.orders-list').html(html);

        //当页面元素存在后，再绑定接单、拒单事件

        // 作为房东,接单
        $(".order-accept").on("click", function () {
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-accept").attr("order-id", orderId);
        });

        //拒单
        $(".order-reject").on("click", function () {
            //获取orderId,attr("order-id", orderId);
            // var order_id = $(this).attr('order-id');
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-reject").attr("order-id", orderId);
        });

        //确定接单绑定事件
        $(".modal-accept").click(function () {
            var order_id = $(this).attr('order-id');
            $.ajax({
                url: '/order/order/' + order_id + '/',
                type: 'PUT',
                data: {'status': 'WAIT_PAYMENT'},
                success: function () {
                    //接单弹窗隐藏
                    $('#accept-modal').hide(data);

                    $('.modal-backdrop').css({'display': 'None'});
                    //接单拒单隐藏
                    $('.order-operate' + order_id).hide();
                    //订单状态
                    $('#' + order_id).text('待支付');
                }
            })
        });

        //拒单绑定事件
        $(".modal-reject").click(function () {
            var order_id = $(this).attr('order-id');
            var comment = $('#reject-reason').val();
            $.ajax({
                url: '/order/order/' + order_id + '/',
                type: 'PUT',
                data: {'status': 'REJECTED', 'comment': comment},
                success: function (data) {
                    if (data.code == 200) {
                        $('#reject-modal').modal("hide");

                        $('.modal-backdrop').css({'display': 'None'});
                        //接单拒单隐藏
                        $('.order-operate' + order_id).hide();
                        //订单状态
                        $('#' + order_id).text('已拒单');
                    }
                }
            });
        })
    });
});