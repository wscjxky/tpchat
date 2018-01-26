$('header').show();
$('[name=confirm-pwd]').blur(function(){
    if($('[name=pwd]').val()!=$(this).val())
        $('[name=confirm-pwd-error]').text('两次输入的密码不一致');
    else
        $('[name=confirm-pwd-error]').text('');
});

$('[name=email]').blur(function(){
    $('[name=email-error]').css('color','red');
    if($(this).val().indexOf('@')==-1){
        $('[name=email-error]').text('请输入正确的邮箱')
        return;
    }else
        $('[name=email-error]').text('')
    $.ajax({
        url:'CheckEmail',
        type: "POST",
        data: {Email:$(this).val()},
        success: function (data) {
            if(data=='true')
                $('[name=email-error]').text('可以使用').css('color','green');
            else
                $('[name=email-error]').text('该邮箱已被使用');
        },
        error: function () {
            alert('网络连接异常，请检查');
        }
    });
});
$('#SendIdentityCode').unbind('clicked').click(function () {
    $.ajax({
        url: 'GetIdentityCode',
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
