define(['jquery', 'template', 'director', 'md5'], function ($, Template) {
    function loginPage() { //加载登录界面
        var tem = Template.get('template/login.html');
        var test = tem({path:$("#login_image").val()});
        $('#pageContent').html($.trim(test));

        $(document).keydown(function (e) { //挂载快捷键
            if (e.keyCode == 13||e.keyCode ==39) {
                login ($("#normal_user_tab").hasClass("active")?0:1);
            }
        });

        $(".login").unbind('click').click(function () { //挂载按钮响应
            $(this).html('<div class="spinner"><div class="rect1"></div><div class="rect2"></div><div class="rect3"></div><div class="rect4"></div><div class="rect5"></div></div>');
            login ($("#normal_user_tab").hasClass("active")?0:1);
        });
    }

    function login(type) { //登录
        var param;

        if(type==0) //普通用户
            param = { UserName: $('#normal_userName').val(), Password: $.md5($('#normal_userPwd').val())};
        else if( type==1) //域用户
            param = { UserName: $('#domain_userName').val(), Password: $.md5($('#domain_userPwd').val()), DomainName: $("#domain_name").val()};

        $.ajax({
            type: "POST",
            url: "/cloud/login",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function (data) {
                if ( isResponseDataAvailable(data)) {
                    $().tryRetrieveSession(function(bSuccess){
                        if (bSuccess){
                            if (document.referrer == window.location.origin + "/session")
                                window.history.go(-2);
                            else
                                location.href = "/session#/requirementPage";
                        }
                    });
                }
                else{
                    alert(data.errorMsg);
                }

                $(".login").html("登录");
            },
            error: function () {
                alertState("网络异常", "failed");
                $(".login").html("登录");
            }
        });
    }

    var login_interface = {};
    login_interface.pageRouter = {
        '/loginPage': loginPage
    };
    return login_interface;
});