$(document).ready(function () {
    $('#create').click(function () {
        var modaldaig = $('#edtdep');

        modaldaig.modal('show')
    });

    $('#save').on('click',function () {
        var modaldaig = $('#edtdep');
        $.post(
                "/hr/dep/",
                $('form#modaldepedit').serialize(),
                function(data){
                    if(data.code === 0){
                         window.location.reload()
                    } else {
                        var mtoasttype = $('.toast-header');
                        var mtoasttitle = $('#toast-title');
                        var mtoastmsg = $('#toast-msg');

                        mtoasttype.addClass('bg-warning');
                        mtoasttitle.text('警告:');
                        mtoastmsg.text(data.data);
                        $('#showtoast').toast('show');
                    }
                }
            );
        modaldaig.modal('hide')
    });

    $('button[data-action="delete"]').on('click',function () {
        var cardid = $(this).data('pid');
        $.post(
            "/hr/dep/",
            {"act": "delete",
            "pid": cardid},
            function(data){
                if(data.code === 0){
                    window.location.reload()
                } else {
                    var mtoasttype = $('.toast-header');
                    var mtoasttitle = $('#toast-title');
                    var mtoastmsg = $('#toast-msg');

                    mtoasttype.addClass('bg-warning');
                    mtoasttitle.text('警告:');
                    mtoastmsg.text(data.data);
                    $('#showtoast').toast('show');
                }
            }
            );
    });

    // $('#showtoast').on('show.bs.toast',function (event) {
    //     var modal = $(this);
    //     modal.find('#toast-title').text('kkkkkkkk')
    // })

    $('#showtoast').on('hidden.bs.toast',function (event) {
        var modal = $(this);
        modal.find('.toast-header').removeClass('bg-success');
        modal.find('.toast-header').removeClass('bg-warning');
    })
});