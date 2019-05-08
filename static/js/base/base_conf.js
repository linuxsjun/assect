$(document).ready(function () {
    $('[data-toggle="savecorpid"]').on('click',function () {
        var corpid;
        corpid = $('#corpid').val();
        $.post(
            "/corpid/",
            {corpid: corpid},
            function (context, status) {

            });
    })
});