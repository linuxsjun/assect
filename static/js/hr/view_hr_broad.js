$(document).ready(function () {
    $('[data-toggle="gethr"]').on('click',function () {
        var $btn = $(this).button('loading');
        $.ajax({
            url:"/hr/gethr",
            type:"GET",
            data:{
                "act":'gettoken'
            },
            success:function (data) {
                console.log(data)
            }
        });
        $btn.button('reset')
    });

    $('#kkkk').click(function () {
        $('#showtoast').toast('show')
    })
});