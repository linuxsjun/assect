$(document).ready(function () {
    $('#save-crid').click(function () {
    // corpsecret
        var corpsecretstr;
        corpsecretstr = $('#inputcrid').val();
        $.post(
            "/hr/corpsecret/",
            {corpsecret: corpsecretstr},
            function (context, status) {

            });
    });

    $('button[data-action="syncfromwx"]').click(function () {
    // corpsecret
        var corpsecretstr;
        corpsecretstr = $('#inputcrid').val();
        $.post(
            "/hr/syncfromwx/",
            {corpsecret: corpsecretstr},
            function (context) {
                if(context.code === 0){
                    var k = $('#showtoast');
                    var mtoasttype = $('.toast-header');
                    var mtoasttitle = $('#toast-title');
                    var mtoastmsg = $('#toast-msg');
                    // Todo 没有报错刷新网页，有报错显示报错
                    // window.location.reload()
                    mtoasttype.addClass('bg-success');
                    mtoasttitle.text('通知:');
                    mtoastmsg.text('同步员工信息成功');
                    k.toast('show');
                } else {
                    mtoasttype.addClass('bg-warning');
                    mtoasttitle.text('警告:');
                    mtoastmsg.text(context.data);
                   k.toast('show');
                }
            });
    })
});