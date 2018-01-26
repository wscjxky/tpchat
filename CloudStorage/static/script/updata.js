define(['jquery','template','storage', 'JcropWarp'],function($,Template,Storage,JcropWarp){
    Template.helper("FloatFormat", function (float) {
        return Math.round(float*100)/100;
    });
    Template.helper("LicenseFormat",function(License){
        s = "";
        l = License.length;
        for(i=0;i<4;i++)
            s = s+License[i];
        return s+'*******'+License[l-4]+License[l-3]+License[l-2]+License[l-1];
    });
    Template.helper("ParseTime3", function (date) {
        var d = new Date(date);
        return d.Format("yyyy-MM-dd");
    });
    function updataInit(){
        $.ajax({
            type: "POST",
            url: "/share/getUserSize",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
            }),
            error: function(){
                alert("发生错误！请重试");
            },
            success: function(data){
                var tem = Template.get('template/updata/updata.html');
                var test = tem({user:data});
                $('#pageContent').html($.trim(test));

                $("#gotoUserSettingPage").unbind('clicked').click(function(){
                    UserSetting();
                });
                $('#tovip-submit').unbind('clicked').click(function(){
                    tovip(data);
                });
                $('#extend').unbind('clicked').click(function(){
                    extend(data);
                });
                $('#ShowWall').unbind('clicked').click(function(){
                    ShowWall(data);
                });
                $('#Money').unbind('clicked').click(function(){
                    Money(data);
                });
                $('#updata-index').unbind('clicked').click(function(){
                    updataInit();
                });
                $('#logCenter').unbind('clicked').click(function(){
                    logCenterInstance.init();
                });
//                $('#SelfSetting').unbind('clicked').click(function(){
//                    logCenterInstance.init();
//                });
            }
        });
        function UserSetting(){
            function GetDomainInfo(cb){
                $.ajax({
                    type: "POST",
                    url: "/share/getDomainInfo",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({}),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("获取域信息失败.问题描述: " + data.errorMsg, "info");
                            return;
                        }
                        parseData(data);
                        cb(data);
                    },
                    error: function () {
                        alertState("获取域信息失败，网络异常", "failed");
                    }
                });
            }
            function parseData(data){
                cache_ = {
                    id: data.Id,
                    name: data.DomainName,
                    ownerUserId: data.OwnerUserId,
                    roles: {},
                    users: {},
                    info:data
                };
                //域角色信息
                $(data.Roles).each(function (i, role) {
                    cache_.roles[role.Id] = role;
                });
                //域用户信息
                $(data.Users).each(function (i, data_userInfo) {
                    var userInfo;
                    userInfo = {
                        id: data_userInfo.Id,
                        name: data_userInfo.NickName,
                        domainName: data_userInfo.DomainName,
                        roles: {}
                    };
                    //用户角色信息
                    $(data_userInfo.Roles).each(function (j, data_userRole) {
                        var roleInfo = cache_.roles[data_userRole.Id];
                        userInfo.roles[data_userRole.Id] = {
                            id: data_userRole.Id,
                            name: roleInfo.Name
                        };
                        userInfo.domainAdmin = userInfo.domainAdmin | roleInfo.DomainAdmin;
                    });
                    cache_.users[data_userInfo.Id] = userInfo;
                });
            }
            var Family = {
                create: function(){
                    var family = {};
                    family.show = function(bAnimate){
                        GetDomainInfo(function(){
                            _init_frame(bAnimate);
                            family.initUserList();
                        });
                    };
                    family.deleteUser = function(userId, cb){
                        var domainModifyInfo = {
                            Id: cache_.id,
                            Name: cache_.name,
                            Users: [
                                {
                                    Id: userId,
                                    Operate: "del"
                                }
                            ]
                        };
                        $.ajax({
                            type: "POST",
                            url: "/share/modifyDomainInfo",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(domainModifyInfo),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("删除域用户失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                cb(data);
                                alertState("删除域用户完成", "success");
                            },
                            error: function () {
                                alertState("删除域用户失败，网络异常", "failed");
                            }
                        });
                    };
                    family.modifyUser = function(userId, originalRoles){
                        $("#domain_user_modify_dialog").modal('hide');
                        var rolesCount = 0;
                        var modifyRoles = [];
                        //获取设置的角色信息
                        $("#domain_user_modify_role_selector").children().each(function (i, tr) {
                            var check = $(tr).find(".role_check").find("input");
                            var roleId = parseInt($(tr).find(".role_id").text());
                            if (check.is(':checked') && originalRoles[roleId] == null) {
                                modifyRoles[rolesCount++] = {Id: roleId, Operate: "add"};
                            }
                            else if (!check.is(':checked') && originalRoles[roleId] != null) {
                                modifyRoles[rolesCount++] = {Id: roleId, Operate: "del"};
                            }
                        });
                        var userInfo = {
                            Id: userId,
                            Operate: "modify",
                            DomainName: $("#domain_user_modify_domainName").val(),
                            Roles: modifyRoles
                        };
                        if ($("#domain_user_modify_domainPwd").val() != "")
                            userInfo.Password = $.md5($("#domain_user_modify_domainPwd").val());
                        var domainModifyInfo = {
                            Id: cache_.id,
                            Name: cache_.name,
                            Users: [ userInfo ]
                        };
                        $.ajax({
                            type: "POST",
                            url: "/share/modifyDomainInfo",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(domainModifyInfo),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("修改域用户信息失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                parseData(data);
                                family.initUserList();
                                alertState("修改域用户信息完成", "success");
                            },
                            error: function () {
                                alertState("修改域用户信息失败，网络异常", "failed");
                            }
                        });
                    };
                    family.initModifyUser = function(userId){
                        var tem = Template.get('template/domain/domain_user_modify_dialog.html');
                        var test = tem(cache_);
                        $('#domain_user_modify_dialog').html($.trim(test));
                        var originalRoles = {};
                        $.each(cache_.users[userId].roles, function (i, role) {
                            originalRoles[role.id] = role.id;
                        });
                        //设置用户角色显示
                        $("#domain_user_modify_role_selector").children().each(function (i, tr) {
                            var check = $(tr).find(".role_check").find("input");
                            var roleId = parseInt($(tr).find(".role_id").text());
                            if (originalRoles[roleId] != null)
                                check.attr("checked", "checked");
                            //如果用户是域所有者并且该角色为管理员角色，则disable该角色check功能
                            if (cache_.roles[roleId].domainAdmin && cache_.ownerUserId == userId)
                                check.attr("disabled", "disabled");
                        });
                        $("#domain_user_modify_commit").unbind("click").click(function () {
                            family.modifyUser(userId, originalRoles);
                        });
                        $("#domain_user_modify_domainName").val(cache_.users[userId].domainName);
                        $("#domain_user_modify_dialog").modal();
                    };
                    family.searchUser = function(username){
                        $.ajax({
                            type: "POST",
                            url: "/share/searchUser",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({KeyWord: username}),
                            success: function (data) {
                                var tem = Template.get('template/domain/searchUserList.html');
                                var test = tem(data);
                                $("#domain_user_add_search_after").html($.trim(test));
                                if (!isResponseDataAvailable(data)) {
                                    alertState("查找用户失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                alertState("查找用户完成", "success");
                            },
                            error: function () {
                                alertState("查找用户失败，网络异常", "failed");
                            }
                        });
                    };
                    family.addUser = function(){
                        $("#domain_user_add_dialog").modal('hide');
                        //查找是否有选中用户
                        var userId = -1;
                        $("#searchResult").children().each(function (i, tr) {
                            var check = $(tr).find(".searchUser_check").find("input");
                            if (check.is(':checked')) {
                                userId = parseInt($(tr).find(".searchUser_id").text());
                                return false;
                            }
                        });
                        //获取设置的角色信息
                        var roleCount = 0;
                        var selectRoles = [];
                        $("#domain_user_add_role_selector").children().each(function (i, tr) {
                            var roleId = parseInt($(tr).find(".role_id").text());
                            if ($(tr).find(".role_check").find("input").is(':checked')) {
                                selectRoles[roleCount++] = {Id: roleId, Operate: "add"};
                            }
                        });
                        var userPwd = $.md5($("#domain_user_add_userDomainPwd").val());
                        var UserInfo = {
                            Operate: "add",
                            DomainName: $("#domain_user_add_userDomainName").val(),
                            Password: userPwd,
                            Roles: selectRoles
                        };
                        if (userId != -1) {
                            UserInfo.Id = userId;
                        }
                        var domainModifyInfo = {
                            Id: cache_.id,
                            Name: cache_.name,
                            Users: [
                                UserInfo
                            ]
                        };
                        $.ajax({
                            type: "POST",
                            url: "/share/modifyDomainInfo",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(domainModifyInfo),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alert('添加企业用户失败'+data.errorMsg+'，请换个名称');
                                    return;
                                }
                                parseData(data);
                                family.initUserList();
                                alertState("添加域用户完成", "success");
                            },
                            error: function () {
                                alertState("添加域用户失败，网络异常", "failed");
                            }
                        });
                    };
                    family.initAddUser = function(){
                        var tem = Template.get('template/domain/domain_user_add_dialog.html');
                        var test = tem(cache_);
                        $('#domain_user_add_dialog').html($.trim(test));
                        //搜索用户键盘回车事件
                        var searchInput = $("#domain_user_add_search_input");
                        searchInput.bind('keyup', function (event) {
                            if (event.keyCode == 13)
                                family.searchUser(searchInput.val());
                        });
                        //搜索用户按钮事件
                        $("#domain_user_add_search_btn").unbind("click").click(function () {
                            family.searchUser(searchInput.val());
                        });
                        //确认添加按钮事件
                        $("#domain_user_add_commit").unbind("click").click(function () {
                            family.addUser();
                        });
                        $("#domain_user_add_dialog").modal();
                    };
                    function _init_frame(bAnimate){
                        var tem = Template.get('template/domain/userSetting.html');
                        var test = tem({Domain: cache_.info});
                        if (bAnimate)
                            $('#updata-content').html($.trim(test));
                        else
                            $('#updata-content').html($.trim(test));
                        $("#roleSetting").unbind("click").click(function () {
                            role_instance.show(true);
                        });
                        //添加用户或角色按钮事件绑定
                        $("#addUser").unbind("click").click(function () {
                            family.initAddUser();
                        });
                        var Portrait = cache_.info.Portrait;
                        var left = 0, right = 0, top = 0, bottom = 0;
                        var jInstance = JcropWarp();
                        jInstance.init(Portrait, $('#portrait_part'), function(p, l, t, r, b){
                            Portrait = p;
                            left = l;
                            top = t;
                            right = r;
                            bottom = b;
                        });
                        jInstance.startSelect();
                        $("#modify-domain-info").unbind("click").click(function(){
                            var param = {
                                Portrait: Portrait,
                                left: left,
                                right: right,
                                top: top,
                                bottom: bottom,
                                CompanyName: $('#CompanyName-edit').val(),
                                CompanyAddr: $('#Address-edit').val(),
                                CompanyLicense: $('#License-edit').val(),
                                CompanyCelPhone: $('#CompanyCelPhone-edit').val(),
                                CompanyEmail: $('#CompanyEmail-edit').val(),
                                CompanyPhone: $('#CompanyPhone-edit').val(),
                                CompanyFax: $('#CompanyFax-edit').val(),
                                DomainName: $('#DomainName-edit').val()
                            };
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
                                    family.initUserList();
                                    alert("保存成功！");
                                }
                            });
                        });
                    }
                    family.initUserList = function(){
                        var tem = Template.get('template/domain/domain_user.html');
                        var test = tem(cache_);
                        $("#domain_user_list").html($.trim(test));
                        $(".domain_user_delete_Btn").unbind("click").click(function (e) {
                            var userId = parseInt($(e.currentTarget).parent().find(".user_id").text());
                            function _cb(data){
                                $(e.currentTarget).parent().remove();
                            }
                            family.deleteUser(userId, _cb);
                        });
                        $(".domain_user_modify_Btn").unbind("click").click(function (e) {
                            var userId = parseInt($(e.currentTarget).parent().find(".user_id").text());
                            family.initModifyUser(userId);
                        });
                    };
                    return family;
                }
            };
            var Role = {
                create: function(){
                    var role = {};
                    role.rights = {};
                    role.curRoleId = 0;
                    role.show = function(bAnimate){
                        var tem = Template.get('template/domain/roleSetting.html');
                        var test = tem({domainName: cache_.name});
                        $('#role').html($.trim(test)).fadeIn();
                        $('#profile').hide();
                        $('#list').hide();
                        _init_roleList();
                        $("#addSomething").unbind("click").click(function () {
                            role.initAddRole();
                        });
                        $("#back_to_userSetting").unbind("click").click(function () {
                            family_instance.show(true);
                        });
                    };
                    role.initAddRole = function(){
                        var tem = Template.get('template/domain/rightSetting.html');
                        var test = tem();
                        $('.roleSetting_panel').html($.trim(test));
                        $.ajax({
                            type: "POST",
                            url: "/share/userRights",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({}),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("获取权限信息失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                _cb_initRights(data, true);
                            },
                            error: function () {
                                alertState("获取权限信息失败，网络异常", "failed");
                            }
                        });
                    };
                    role.save = function(isNew){
                        var param = {};
                        $.each(role.rights, function(i, v){
                            var selector = "";
                            if (v.Leaf){
                                selector = "#rights_leaf_" + v.Id;
                                param[v.Id] = $(selector).find('input[type="checkbox"]').prop('checked');
                            }
                        });
                        $.ajax({
                            type: "POST",
                            url: "/share/saveRole",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                Rights: param,
                                DomainId: cache_.id,
                                CreatorId: cache_.ownerUserId,
                                RoleName: $('.roleSetting_name').val(),
                                bNew: isNew,
                                RoleId: role.curRoleId
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("修改角色失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                _cb_save(data);
                            },
                            error: function () {
                                alertState("修改角色失败，网络异常", "failed");
                            }
                        });
                    };
                    role.deleteRole = function(e){
                        var id = $(e.currentTarget).parent().find(".role_id").text();
                        var domainModifyInfo = {
                            Id: cache_.id,
                            Name: cache_.name,
                            Roles: [
                                {
                                    Id: id,
                                    Name: "",
                                    Operate: "del"
                                }
                            ]
                        };
                        $.ajax({
                            type: "POST",
                            url: "/share/modifyDomainInfo",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(domainModifyInfo),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("删除域角色失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                $(e.currentTarget).parent().remove();
                                parseData(data);
                                _init_roleList();
                                alertState("删除域角色完成", "success");
                            },
                            error: function () {
                                alertState("删除域角色失败，网络异常", "failed");
                            }
                        });
                    };
                    role.initModifyRole = function(e){
                        var id = $(e.currentTarget).parent().find(".role_id").text();
                        role.curRoleId = id;
                        var tem = Template.get('template/domain/rightSetting.html');
                        var test = tem();
                        $('.roleSetting_panel').html($.trim(test));
                        $.ajax({
                            type: "POST",
                            url: "/share/userRights",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({RoleId: id}),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("获取权限信息失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                _cb_initRights(data, false);
                            },
                            error: function () {
                                alertState("获取权限信息失败，网络异常", "failed");
                            }
                        });
                    };
                    function _init_roleList(){
                        var tem = Template.get('template/domain/domain_role.html');
                        var test = tem(cache_);
                        $("#domain_role_list").html($.trim(test));
                        $(".domain_role_delete_Btn").unbind("click").click(function (e) {
                            role.deleteRole(e);
                        });
                        $(".domain_role_modify_Btn").unbind("click").click(function (e) {
                            role.initModifyRole(e);
                        });
                    }
                    function _cb_save(data){
                        GetDomainInfo(function(){
                           role.show(false);
                        });
                    }
                    function _cb_initRights(data, bNew){
                        $.each(data.rights, function(i, v){
                            var tem, t;
                            if (v.Level == 0){
                                tem = Template.get('template/domain/rightSetting_level1.html');
                                t = tem(v);
                                $('.rightSetting_level_1').append($.trim(t));
                            }
                            else{
                                tem = Template.get('template/domain/rightSetting_level2.html');
                                t = tem(v);
                                var selector = "#rights_" + v.ParentId;
                                $(selector).append($.trim(t));
                            }
                        });
                        $.each(data.roleRights, function(i, v){
                            var selector = "#rights_leaf_" + v.RightId;
                            if (v.Checked){
                                $(selector).find('input[type="checkbox"]').prop('checked', true);
                           }
                        });
                        if (!bNew){
                            $(".roleSetting_name").val(cache_.roles[role.curRoleId].Name);
                        }
                        role.rights = data.rights;
                        $('#role_save').unbind("click").click(function () {
                            role.save(bNew);
                        });
                        $('#role_cancel').unbind("click").click(function () {
                            role.show(false);
                        });
                    }
                    return role;
                }
            };
            var role_instance = Role.create();
            var family_instance = Family.create();
            family_instance.show(false);
        }
        function Money(data){
            $.ajax({
                type: "POST",
                url: '/platform/moneySetting',
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                }),
                success: function(platformSetting){
                    var UserId = data.Id;
                    var tem = Template.get('template/updata/Money.html');
                    var bShowApplyMoney = true;
                    if (data.ApplyMoney){
                        $(data.ApplyMoney).each(function(index, value){
                            if (value.Status == 0)
                                bShowApplyMoney = false;
                        })
                    }
                    var test = tem({bShowApplyMoney: bShowApplyMoney, user:data, MemberShipTax: platformSetting.setting.MemberShipTax, domainPrice: platformSetting.domainPrice});
                    $('#updata-content').html($.trim(test));
                    $('#ReBinding').unbind('clicked').click(function(){
                        var test = tem({user:data,Modify:true});
                        $('#updata-content').html($.trim(test));
                        $("#BackUp").unbind('clicked').click(function(){
                            Money(data);
                        });
                        $("#binding-submit").unbind('clicked').click(function(){
                            AlipaySubit();
                        });
                        $("#alipay-BackUp").unbind('clicked').click(function () {
                            Money(data);
                        });
                    });
                    $("#binding-submit").unbind('clicked').click(function(){
                        AlipaySubit();
                    });
                    function AlipaySubit(){
                        $.ajax({
                            type: "POST",
                            url: "/cloud/bindingAccount",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                account:$('#alipay-account').val()
                            }),
                            error: function(){
                                alert("修改信息发生错误！请重试");
                            },
                            success: function(){
                                if (!isResponseDataAvailable(data)) {
                                    alertState("域用户登录失败.问题描述:" + data.errorMsg, "failed");
                                    return;
                                }
                                updataInit();
                            }
                        });
                    }
                    $('#Recharge_tax').unbind('clicked').click(function() {
                        $('#simple_tax_recharge').hide();
                        $('#detail_tax_recharge').slideDown();
                        $("#tax_backup").unbind('clicked').click(function () {
                            $('#simple_tax_recharge').show();
                            $('#detail_tax_recharge').slideUp();
                        });
                        $('#charge-tax').change(function(){
                            var year = parseInt($('#charge-tax').val());
                            $('#tax_amount').text(year * platformSetting.setting.MemberShipTax);
                        });
                        $('#Tax-Recharge-Submit').unbind('clicked').click(function(){
                            createOrder('MemberShipTax', {
                                Year: parseInt($('#charge-tax').val())
                            });
                        });
                    });

                    $('#Recharge').unbind('clicked').click(function(){
                        $('#simple_recharge').hide();
                        $('#detail_recharge').slideDown();
                        $("#BackUp").unbind('clicked').click(function(){
                            $('#detail_recharge').slideUp();
                            $('#simple_recharge').show();
                        });
                        $('#Recharge-Submit').unbind('clicked').click(function(){
                            createOrder('RechargeAccount', {RechargeAccount:$('#charge-account').val()});
                        });
                    });
                    $('#change_price').unbind('clicked').click(function(){
                        $('#domain_price').val($('#domain_price_text').text());
                        $('#simple_domain_price').hide();
                        $('#detail_domain_price').slideDown();
                        $("#price_backup").unbind('clicked').click(function(){
                            $('#detail_domain_price').slideUp();
                            $('#simple_domain_price').show();
                        });
                        $('#price_Submit').unbind('clicked').click(function(){
                            modifyDomainPrice($('#domain_price').val());
                        });
                    });
                    $('#account-apply-submit').unbind('click').click(function(){
                        if(!data.Domain.Alipay){
                            alert('请先绑定支付宝账号');
                            return;
                        }
                        if($('#account-apply').val()) {
                            if ($('#account-apply').val() > data.Domain.Count) {
                                alert('转现金额不得大于平台余额');
                                return;
                            };
                            $.ajax({
                                type: "POST",
                                url: "/platform/applyMoney",
                                dataType: "json",
                                contentType: "application/json",
                                data: JSON.stringify({
                                    account:$('#account-apply').val()
                                }),
                                error: function(){
                                    alert("修改信息发生错误！请重试");
                                },
                                success: function(){
                                    alert('转现申请成功，请耐心等候，我们会在一个工作日内给您回复。');
                                    updataInit();
                                }
                            });
                        }
                    });
                    function modifyDomainPrice(price){
                        var param = {
                            Price: parseFloat(price)
                        };
                        $.ajax({
                            type: "POST",
                            url: '/platform/modifyDomainPrice',
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(param),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("修改竞价信息失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                $('#domain_price_text').text(price);
                                $('#detail_domain_price').hide();
                                $('#simple_domain_price').show();
                            }
                        })
                    }
                    function createOrder(orderType, selfParams){
                        var param = {
                            UserId:UserId,
                            OrderType: orderType
                        };
                        var title;
                        if (orderType == 'RechargeAccount')
                            title = '账号充值服务';
                        else if (orderType == 'MemberShipTax')
                            title = '会员续费服务';
                        $.extend(param, selfParams);
                        $.ajax({
                            type: "POST",
                            url: '/platform/CreateOrder',
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(param),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("支付请求失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                $().alipayProcess(
                                    title,
                                    data.SerialNumber,
                                    data.Id,
                                    data.Amount,
                                    0,
                                    '商影联盟官方账号',
                                    function(bSuccess) {
                                        if (bSuccess)
                                            window.history.go(0);
                                    }
                                );
                            },
                            error: function () {
                                alertState("支付请求失败，网络异常", "failed");
                            }
                        });
                    }
                }
            });
        }
        function ShowWall(user){
            var wall = [];
            var curPortrait = '';
            var left = 0, top = 0, bottom = 0, right = 0, zoneItemPortrait;
            $.ajax({
                type: "POST",
                url: "/share/getWall",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                }),
                error: function () {
                    alert("get失败");
                },
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("失败.问题描述: " + data.errorMsg, "info");
                        return;
                    }
                    var tem = Template.get("template/wall/wall.html");
                    var r = tem({
                        'wall':data.wall,
                        'user':data.user,
                        'category':data.category,
                        'tag_normal':data.tag_normal,
                        'tag_personal':data.tag_personal,
                        'zone_item':data.zone_item,
                        'zone_pic':data.zone_pic,
                        'priceRange': data.priceRange,
                        'zone_banner': data.zone_banner
                    });
                    user = data.user;
                    $('#updata-content').html(r);
                    $('.btn-compile').unbind("clicked").click(function(e) {
                        var EditVideoId = $(this).siblings('input').val();
                        var tem = Template.get("template/wall/editZoneItem.html");
                        var tmp = $(this).find('input').val();
                        var tags = data.zone_item[tmp].Object.Tag;
                        var tagsArray = tags.split(" ");
                        var r = tem({
                            'user':data.user,
                            'category':data.category,
                            'category_1':data.zone_item[tmp].Object.Category_1,
                            'category_2':data.zone_item[tmp].Object.Category_2,
                            'tag_normal':data.tag_normal,
                            'tag_personal':data.tag_personal,
                            'priceRange': data.priceRange,
                            'tags':tagsArray,
                            'zone_item':data.zone_item[tmp]
                        });
                        $('#EditItem').html(r);
                        $('#category_1').blur(function(){
                            $('#category_2').html('');
                            var category_1 = $('#category_1').val();
                            if(category_1 != '')
                                for (var item in data.category) {
                                    if (data.category[item].ParentId == category_1)
                                        $('#category_2').html($('#category_2').html()+
                                            '<option value="' + data.category[item].Id + '">' + data.category[item].Name + '</option>'
                                        );
                                }
                        });
                        $('#addtag_1').unbind("click").click(function(e) {
                            if($('#tag_normal').val()!=''){
                                $('#tag_room').html($('#tag_room').html()+
                                    '<span class="label label-primary" style="margin:5px;display:inline-block"><div style="display:inline-block">'+
                                    $('#tag_normal')[0][$('#tag_normal').val()].innerHTML+
                                    '</div><span style="cursor:pointer;margin-left:5px"' +
                                    'onclick="$(this).parent().remove();"'+
                                    '>&times;</span></span>'
                                )
                            }
                        });
                        $('#addtag_2').unbind("click").click(function(e) {
                            if($('#tag_personal').val()!=''){
                                $('#tag_room').html($('#tag_room').html()+
                                    '<span class="label label-primary" style="margin:5px;display:inline-block"><div style="display:inline-block">'+
                                    $('#tag_personal').val()+
                                    '</div><span style="cursor:pointer;margin-left:5px"' +
                                    'onclick="$(this).parent().remove();"'+
                                    '>&times;</span></span>'
                                )
                            };
                        });
                        $('#Save').unbind('click').click(function(){
                            if(!$('#EditVideoDescription').val()){
                                alert('视频描述不能为空');
                                return;
                            };
                            if(!$('#category_1').val() || !$('#category_2').val()){
                                alert('视频分类不能为空');
                                return;
                            };
                            if(price = $('#Editprice').val()<0){
                                alert('竞价不能为负值');
                                return;
                            }
                            if($('#Editprice').val())
                                var price = $('#Editprice').val();
                            else
                                var price = 0;
                            var tags=[];
                            for(var tag in $('#tag_room').children().children('div')){
                                if(!$('#tag_room').children().children('div')[tag].innerText)break;
                                tags += $('#tag_room').children().children('div')[tag].innerText + ' ';
                            };
                            if(tags.length==0){
                                alert('视频标签不能为空');
                                return;
                            };
                            var TagsArray = tags.split(" ");
                            var RP = parseFloat($('#BasePrice').val())+
                                parseFloat($('#SchemePrice').val())+
                                parseFloat($('#ShotPrice').val())+
                                parseFloat($('#MusicPrice').val())+
                                parseFloat($('#AEPrice').val())+
                                parseFloat($('#ActorPrice').val());
                            var referprice = RP?RP:0;
                            $.ajax({
                                type: "POST",
                                url: "/share/editVideoToZone",
                                dataType: "json",
                                contentType: "application/json",
                                data: JSON.stringify({
                                    FileId:EditVideoId,
                                    DomainId:user.DomainId,
                                    Intro:$('#EditVideoDescription').val(),
                                    Category_1:$('#category_1').val(),
                                    Category_2:$('#category_2').val(),
                                    TagsArray:TagsArray,
                                    Price:price,
                                    Portrait: curPortrait,
                                    ReferPrice: referprice,
                                    bp:$('#BasePrice').val(),
                                    scp:$('#SchemePrice').val(),
                                    shp:$('#ShotPrice').val(),
                                    acp:$('#ActorPrice').val(),
                                    mp:$('#MusicPrice').val(),
                                    aep:$('#AEPrice').val()
                                }),
                                error: function(){
                                    alert("添加失败，请检查网络。");
                                    ShowWall(user);
                                    return;
                                },
                                success:function(data){
                                    if(data.result)
                                        ShowWall(user)
                                    else{
                                        alert('修改失败，请检查网络。');
                                        ShowWall(user)
                                    }
                                }
                            });
                        });
                    });
                    var jInstance = JcropWarp();
                    jInstance.title = '修改图片';
                    jInstance.useAge = 'zoneBG';
                    jInstance.ratio = 4.5;
                    jInstance.init(data.zone_banner, $('#zoneBG_area'), function(p, l, t, r, b){
                        $('#AddZoneBg').unbind('click').click(function(){
                            $.ajax({
                                type: "POST",
                                url: server + "share/addZoneBg",
                                dataType: "json",
                                contentType: "application/json",
                                data: JSON.stringify({
                                    file:p,
                                    DomainId:user.DomainId,
                                    left: l,
                                    top: t,
                                    right: r,
                                    bottom: b
                                }),
                                error: function(){
                                    alert("添加失败，请检查网络。");
                                    ShowWall(user);
                                },
                                success:function(){
                                    ShowWall(user);
                                }
                            });
                        });
                    });
                    jInstance.startSelect();
                    initAddPhotos();
                    function initAddPhotos(){
                        $('.ModifyPicIntro').unbind('click').click(function(){
                            var tmp = $(this).parent().parent();
                            if($(this).parent().find('.glyphicon-pencil').length == 1)
                                $(this).removeClass("glyphicon-pencil").addClass("glyphicon-floppy-disk");
                            else{
                                $(this).removeClass("glyphicon-floppy-disk").addClass("glyphicon-pencil");
                                var text = tmp.find('.PicIntroText').val()
                                var id = $(this).parent().parent().find('.wall-a')[0].id;
                                $.ajax({
                                    type: "POST",
                                    url: "/share/modifyPicIntro",
                                    dataType: "json",
                                    contentType: "application/json",
                                    data: JSON.stringify({
                                        text:text,
                                        id:id
                                    }),
                                    error: function(){
                                        alert("添加失败，请检查网络。");
                                        ShowWall(user);
                                        return;
                                    },
                                    success:function(){
                                         tmp.find('small').find('span')[0].innerText = text;
                                    }
                                });
                            }
                            tmp.find('.wall-a').slideToggle();
                            tmp.find('.PicIntroText').fadeToggle(100).val(tmp.find('small').find('span')[0].innerText);
                        });
                        $('#addwall').unbind("click").click(function(e){
                            Storage.filePickerDialog.open($('#addwall-sel'), function (files) {
                                if (files.length == 0){
                                    $('#addwall-sel').html('');
                                    return;
                                }
                                $.ajax({
                                    type: "POST",
                                    url: "/share/addWall",
                                    dataType: "json",
                                    contentType: "application/json",
                                    data: JSON.stringify({
                                        files:files,
                                        DomainId:user.DomainId
                                    }),
                                    error: function(){
                                        alert("添加失败，请检查网络。");
                                        $('#addwall-sel').html('');
                                    },
                                    success:function(data){
                                        var tem = Template.get("template/wall/photos.html");
                                        var r = tem({
                                            'user':user,
                                            'zone_pic':[data]
                                        });
                                        $('#photos_wall').append(r);
                                        $('#addwall-sel').html('');
                                        initAddPhotos();
                                    }
                                });
                            });
                        });
                        $(".wall-a").mouseover(function (e) {
                            var id = e.currentTarget.id;
                            var a = $(e.currentTarget).find("#wall_cancel").css("font-size","20px");
                            $(e.currentTarget).find("#wall_cancel").unbind("click").click(function(e){
                                $.ajax({
                                    type: "POST",
                                    url: "/share/dropWall",
                                    dataType: "json",
                                    contentType: "application/json",
                                    data: JSON.stringify({
                                        id:id
                                    }),
                                    error: function(){
                                        alert("网络出现故障，请稍后");
                                        return;
                                    },
                                    success:function(data){
    //                                    ShowWall(user);
                                        var tem = Template.get("template/wall/photos.html");
                                        var r = tem({
                                            'user':user,
                                            'zone_pic':data
                                        });
                                        $('#photos_wall').html(r);
                                        initAddPhotos();
                                    }
                                });
                            });
                        });
                        $(".wall-a").mouseout(function (e) {
                            var a = $(e.currentTarget).find("#wall_cancel").css("font-size","0px");
                        });
                    }
                    $('#AddVideoToZone').unbind("click").click(function(e) {
                        Storage.filePickerDialog.open($('#AddVideoRoom'), function (files) {
                            if (files.length == 0){
                                $('#AddVideoRoom').html('');
                                return;
                            }
                            $('#AddVideoRoom').html('');
                            $('#VideoId').val(files[0].Id);
                            $('#VideoName').text(files[0].Name);
                            var jnext = JcropWarp();
                            jnext.title = '修改视频图标';
                            jnext.useAge = 'zoneItem';
                            jnext.ratio = 1;
                            jnext.uploadBtn = 'zoneItem-btn';
//                            jnext.needCrop = false;
                            zoneItemPortrait = files[0].Path;
                            jnext.init(files[0].Path, $('#zoneitem_portrait'), function(p, l, t, r, b){
                                zoneItemPortrait = p;
                                left = l;
                                right = r;
                                top = t;
                                bottom = b;
                            });
                            jnext.startSelect();
                            $('#zoneItem-btn').css('margin-left', '30px');
                        });
                    });
                    $('#VideoDescriptionInput').blur(function(e) {
                        $('#VideoDescription').text($('#VideoDescriptionInput').val());
                    });
                    $('#category_1').change(function(){
                        $('#category_2').html('');
                        var category_1 = $('#category_1').val();
                        if(category_1 != '')
                            for (var item in data.category) {
                                if (data.category[item].ParentId == category_1)
                                    $('#category_2').append(
                                        '<option value="' + data.category[item].Id + '">' + data.category[item].Name + '</option>'
                                    );
                            }
                    });
                    $('#addtag_1').unbind("click").click(function(e) {
                        if($('#tag_normal').val()!=''){
                            $('#tag_room').html($('#tag_room').html()+
                                '<span class="label label-primary" style="margin:5px;display:inline-block"><div style="display:inline-block">'+
                                $('#tag_normal')[0][$('#tag_normal').val()].innerHTML+
                                '</div><span style="cursor:pointer;margin-left:5px"' +
                                'onclick="$(this).parent().remove();"'+
                                '>&times;</span></span>'
                            )
                        }
                    });
                    $('#addtag_2').unbind("click").click(function(e) {
                        if($('#tag_personal').val()!=''){
                            $('#tag_room').html($('#tag_room').html()+
                                '<span class="label label-primary" style="margin:5px;display:inline-block"><div style="display:inline-block">'+
                                $('#tag_personal').val()+
                                '</div><span style="cursor:pointer;margin-left:5px"' +
                                'onclick="$(this).parent().remove();"'+
                                '>&times;</span></span>'
                            )
                        };
                    });
                    $('#SubmitVideo').unbind("click").click(function(e) {
                        if(!$('#VideoId').val()){
                            alert('请加入视频文件');
                            return;
                        };
                        if(!$('#VideoDescription').text()){
                            alert('视频描述不能为空');
                            return;
                        };
                        if(!$('#category_1').val() || !$('#category_2').val()){
                            alert('视频分类不能为空');
                            return;
                        };
                        if($('#itemprice').val()<0){
                            alert('竞价不能为负值');
                            return;
                        }
                        if($('#itemprice').val())
                            var price = $('#itemprice').val();
                        else
                            var price = 0;
                        var tags=[];
                        for(var tag in $('#tag_room').children().children('div')){
                            if(!$('#tag_room').children().children('div')[tag].innerText)break;
                            tags += $('#tag_room').children().children('div')[tag].innerText + ' ';
                        };
                        if(tags.length==0){
                            alert('视频标签不能为空');
                            return;
                        };
                        if(!zoneItemPortrait){
                            alert('请设置视频图标');
                            return;
                        }
                        var TagsArray = tags.split(" ");
                        var RP = parseFloat($('#BasePrice').val())+
                            parseFloat($('#SchemePrice').val())+
                            parseFloat($('#ShotPrice').val())+
                            parseFloat($('#MusicPrice').val())+
                            parseFloat($('#AEPrice').val())+
                            parseFloat($('#ActorPrice').val());
                        var referprice = RP?RP:0;
                        $.ajax({
                            type: "POST",
                            url: "/share/addVideoToZone",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                FileId:$('#VideoId').val(),
                                DomainId:user.DomainId,
                                Intro:$('#VideoDescription').text(),
                                Category_1:$('#category_1').val(),
                                Category_2:$('#category_2').val(),
                                Tags:tags,
                                TagsArray:TagsArray,
                                Price:price,
                                Portrait: zoneItemPortrait,
                                ReferPrice: referprice,
                                bp:$('#BasePrice').val()?$('#BasePrice').val():0,
                                scp:$('#SchemePrice').val()?$('#SchemePrice').val():0,
                                shp:$('#ShotPrice').val()?$('#ShotPrice').val():0,
                                acp:$('#ActorPrice').val()?$('#ActorPrice').val():0,
                                mp:$('#MusicPrice').val()?$('#MusicPrice').val():0,
                                aep:$('#AEPrice').val()?$('#AEPrice').val():0,
                                left: left,
                                right: right,
                                top: top,
                                bottom: bottom
                            }),
                            error: function(){
                                alert("添加失败，请检查网络。");
                                ShowWall(user);
                                return;
                            },
                            success:function(data){
                                if(data.result)
                                    ShowWall(user)
                                else{
                                    alert(data.info);
                                    ShowWall(user)
                                }
                            }
                        });
                    });
                    $('.btn-del').unbind("click").click(function(e) {
                        $.ajax({
                            type: "POST",
                            url: "/share/deleteVideoFromZone",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                Id:$(this).siblings('input').val()
                            }),
                            error: function(){
                                alert("添加失败，请检查网络。");
                                ShowWall(user);
                                return;
                            },
                            success:function(data){
                                ShowWall(user)
                            }
                        });
                    });
                    $('.ApplyClassical').unbind("click").click(function(e) {
                        $.ajax({
                            type: "POST",
                            url: "/share/applyClassical",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                Id:$(this).val()
                            }),
                            error: function(){
                                alert("添加失败，请检查网络。");
                                ShowWall(user);
                                return;
                            },
                            success:function(data){
                                ShowWall(user)
                            }
                        });
                    });
                    $("#IntroInput").keydown(function(event){
                        var len = $(this).val().length;
                        if(len > 127)
                            $(this).val($(this).val().substring(0,128));
                        else{
                            var num = 127 - len;
                            if(event.which==8)
                                if(len==1||len==0)num=128;
                                else
                                    num = num+2;
                            $("#IntroInfo").text('还可以输入' + num + '个字');
                        }
                    });
                    $('#IntroBtn').unbind('click').click(function(){
                        var text = $('#IntroInput').val();
                        $.ajax({
                            type: "POST",
                            url: "/share/saveIntroInZone",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                text:text
                            }),
                            error: function(){
                                alert("添加失败，请检查网络。");
                                ShowWall(user);
                                return;
                            },
                            success:function(data){
                                $('#IntroInfo').text('简介保存成功！').delay(2000).fadeOut('slow',function(){
//                                    ShowWall(user);
                                });
                            }
                        });
                    });
//                    $("#upload_video_image").uploadify({
//                        'buttonText': '修改视频图标',
//                        'hideButton': true,
//                        'wmode': 'transparent',
//                        'swf': "/script/uploadify/uploadify.swf",
//                        'height': 34,
//                        'uploader': '/cloud/uploadFile/easy?useAge=zoneItemPortrait',
//                        'onUploadSuccess': function (file, data, response) {
//                            var obj = JSON.parse(data);
//                            if (obj.errorMsg == undefined) {
//                                curPortrait = obj.fileName;
//                                var bi = 'url(/static' + obj.filePath + ')';
//                                $('#zoneitem_portrait').css('background-image', bi);
//                            } else {
//                                alertState("上传文件失败，错误信息：" + obj.errorMsg, "failed");
//                                alert("上传文件失败，错误信息：" + obj.errorMsg);
//                            }
//                        },
//                        onUploadError: function (file, errorCode, errorMsg) {
//                            alertState("上传文件失败，错误信息：" + errorMsg, "failed");
//                        }
//                    });
                }
            });
        }
        function tovip(data){
            var tem = Template.get('template/updata/tovip_next.html');
            var test = tem({user:data});
            $('#updata-content').html($.trim(test));
            $("#updata-back").unbind('clicked').click(function(){
                window.history.go(0);
            });
            $('#tovip-next-submit').unbind('clicked').click(function(){
                if($('#domain_new_name_input').val()==""){
                    alert("请输入企业真实名称");
                    return;
                }
                if($('#CellPhone').val()==""){
                    alert("请输入企业联系人姓名");
                    return;
                }
                $.ajax({
                    type: "POST",
                    url: "/share/createDomain",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        DomainName : $("#domain_new_name_input").val(),
                        CellPhone : $('#CellPhone').val()
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alert("创建域失败.问题描述: " + data.errorMsg);
                            return;
                        }
                         $().GoToUrl('/UpdataPage');
                        window.location.reload();
                    },
                    error: function () {
                        alert("创建域失败，网络异常");
                    }
                });
            });
        }
        function extend(data){
            var UserId = data.Id;
            var tem = Template.get('template/updata/extend.html');
            var test = tem({user:data});
            $('#updata-content').html($.trim(test));

            function calPrice(){
                var extendSize = parseInt(data.Domain.ExtendStorageSize / 1024 / 1024 / 1024);
                var buySize = parseFloat($('#input_extendStorage').val());
                var esTime = new Date(data.Domain.ESExpireTime);
                var buyTime = $('#input_extendTime').val();
                var curTime = new Date();
                if (!buySize)
                    buySize = 0;
                if (!buyTime)
                    buyTime = 0;
                esTime = parseInt(esTime.getTime() / 1000 / 60 / 60 / 24);
                buyTime = buyTime * 31;
                curTime = parseInt(curTime.getTime() / 1000 / 60 / 60 / 24);
                var timeLeft = (esTime > curTime) ? esTime - curTime : 0;
                var price = 0.0161;
                var result = timeLeft * buySize * price + buyTime * (buySize + extendSize) * price;
                if (result > 0)
                    $('#ExtendSubmit').removeClass('disabled');
                else
                    $('#ExtendSubmit').addClass('disabled');
                return result.toFixed(2);
            }
            $('#input_extendStorage').blur(function(){
                $('#price').text(calPrice());
            });
            $('#input_extendTime').blur(function(){
                $('#price').text(calPrice());
            });
            var e_useCount = $("#UseCount");
            $("#UseCountOn").unbind('clicked').click(function(){
                if ($("#UseCountOn")[0].checked == true){
                    e_useCount.fadeToggle().focus();
                    e_useCount.css('display', 'inline-block');
                }
                else
                    e_useCount.css('display', 'none');
                check_useCount();
            });
            e_useCount.blur(function(){
                check_useCount();
            });
            function check_useCount(){
                if ($("#UseCountOn")[0].checked == false) {
                    e_useCount.val('');
                }
                else if(data.Domain.Count < e_useCount.val()){
                    e_useCount.focus();
                    if (data.Domain.Count > calPrice())
                        e_useCount.val(calPrice());
                    else
                        e_useCount.val(data.Domain.Count);
                }
                else if (calPrice() - e_useCount.val() < 0){
                    e_useCount.val(calPrice());
                }
                $("#price").text(parseFloat(calPrice() - e_useCount.val()).toFixed(2));
            }
            $("#ExtendSubmit").unbind('clicked').click(function(){
                check_useCount();
                var useAccount = e_useCount.val();
                if (useAccount == '')
                    useAccount = 0;
                if (calPrice() <= 0)
                    return;
                var extendStorage = $('#input_extendStorage').val();
                if (!extendStorage)
                    extendStorage = 0;
                var extendTime = $('#input_extendTime').val();
                if (!extendTime)
                    extendTime = 0;
                $.ajax({
                    type: "POST",
                    url: '/platform/CreateOrder',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        Price: calPrice(),
                        UseCount: parseFloat(useAccount),
                        ExtendStorage: parseInt(extendStorage),
                        ExtendTime: parseInt(extendTime),
                        OrderType: 'ExtendStorage'
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("支付请求失败.问题描述: " + data.errorMsg, "info");
                            return;
                        }
                        $().alipayProcess(
                            '购买扩展云空间',
                            data.SerialNumber,
                            data.Id,
                            data.Amount,
                            useAccount,
                            '商影联盟官方账号',
                            function(bSuccess) {
                                if (bSuccess)
                                    window.history.go(0);
                            }
                        );
                    },
                    error: function () {
                        alertState("支付请求失败，网络异常", "failed");
                    }
                });
            });
        }
    }

    function logCenter(){
        var lc = {};
        lc.operFilter = {success: 1, info: 2, failed: 3};
        lc.logType = {oper: 1, req: 2, contract: 3};
        lc.curOperFilter = lc.operFilter["success"];
        lc.init = function(){
            var tem = Template.get('template/updata/logCenter.html');
            $('#updata-content').html($.trim(tem()));
            $('#operFilter_success').unbind('click').click(function(){
                 lc.changeFilter(lc.logType["oper"], lc.operFilter["success"]);
            });
            $('#operFilter_info').unbind('click').click(function(){
                 lc.changeFilter(lc.logType["oper"], lc.operFilter["info"]);
            });
            $('#operFilter_failed').unbind('click').click(function(){
                 lc.changeFilter(lc.logType["oper"], lc.operFilter["failed"]);
            });
            $('#oper_clear').unbind('click').click(function(){
                 lc.clear(lc.logType["oper"]);
            });
            lc.load(lc.logType["oper"]);
        };
        lc.changeFilter = function(logType, filter){
            if (logType == lc.logType["oper"]){
                lc.curOperFilter = filter;
            }
            else if (logType == lc.logType["req"]){

            }
            else if (logType == lc.logType["contract"]){

            }
            lc.load(logType);
        };
        lc.clear = function(logType){
            if (logType == lc.logType["oper"]){
                $().clearOperLog();
            }
            else if (logType == lc.logType["req"]){

            }
            else if (logType == lc.logType["contract"]){

            }
            lc.load(logType);
        };
        lc.load = function(logType){
            if (logType == lc.logType["oper"]){
                var tem = Template.get('template/updata/operLog.html');
                var logs = $().getOperLog();
                $(logs).each(function(index, value){
                    value["bShow"] = true;
                    if (lc.curOperFilter == lc.operFilter["info"] && value["level"] == "success")
                        value["bShow"] = false;
                    else if (lc.curOperFilter == lc.operFilter["failed"] &&
                        (value["level"] == "success" || value["level"] == "info"))
                        value["bShow"] = false;
                });
                $('#operLogArea').html($.trim(tem({operLog: logs})));
            }
            else if (logType == lc.logType["req"]){

            }
            else if (logType == lc.logType["contract"]) {
            }
        };
        return lc;
    }
    var logCenterInstance = logCenter();

    var updata_interface = {};
    updata_interface.pageRouter = {
        '/UpdataPage': updataInit
    };
    return updata_interface;
});