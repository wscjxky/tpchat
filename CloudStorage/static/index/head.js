$("#Logout").unbind('click').click(function () {
    $.cookie('DBToken','',{expires: -1,path:'/'});
    $.cookie('newReq','',{expires: -1,path:'/'});
    $.cookie('category_1','',{expires: -1,path:'/'});
    $.cookie('category_2','',{expires: -1,path:'/'});
    $.cookie('producerDomain','',{expires: -1,path:'/'});
    location.reload();
});
//$('.index-submit-requirement').unbind('click').click(function(){
//    self.location='/submit';
//});
function CheckLogin(cb){
    $.ajax({
        type: "POST",
        url: "/checkDBToken",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            dbtoken:$.cookie('DBToken')
        }),
        success: function (data) {
            (data.bSuccess)?cb():signin();
        },
        error: function () {
            alert("登录失败，网络异常");
        }
    });
    function signin(){
        $('#signin').modal('show')
        $('#btn-signin').unbind('click').click(function(){
            $.ajax({
                type: "POST",
                url: "/SignIn",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    UserName: $('#normal_userName').val(),
                    Password: $.md5($('#normal_userPwd').val()),
                    DomainName: $("#domain_name").val(),
                    DomainUserName:$("#domain_userName").val(),
                    DomainPassword:$.md5($("#domain_userPwd").val())
                }),
                success: function (data) {
                    if (!data.result) {
                        alert(data.info);
                        return;
                    }
                    $('#signin').modal('hide')
                    cb();
                },
                error: function () {
                    alert("登录失败，网络异常");
                }
            });
        })
    }
}
