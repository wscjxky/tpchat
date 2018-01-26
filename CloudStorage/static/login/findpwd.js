$('header').show();
$('#FindPwdSendIdentityCode').unbind('clicked').click(function () {
    $.ajax({
        url: 'GetPwdIdentityCode',
        type: "POST",
        data: {Email: $('[name=email]').val()},
        success: function (data) {
            if(data.bSend)
                $('#sendstatus').text('发送成功!');
            else{
                $('[name=email-error]').text(data.ErrorInfo);
            }
        },
        error: function () {
            alert('网络连接异常，请检查');
        }
    });
});
