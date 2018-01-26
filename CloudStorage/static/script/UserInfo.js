define(['jquery', 'template', 'storage', 'JcropWarp'], function ($, Template, Storage, JcropWarp) {
    Template.helper("ParseTime", function (date) {
        var d = new Date(date);
        return d.Format("yyyy-MM-dd hh:mm");
    });
    Template.helper("FileName", function (path) {
        var pos = path.lastIndexOf('/');
        if (pos != -1)
            return path.substr(pos + 1, path.length);
        return path;
    });
    function UserInfo() {
        $.ajax({
            type: "POST",
            url: "/cloud/getUserInfo",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({}),
            cache: false,
            error: errorFunction,
            success: function(data){
                var tem = Template.get('template/usercard/usercard.html');
                var test = tem(data);
                var Portrait = data.Domain.Portrait;
                var left = 0, right = 0, top = 0, bottom = 0;
                $('#pageContent').html($.trim(test));
                $("#modifyUserInfo").on('click',function () {       //修改名片
                    $("#PostUserInfo").show();
                    $("#CancelModify").show();
                    $("#modifyUserInfo").hide();
                    jInstance.startSelect();
                    textin(data);
                });
                var jInstance = JcropWarp();
                jInstance.init(Portrait, $('#portrait-area'), function(p, l, t, r, b){
                    Portrait = p;
                    left = l;
                    top = t;
                    right = r;
                    bottom = b;
                });
                function textin(data){
                    $('.info-list').hide();
                    $('.info-edit').addClass("form-control").css('display','block');
                    $('#NickName-edit').val(data.NickName).show();
                    $('#CellPhone-edit').val(data.CellPhone).show();
                    $('#RealName-edit').val(data.RealName).show();
                    $('#portrait_part').show();
                    if (data.Domain.Status == 2){
                        $('#CompanyName-edit').val(data.Domain.CompanyName).show();
                        $('#Address-edit').val(data.Domain.CompanyAddr).show();
                        $('#License-edit').val(data.Domain.CompanyLicense).show();
                        $('#CompanyCelPhone-edit').val(data.Domain.CompanyCelPhone).show();
                        $('#CompanyEmail-edit').val(data.Domain.CompanyEmail).show();
                        $('#CompanyPhone-edit').val(data.Domain.CompanyPhone).show();
                        $('#CompanyFax-edit').val(data.Domain.CompanyFax).show();
                        $('#DomainName-edit').val(data.Domain.DomainName).show();
                    }
                    $("#userInfo-intro").hide();

                    $("#CancelModify").on('click',function(){
                        UserInfo();
                    });
                    $("#PostUserInfo").on('click',function(){
                        modifyUserInfo();
                    });
                }
                function modifyUserInfo(){
                    var param = {
                        CellPhone : $('#CellPhone-edit').val(),
                        NickName : $('#NickName-edit').val(),
                        RealName : $('#RealName-edit').val(),
                        Portrait: Portrait,
                        left: left,
                        right: right,
                        top: top,
                        bottom: bottom
                    };
                    if (data.Domain.Status == 2){
                        $.extend(param, {
                            CompanyName: $('#CompanyName-edit').val(),
                            CompanyAddr: $('#Address-edit').val(),
                            CompanyLicense: $('#License-edit').val(),
                            CompanyCelPhone: $('#CompanyCelPhone-edit').val(),
                            CompanyEmail: $('#CompanyEmail-edit').val(),
                            CompanyPhone: $('#CompanyPhone-edit').val(),
                            CompanyFax: $('#CompanyFax-edit').val(),
                            DomainName: $('#DomainName-edit').val()
                        })
                    }
                    $.ajax({
                        type: "POST",
                        url: "/cloud/modifyUserInfo",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify(param),
                        error: function(){
                            alert("修改信息发生错误！请重试");
                        },
                        success: function(){
                            if (!isResponseDataAvailable(data)) {
                                alertState("域用户登录失败.问题描述:" + data.errorMsg, "failed");
                                return;
                            }
                            UserInfo();
                        }
                    });
                }
                $("#modifypassword").unbind('clicked').click(function (e) {
                    if($("#reNewPwd").val()!=$("#NewPassword").val()){
                        alert("两次输入的新密码不一致");
                        return;
                    }
                    if($("#Password").val()==$("#NewPassword").val()){
                        alert("新密码不能与原密码相同");
                        return;
                    }
                    $.ajax({
                        type: "POST",
                        url: "/cloud/modifyPassword",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            Password: $("#Password").val(),
                            NewPassword: $("#NewPassword").val()
                        }),
                        error: function () {
                            alert("发生错误！请重试");
                        },
                        success: function (response) {
                            if (!isResponseDataAvailable(response)) {
                                alert(response.errorMsg);
                                return;
                            }
                            alert("修改密码成功！");
                        }
                    });
                });
            }
        });
        function errorFunction() {
            alert("读取信息发生错误！");
        }
    }

    var UserInfo_interface = {};
    UserInfo_interface.pageRouter = {
        '/UserInfoPage': UserInfo
    }
    return UserInfo_interface
});