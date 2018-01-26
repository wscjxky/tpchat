define(['jquery', 'template', 'storage', 'md5'], function ($, Template, Storage) {
	var cache_ = {};
	//解析域数据
	function parseDomainInfo(data) {
		cache_ = {
			id: data.Id,
			name: data.DomainName,
			ownerUserId: data.OwnerUserId,
			roles: {},
			users: {}
		};
		//域角色信息
		$(data.Roles).each(function (i, data_roles) {
			cache_.roles[data_roles.Id] = {
				name: data_roles.Name,
				domainAdmin: data_roles.DomainAdmin,
				domainCreate: data_roles.DomainCreate,
				domainWrite: data_roles.DomainWrite,
				domainShare: data_roles.DomainShare,
				domainDelete: data_roles.DomainDelete,
				domainDownload: data_roles.DomainDownload
			};
		});
		//域用户信息
		$(data.Users).each(function (i, data_userInfo) {
			var userInfo;
			userInfo = {
				id: data_userInfo.Id,
				name: data_userInfo.NickName,
				domainName: data_userInfo.DomainName,
				domainWrite: false,
				domainCreate: false,
				domainDelete: false,
				domainDownload: false,
				domainShare: false,
				domainAdmin: false,
				roles: {}
			};
			//用户角色信息
			$(data_userInfo.Roles).each(function (j, data_userRole) {
				var roleInfo = cache_.roles[data_userRole.Id];
				userInfo.roles[data_userRole.Id] = {
					id: data_userRole.Id,
					name: roleInfo.name,
					domainAdmin: roleInfo.domainAdmin,
					domainWrite: roleInfo.domainWrite,
					domainCreate: roleInfo.domainCreate,
					domainShare: roleInfo.domainShare,
					domainDelete: roleInfo.domainDelete,
					domainDownload: roleInfo.domainDownload
				};
				userInfo.domainWrite = userInfo.domainWrite | roleInfo.domainWrite;
				userInfo.domainCreate = userInfo.domainCreate | roleInfo.domainCreate;
				userInfo.domainDelete = userInfo.domainDelete | roleInfo.domainDelete;
				userInfo.domainShare = userInfo.domainShare | roleInfo.domainShare;
				userInfo.domainDownload = userInfo.domainDownload |  roleInfo.domainDownload;
				userInfo.domainAdmin = userInfo.domainAdmin | roleInfo.domainAdmin;
			});
			cache_.users[data_userInfo.Id] = userInfo;
		});
	};

	
	function fetchDomainInfo() {
		$.ajax({
			type: "POST",
			url: "/share/getDomainInfo",
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({}),
			success: function (data) {
				if (!isResponseDataAvailable(data)) {
					alertState("获取域信息失败.问题描述: " + data.errorMsg, "info");
					loadDomainUI(false);
					return;
				}
				parseDomainInfo(data);												//获取信息
				loadDomainUI(true);													//此处加载页面
			},
			error: function () {
				alertState("获取域信息失败，网络异常", "failed");
			}
		});
	};
	//加载域角色界面
	function loadDomainUI(bHasDomain) {
		var tem = Template.get('template/domain/roleSetting.html');
		var test = tem({hasDomain: bHasDomain, domainName: cache_.name});
        $("#functionalArea").html($.trim(test));
        //$("#functionalArea").animate({left:'-100%'},300);
		//$("#functionalArea").html($.trim(test)).animate({left:'100%'},0).animate({left:'0px'},200);

		//添加用户或角色按钮事件绑定
		$("#addSomething").unbind("click").click(function () {
			addSomething();
		});

        roleSettingListInit();
	};
			
	function addSomething() {
		initAddRole();
	};
	
	function initAddRole() {
			var tem = Template.get('template/domain/domain_role_add_dialog.html');
			var test = tem(cache_);
			$('#domain_role_add_dialog').html($.trim(test));
			$("#domain_role_add_commit").unbind("click").click(function () {
				addRole_add();
			});
			$("#domain_role_add_dialog").modal();

			function addRole_add() {
				$("#domain_role_add_dialog").modal('hide');
				var domainWrite = $("#domain_role_add_right_write").prop("checked");
				var domainCreate = $("#domain_role_add_right_create").prop("checked");
				var domainDelete = $("#domain_role_add_right_delete").prop("checked");
				var domainDownload = $("#domain_role_add_right_download").prop("checked");
				var domainShare = $("#domain_role_add_right_share").prop("checked");

				var domainModifyInfo = {
					Id: cache_.id,
					Name: cache_.name,
					Roles: [
						{
							Id: -1,
							Name: $("#domain_role_add_roleName_input").val(),
							DomainWrite: domainWrite,
							DomainCreate: domainCreate,
							DomainDelete: domainDelete,
							DomainShare: domainShare,
							DomainDownload:domainDownload,
							Operate: "add"
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
							alertState("添加域角色失败.问题描述: " + data.errorMsg, "failed");
							return;
						}
						parseDomainInfo(data);
						roleSettingListInit();
						alertState("添加域角色完成", "success");
					},
					error: function () {
						alertState("添加域角色失败，网络异常", "failed");
					}
				});
			}
		}
	
	function roleSettingListInit(){
		var tem = Template.get('template/domain/domain_role.html');
		var test = tem(cache_);
		$("#domain_role_list").html($.trim(test));
		
		$(".domain_role_delete_Btn").unbind("click").click(function (e) {
			deleteRole(e);
		});
		$(".domain_role_modify_Btn").unbind("click").click(function (e) {
			initModifyRole(e);
		});
		//删除角色
		function deleteRole(e) {
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
					parseDomainInfo(data);
					roleSettingListInit();
					alertState("删除域角色完成", "success");
				},
				error: function () {
					alertState("删除域角色失败，网络异常", "failed");
				}
			});
		}
		//修改域用户流程
		function initModifyRole(e) {
			var tem = Template.get('template/domain/domain_role_modify_dialog.html');
			var test = tem(cache_);
			$('#domain_role_modify_dialog').html($.trim(test));
			$("#domain_role_modify_commit").unbind("click").click(function () {
				modifyRole_modify();
			});

			var roleId = parseInt($(e.currentTarget).parent().find(".role_id").text());
			//设置角色权限显示
			if (cache_.roles[roleId].domainWrite)
				$("#domain_role_modify_right_write").attr("checked", "checked");
			if (cache_.roles[roleId].domainCreate)
				$("#domain_role_modify_right_create").attr("checked", "checked");
			if (cache_.roles[roleId].domainDelete)
				$("#domain_role_modify_right_delete").attr("checked", "checked");
			if (cache_.roles[roleId].domainDownload)
				$("#domain_role_modify_right_download").attr("checked", "checked");
			if (cache_.roles[roleId].domainShare)
				$("#domain_role_modify_right_share").attr("checked", "checked");

			$("#domain_role_modify_domainName").val(cache_.roles[roleId].name);
			$("#domain_role_modify_dialog").modal();

			function modifyRole_modify() {
				$("#domain_role_modify_dialog").modal('hide');

				var domainModifyInfo = {
					Id: cache_.id,
					Name: cache_.name,
					Roles: [
						{
							Id: roleId,
							Operate: "modify",
							Name: $("#domain_role_modify_domainName").val(),
							DomainWrite: $("#domain_role_modify_right_write").is(':checked'),
							DomainCreate: $("#domain_role_modify_right_create").is(':checked'),
							DomainDelete: $("#domain_role_modify_right_delete").is(':checked'),
							DomainDownload: $("#domain_role_modify_right_download").is(':checked'),
							DomainShare: $("#domain_role_modify_right_share").is(':checked')
							//,DomainAdmin: $("#domain_role_modify_right_admin").is(':checked')
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
							alertState("修改域角色信息失败.问题描述: " + data.errorMsg, "failed");
							return;
						}
						parseDomainInfo(data);
						roleSettingListInit();
						initDomainUserList();
						alertState("修改域角色信息完成", "success");
					},
					error: function () {
						alertState("修改域角色信息失败，网络异常", "failed");
					}
				});
			}
		}
	};
	//初始化新域流程
	function initNewDomain() {
		//创建域事件
		$("#domain_create_btn").unbind("click").click(function () {
			$().GoToUrl('/UpdataPage');
		});
	};
	function roleSettingInit() {
		fetchDomainInfo();
	};
		
	var roleSetting_interface = {};
    roleSetting_interface.pageRouter = {
        '/roleSettingPage': roleSettingInit
    };
    return roleSetting_interface;
});