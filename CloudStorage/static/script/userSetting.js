define(['jquery', 'template'], function ($, Template) {
    var cache_ = {};
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
            users: {}
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
                    Users: [
                        userInfo
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
                            alertState("添加域用户失败.问题描述: " + data.errorMsg, "failed");
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
                var test = tem({domainName: cache_.name});
                if (bAnimate)
                    $('#updata-content').html($.trim(test)).animate({left:'-100%'},0).animate({left:0},300);
                else
                    $('#updata-content').html($.trim(test));
                $("#roleSetting").unbind("click").click(function () {
                    role_instance.show(true);
                });
                //添加用户或角色按钮事件绑定
                $("#addSomething").unbind("click").click(function () {
                    family.initAddUser();
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
                if (bAnimate)
                    $("#updata-content").html($.trim(test));
                else
                    $("#updata-content").html($.trim(test));
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

    function userSettingInit() {
        family_instance.show(false);
    }

	var userSetting_interface = {};
    userSetting_interface.pageRouter = {
        '/userSettingPage': userSettingInit
    };
    return userSetting_interface;
});