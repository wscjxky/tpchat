define(['jquery', 'template', 'md5', 'director'], function ($, Template) {
        //ajax响应基类
        function Ajax_response(msgTitle) {
            this.msgTitle = msgTitle;
            this.Check_response = function (bSuccess, response) {
                if (!bSuccess)
                    alertState(this.msgTitle + "失败,网络异常", "failed");
                else if (!isResponseDataAvailable(response)) {
                    alert(this.msgTitle + "失败.问题描述:" + response.errorMsg, "failed");
                    bSuccess = false;
                }
                else
                    alertState(msgTitle + "成功", "success");
                this.Cb_response(bSuccess, response);
            };
            this.Cb_response = function (bSuccess, response) {
            }
        }

        //Signup功能类
        function Signup() {
            this.userInfo = {
                UserName: "",
                Password: "",
                IdentityCode: "",
                CompanyName: "",
                Address: "",
                License: "",
                LicenseAttachment: "",
                UserIdentity: "",
                RealName: "",
                CellPhone: ""
            };
            //获取验证码
            this.Get_identityCode = function (userName, ajax_cb) {
                $.ajax({
                    type: "POST",
                    dataType: "json",
                    contentType: "application/json",
                    url: "/cloud/getIdentityCode",
                    data: JSON.stringify({Email: userName}),
                    success: function (response) {
                        ajax_cb.Check_response(true, response);
                    },
                    error: function () {
                        ajax_cb.Check_response(false, "");
                    }
                });
            };

            //检查email是否被使用
            this.Check_userName_unique = function (userName, ajax_cb) {
                $.ajax({
                    url: "/cloud/checkName",
                    type: "POST",
                    data: {Email: userName},
                    success: function (response) {
                        ajax_cb.Check_response(true, response);
                    },
                    error: function () {
                        ajax_cb.Check_response(false, "");
                    }
                });
            };

            //普通用户注册
            this.Signup_normal = function (ajax_cb) {
                $.ajax({
                    url: "/cloud/register",
                    type: "POST",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        UserName: this.userInfo.UserName,
                        Password: this.userInfo.Password,
                        IdentityCode: this.userInfo.IdentityCode
                    }),
                    success: function (response) {
                        ajax_cb.Check_response(true, response);
                    },
                    error: function () {
                        ajax_cb.Check_response(false, "");
                    }
                });
            };

            this.Signup_domain = function (ajax_cb) {
                $.ajax({
                    url: "/cloud/register",
                    type: "POST",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        UserName: this.userInfo.UserName,
                        Password: this.userInfo.Password,
                        IdentityCode: this.userInfo.IdentityCode,
                        CompanyName: this.userInfo.CompanyName,
                        License: this.userInfo.License,
                        Address: this.userInfo.Address,
                        RealName: this.userInfo.RealName,
                        CellPhone: this.userInfo.CellPhone,
                        LicenseAttachment: this.userInfo.LicenseAttachment
                    }),
                    success: function (response) {
                        ajax_cb.Check_response(true, response);
                    },
                    error: function () {
                        ajax_cb.Check_response(false, "");
                    }
                });
            };
        }

        var signupImpl = new Signup();

        function checkBaseInfo() {
            var activePanel = $('#base_signup_panel').find('.active');
            var userName = activePanel.find('.base_username').val();
            var pwd = activePanel.find('.base_password').val();
            var repeatPwd = activePanel.find('.base_password_again').val();
            var identityCode = activePanel.find('.base_identityCode').val();
            var bCheck = activePanel.find('.base_protocol').is(":checked");
            if (userName == "") {
                alert("用户名不能为空!");
                return false;
            }
            else if (userName.indexOf('@') < 0) {
                alert("邮箱格式错误！");
                return false;
            }
            if (pwd == "") {
                alert("密码不能为空!");
                return false;
            }
            if (pwd != repeatPwd) {
                alert("前后密码不一致!");
                return false;
            }
            if (identityCode == "") {
                alert("请填写邮箱验证码!");
                return false;
            }
            if (!bCheck) {
                alert("请同意协议!");
                return false;
            }
            return true;
        }

        function checkAdvanceInfo() {
            var activePanel = $('#domain_panel').find('.active');
            var companyName = activePanel.find('domain_company').val();
            var license = activePanel.find('domain_id').val();
            var address = activePanel.find('domain_address').val();
            var realName = activePanel.find('domain_man').val();
            var cellPhone = activePanel.find('domain_phone').val();
            if (companyName == "") {
                alert("企业名不能为空!");
                return false;
            }
            if (license == "") {
                alert("营业执照/身份证号不能为空!");
                return false;
            }
            if (address == "") {
                alert("地址不能为空!");
                return false;
            }
            if (realName == "") {
                alert("联系人不能为空!");
                return false;
            }
            if (cellPhone == "") {
                alert("联系人电话不能为空!");
                return false;
            }
            return true;
        }

        function domain_signup_first() {
            var tem = Template.get('template/signup/signup_next.html');
            var test = tem();
            $('#pageContent').html($.trim(test));
            $(".signup_submit").unbind('clicked').click(function () {
                domain_signup_second();
            });
            $("#team_file_upload").uploadify({
                'buttonText': '上传身份证',
                'hideButton': true,
                'wmode': 'transparent',
                'swf': "script/uploadify/uploadify.swf",
                'height': 34,
                'uploader': "/cloud/uploadLicenseFile" + "?Id=0",
                'onUploadSuccess': function (file, data, response) {
                    var obj = JSON.parse(data);
                    if (obj.errorMsg == undefined) {
                        $('#teamUploadedList').append('<div>' + obj[0].Name + '[未提交]</div>');
                    } else {
                        alertState("上传文件失败，错误信息：" + obj.errorMsg, "failed");
                    }
                    signupImpl.userInfo.LicenseAttachment = obj;
                },
                onUploadProgress: function (file, bytesUploaded, bytesTotal, totalBytesUploaded, totalBytesTotal) {
                    var curPos = parseInt(totalBytesUploaded / bytesTotal * 100);
                    alertState("\"" + file.name + "\"上传中,总共需要上传" + bytesTotal + "字节,已上传" + totalBytesUploaded + '字节 [' + curPos + "%]", "info");
                },
                onUploadError: function (file, errorCode, errorMsg) {
                    alertState("上传文件失败，错误信息：" + errorMsg, "failed");
                }
            });
            $("#company_file_upload").uploadify({
                'buttonText': '上传营业执照',
                'hideButton': true,
                'wmode': 'transparent',
                'swf': "script/uploadify/uploadify.swf",
                'height': 34,
                'uploader': "/cloud/uploadLicenseFile" + "?Id=0",
                'onUploadSuccess': function (file, data, response) {
                    var obj = JSON.parse(data);
                    if (obj.errorMsg == undefined) {
                        $('#companyUploadedList').append('<div>' + obj[0].Name + '[未提交]</div>');
                    } else {
                        alertState("上传文件失败，错误信息：" + obj.errorMsg, "failed");
                    }
                    signupImpl.userInfo.LicenseAttachment = obj;
                },
                onUploadProgress: function (file, bytesUploaded, bytesTotal, totalBytesUploaded, totalBytesTotal) {
                    var curPos = parseInt(totalBytesUploaded / bytesTotal * 100);
                    alertState("\"" + file.name + "\"上传中,总共需要上传" + bytesTotal + "字节,已上传" + totalBytesUploaded + '字节 [' + curPos + "%]", "info");
                },
                onUploadError: function (file, errorCode, errorMsg) {
                    alertState("上传文件失败，错误信息：" + errorMsg, "failed");
                }
            });
        }

        function domain_signup_second() {
            if (!checkAdvanceInfo())
                return;
            var cb_signup = new Ajax_response("用户注册");
            cb_signup.Cb_response = function (bSuccess, response) {
                if (!bSuccess)
                    return;
                var tem = Template.get('template/signup/signup_domain_success.html');
                var test = tem();
                $('#pageContent').html($.trim(test));
            };
            var activePanel = $('#domain_panel').find('.active');
            signupImpl.userInfo.CompanyName = activePanel.find('.domain_company').val();
            signupImpl.userInfo.License = activePanel.find('.domain_id').val();
            signupImpl.userInfo.Address = activePanel.find('.domain_address').val();
            signupImpl.userInfo.RealName = activePanel.find('.domain_man').val();
            signupImpl.userInfo.CellPhone = activePanel.find('.domain_phone').val();
            signupImpl.Signup_domain(cb_signup);
        }

        function normal_signup() {
            var cb_signup = new Ajax_response("用户注册");
            cb_signup.Cb_response = function (bSuccess, response) {
                if (!bSuccess)
                    return;
                var tem = Template.get('template/signup/signup_user_success.html');
                var test = tem();
                $('#pageContent').html($.trim(test));
            };
            signupImpl.Signup_normal(cb_signup);
        }

        function base_signup() {
            if (!checkBaseInfo())
                return;

            var activePanel = $('#base_signup_panel').find('.active');
            var cb = new Ajax_response("检验邮箱");
            cb.Cb_response = function (bSuccess, response) {
                if (!bSuccess)
                    return;
                if (!response['bValidName']) {
                    alert("邮箱已被使用");
                    return;
                }
                signupImpl.userInfo.UserName = activePanel.find('.base_username').val();
                signupImpl.userInfo.Password = $.md5(activePanel.find('.base_password').val());
                signupImpl.userInfo.IdentityCode = activePanel.find('.base_identityCode').val();
                if ($('#usersignup_panel').hasClass('active'))
                    normal_signup();
                else
                    domain_signup_first();
            };
            signupImpl.Check_userName_unique(activePanel.find('.base_username').val(), cb);
        }

        function get_identityCode() {
            var activePanel = $('#base_signup_panel').find('.active');
            if (activePanel.find('.base_username').val() == "") {
                alert("用户名不能为空!");
                return;
            }
            var cb = new Ajax_response("获取验证码");
            cb.Cb_response = function (bSuccess, response) {
                if (bSuccess)
                    activePanel.find('.base_identityCode').val(response.IdentityCode);
            };
            signupImpl.Get_identityCode(activePanel.find('.base_username').val(), cb);
        }

        function SignupInit() {
			$('#Logout').text("我有账号");
			$('#Logout').addClass("btn btn-success");
			$('#Logout').css("margin-top","-4px");
			$('#Logout').click(function(){
				location.href="index.html";
			});
			
            var tem = Template.get('template/signup/signup_index.html');
            var test = tem();
            $('#pageContent').html($.trim(test));
			
            //注册行为
            $(".signup_submit").unbind('clicked').click(function () {
                base_signup();
            });
            //发送验证码行为
            $(".send_key").unbind('clicked').click(function () {
                get_identityCode();
            });
        }

        var signup_interface = {};
        signup_interface.pageRouter = {
            '/signupPage': SignupInit
        };
        return signup_interface;
    }
);