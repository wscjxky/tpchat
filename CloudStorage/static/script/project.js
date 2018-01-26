/**
 * Created by jixia_000 on 2014/10/26.
 */
define(['jquery', 'template', 'storage', 'contract'], function ($, Template, Storage, Contract) {
    var cache_ = {};
    Template.helper("projectStatusTranslator", function (Status) {
        var _status = {0: "正在进行", 1: "已完成"};
        return _status[Status];
    });
    Template.helper("renderProjectAttachment", function (code,name) {
        return '<a href="/platform/downloadAttachment/'+code+'?DBToken='+$().retrieveSession().DBToken+'">'+name+'</a>';
    });
    Template.helper("ParseTime", function (date) {
        var d = new Date(date);
        return d.Format("yyyy-MM-dd hh:mm");
    });
    function autodatepaser(el) {
        el.val('');
        $.each(el.find('input[type="text"]'), function (index, value) {
            value = $(value);
            value.unbind('keyup').keyup(function () {
                var val = value.val();
                var el = value.parent();
                try {
                    var parseddate = new Date(val);
                    el.find('div').html(parseddate.toLocaleString());
                    el.find('div').addClass('alert-success').removeClass('alert-warning');
                    el.val(parseddate);
                } catch (e) {
                    el.find('div').html("请输入合法的日期");
                    el.find('div').removeClass('alert-success').addClass('alert-warning');
                    el.val(null);
                }
            });
            value.trigger('keyup');
        });

    }

    function searchUser(callback) {
        var tem = Template.get('template/contract/searchUser.html');
        if ($('#searchUser').length == 0) {
            $('#functionalArea').append('<div id="searchUser" class="modal fade bs-example-modal-lg"></div>');
        }
        $('#searchUser').html(tem());
        $('#searchUser').modal();
        function search() {
            var username = $('#user_search_input').val();
            $.ajax({
                type: "POST",
                url: "/share/searchUser",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({KeyWord: username}),
                success: function (data) {
                    var tem = Template.get('template/domain/searchUserList.html');
                    var test = tem(data);
                    $("#user_search_result").html($.trim(test));
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
        }

        $('#user_search_input').unbind('keyup').keyup(function (e) {
            if (e.keyCode == 13) {
                search();
            }
        });
        $('#user_search__btn').unbind('click').click(search);

        $('#user_search_commit').unbind('click').click(function (e) {
            var a = +$('.searchUser_check').find('input:checked').parent().parent().find('.searchUser_id').html();
            var username = $('.searchUser_check').find('input:checked').parent().parent().find('.searchUser_email').html();
            if (username == "") {
                username = $('.searchUser_check').find('input:checked').parent().parent().find('.searchUser_domainName').html();
            }
            if (a != 0) {
                callback(a, username);
            }
            $('#searchUser').modal('hide');
        });
    }

    function showDetail(id) {
        $.ajax({
            type: "POST",
            url: "/platform/project",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({Id: id}),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("提交需求失败.问题描述: " + data.errorMsg, "info");
                    return;
                }
                data = data[0];
                cache_.Id = id;
                var lastSegmentStatus = 2;
                $.each(data.ProjectSegment, function (index, value) {
                    {
                        if ((value.Status == 0 || value.Status == 3)&&value.PrincipalUserId == $().retrieveSession().UserId) {
                                if (lastSegmentStatus != 2) {
                                    return false;
                                }
                                value.ReadyApply = true;
                                cache_.applyId = value.Id;
                                return false;
                            } else if (value.Status == 1 && data.PrincipalUserId == $().retrieveSession().UserId) {
                                if (value.ContractSegmentId == null||value.ContractSegmentId == 0) {
                                    value.ReadyConfirm = true;
                                }
                                cache_.confirmId = value.Id;
                                value.ReadyReject = true;

                            }
                        }
                    try{
                        value.ApplyRemark = JSON.parse(value.ApplyRemark);
                    }catch (e){
                    }
                    lastSegmentStatus = value.Status;
                });

                if ($('#editProjectDialog').length == 0) {
                    $('#functionalArea').append('<div class="modal fade bs-example-modal-sm" id="editProjectDialog"></div>')
                }
                var tem = Template.get('template/project/project_detail.html');
                $('#editProjectDialog').html(tem(data));


                $('#editProjectDialog').find('.apply_project_segment').unbind('click').click(function (e) {
                    var tem = Template.get('template/contract/contract_segment_apply.html');
                    if ($('#applyProjectDialog').length == 0) {
                        $('#functionalArea').append('<div class="modal fade bs-example-modal-sm" id="applyProjectDialog"></div>')
                    }
                    var IsAttachmentAllowed = data.ContractId != null;
                    var attachments = IsAttachmentAllowed ? [] : undefined;
                    $('#applyProjectDialog').html(tem({addAttachment: IsAttachmentAllowed ? true : undefined}));
                    if (IsAttachmentAllowed) {
                        $('#applyProjectDialog').find('#add_contract_attachment').unbind('click').click(function (e) {
                            Storage.filePickerDialog.open($('#add_contract_attachment').parent(), function (file) {
                                $('#applyProjectDialog').find('#fileUploadedList').append('<div>' + file.Name + '</div>');
                                attachments.push(file);
                            });
                        });
                        $('#applyProjectDialog').find('#upload_contract_attachment').uploadify({
                            'buttonText': '上传附件',
                            'hideButton': true,
                            'wmode': 'transparent',
                            'swf': "script/uploadify/uploadify.swf",
                            'height': 34,
                            'uploader': "/cloud/uploadFile?DBToken=" + $().retrieveSession().DBToken + "&Id=0",
                            'onUploadSuccess': function (file, data, response) {
                                var obj = JSON.parse(data);
                                if (obj.errorMsg == undefined) {
                                    $('#applyProjectDialog').find('#fileUploadedList').append('<div>' + obj[0].Name + '[未提交]</div>');
                                    attachments.push(obj[0]);
                                } else {
                                    alert(obj.errorMsg);
                                }
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
                    $('#applyProjectDialog').find('#contractsegment_apply_commit').unbind('click').click(function (e) {
                        var remark = $('#contractsegment_apply_remark').val();
                        $.ajax({
                            type: "POST",
                            url: "/platform/applyProjectSegment",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                Id: id,
                                ApplyRemark: remark,
                                Attachments:attachments,
                                SegmentId: cache_.applyId
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("获取需求信息失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                $('#applyProjectDialog').modal('hide');
                                showDetail(id);
                            },
                            error: function () {
                                alertState("获取需求信息失败，网络异常", "failed");
                            }
                        });
                    })
                    $('#applyProjectDialog').modal();
                });
                $('#editProjectDialog').find('.confirm_project_segment').unbind('click').click(function (e) {
                    var IsReject = false;
                    if (e.currentTarget.innerHTML == '拒绝') {
                        IsReject = true;
                    }
                    var tem = Template.get('template/contract/contract_segment_apply.html');
                    if ($('#applyProjectDialog').length == 0) {
                        $('#functionalArea').append('<div class="modal fade bs-example-modal-sm" id="applyProjectDialog"></div>')
                    }
                    $('#applyProjectDialog').html(tem({}));
                    $('#applyProjectDialog').find('#contractsegment_apply_commit').unbind('click').click(function (e) {
                        var remark = $('#contractsegment_apply_remark').val();
                        $.ajax({
                            type: "POST",
                            url: "/platform/confirmProjectSegment",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({Id: id, ConfirmRemark: remark, SegmentId: cache_.confirmId, IsReject: IsReject}),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("获取需求信息失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                $('#applyProjectDialog').modal('hide');
                                showDetail(id);
                            },
                            error: function () {
                                alertState("获取需求信息失败，网络异常", "failed");
                            }
                        });
                    })
                    $('#applyProjectDialog').modal();
                });
                $('#add_contract_attachment').unbind('click').click(function () {
                    Storage.filePickerDialog.open($('#add_contract_attachment').parent(), function (file) {
                        $('#fileUploadedList').append('<div>' + file.Name + '</div>');
                        var param = {ProjectId: data.ContractId};
                        param = $.extend(file, param);
                        $.ajax({
                            type: "POST",
                            url: "/platform/addContractAttachment",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(param),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("获取需求信息失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                            },
                            error: function () {
                                alertState("获取需求信息失败，网络异常", "failed");
                            }
                        });
                    });
                });
                $('#project_detail_close').unbind('click').click(function (e) {
                    $('#editProjectDialog').modal('hide');
                });
                $('#editProjectDialog').modal();
            },
            error: function () {
                alertState("提交需求失败，网络异常", "failed");
            }
        });
    }

    function projectPage() {
        var tem = Template.get('template/project/projects.html');
        $('#functionalArea').html($.trim(tem()));
        $('#addSomething').unbind('click').click(function (e) {
            if ($('#projectCreateDialog').length == 0) {
                $('#functionalArea').append('<div id="projectCreateDialog" class="modal fade bs-example-modal-lg"></div>');
            }
            var t = Template.get('template/project/project_create.html');

            $('#projectCreateDialog').html(t({Title: '', Detail: ''}));
            $("#project_add_principal_user_select_btn").unbind('click').click(function (e) {
                searchUser(function (userid, username) {
                    $('#projectCreateDialog').css({'overflow-x': 'hidden', 'overflow-y': 'auto'});
                    $('#project_add_principal_user').html(username);
                    $('#project_add_principal_user_id').val(userid);
                });
            });
            var project_segment_template = Template.get("template/project/project_segment.html");
            var project_segments = ["拍摄审核", "剪辑审核", "包装审核", "剪辑审核", "调色审核", "包装审核", "配音审核", "成片审核"];
            for (var i = 0; i < project_segments.length; i++) {
                var obj = {};
                obj.Remark = project_segments[i];
                obj.Value = obj.Remark;
                obj.Checked = i == (project_segments.length - 1);//成片审核必选
                project_segments[i] = obj;
                obj.Deadline = "";
            }


            var project_segments_ul = $('#project_add_segment');
            $.each(project_segments, function (index, value) {
                var r = project_segment_template(value);
                project_segments_ul.append(r);
            });
            $('#projectCreateDialog').find('.project_segment').find('input[type="checkbox"]').unbind('change').change(function (e) {
                var control = $(e.currentTarget).parent().find('.datecontrol ,.contract_segment_principal_user_selector');
                if ($(e.currentTarget).prop('checked')) {
                    control.show();
                } else {
                    control.hide();
                }

            });
            $('#projectCreateDialog').find('.project_segment').find('input[type="checkbox"]').trigger('change');
            $(".contract_segment_principal_user_select_btn").unbind('click').click(function (e) {
                var cur = $(e.currentTarget).parent();
                searchUser(function (userid, username) {
                    $('#projectCreateDialog').css({'overflow-x': 'hidden', 'overflow-y': 'auto'});
                    cur.find('.ContractSegmentPrincipalUser').html(username);
                    cur.find('.ContractSegmentPrincipalUserId').val(userid);
                });
            });
            autodatepaser($('#projectCreateDialog').find('.project_segment'));
            $("#project_add_commit").unbind('click').click(function (e) {
                var PrincipalUserId = $('#project_add_principal_user_id').val();
                if (PrincipalUserId == null || PrincipalUserId == undefined || PrincipalUserId == "") {
                    alert("负责人不能为空");
                    return false;
                }
                var segments = [];
                var projectSegment = $('#projectCreateDialog').find('.project_segment').find('input[type="checkbox"]:checked');
                var lastDeadline = null;
                $.each(projectSegment, function (index, value) {
                    var el = $(value);
                    var obj = {};
                    obj.Remark = el.val();
                    obj.Deadline = el.parent().find('.datecontrol').val();
                    obj.PrincipalUserId = el.parent().find('.ContractSegmentPrincipalUserId').val();
                    if (obj.PrincipalUserId == undefined || obj.PrincipalUserId == null) {
                        alert('请选择环节负责人');
                        throw new Error('请选择环节负责人');
                    }
                    if (obj.Deadline == null) {
                        alert('请输入合法的日期');
                        throw new Error('没有合法日期！')
                    }
                    if (lastDeadline != null && lastDeadline > obj.Deadline) {
                        alert('后置流程必须比前置流程时间晚');
                        throw new Error('后置流程必须比前置流程时间晚');
                    }
                    var contractSegmentId = el.parent().find('input[name="ContractSegmentId"]');
                    if (contractSegmentId.length == 1) {
                        obj.ContractSegmentId = +contractSegmentId.val();
                    }
                    obj.Segment = 1;
                    lastDeadline = obj.Deadline;
                    segments.push(obj);
                });
                $.ajax({
                    type: "POST",
                    url: "/platform/createProject",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({Segments: segments, PrincipalUserId: PrincipalUserId, Title: $('#project_title').val(), Detail: $('#project_detail').val()}),
                    success: function (data) {
                        if (data.errorMsg == undefined) {
                            alertState("工程创建成功", "success");
                            $('#projectCreateDialog').modal('hide');
                            $('#editContractDialog,.fade .in').modal('hide');
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            return;
                        }
                        alertState("合同修改失败：" + data.errorMsg, "failed");
                    },
                    error: function () {
                        alertState("合同修改失败，网络异常", "failed");
                    }
                });
            });
            $('#projectCreateDialog').modal();
        });
        $.ajax({
            type: "POST",
            url: "/platform/project",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({}),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("获取项目信息失败.问题描述: " + data.errorMsg, "info");
                    return;
                }
                var tem = Template.get("template/project/project_list.html");
                var r = tem({'projects': data, 'IsService': $().retrieveSession().IsService});
                $('#projectPage').html(r);
                alertState("获取项目信息完成", "success");
                $("#projectPage").find(".project_title").unbind('click').click(function (e) {
                    showDetail($(e.currentTarget).parent().parent().find('.row_id').val());
                });

            },
            error: function () {
                alertState("获取项目信息失败，网络异常", "failed");
            }
        });
    }

    function createProject(contractId, parent) {
        if ($('#projectCreateDialog').length == 0) {
            parent.append('<div id="projectCreateDialog" class="modal fade bs-example-modal-lg"></div>');
        }
        var t = Template.get('template/project/project_create.html');
        $.ajax({
            type: "POST",
            url: "/platform/myContract",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({Id: contractId}),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("获取项目信息失败.问题描述: " + data.errorMsg, "info");
                    return;
                }
                $('#projectCreateDialog').html(t(data));
                $("#project_add_principal_user_select_btn").unbind('click').click(function (e) {
                    searchUser(function (userid, username) {
                        $('#projectCreateDialog').css({'overflow-x': 'hidden', 'overflow-y': 'auto'});
                        $('#project_add_principal_user').html(username);
                        $('#project_add_principal_user_id').val(userid);
                    });
                });
                var project_segment_template = Template.get("template/project/project_segment.html");
                var project_segments = ["拍摄审核", "剪辑审核", "包装审核", "剪辑审核", "调色审核", "包装审核", "配音审核", "成片审核"];
                for (var i = 0; i < project_segments.length; i++) {
                    var obj = {};
                    obj.Remark = project_segments[i];
                    obj.Value = obj.Remark;
                    obj.Checked = i == (project_segments.length - 1);//成片审核必选
                    project_segments[i] = obj;
                    obj.Deadline = "";
                }
                function findSegment(Remark) {
                    for (var i = 0; i < project_segments.length; i++) {
                        if (project_segments[i].Remark == Remark) {
                            return i;
                        }
                    }
                    return -1;
                }

                $.each(data.ContractSegment, function (index, value) {
                    if (value.Segment == 3) {
                        var i = findSegment(value.Remark);
                        if (i == -1)return true;
                        var obj = project_segments[i];
                        obj.ContractSegmentId = value.Id;
                        obj.Checked = true;
                        obj.Value = value.Remark;
                        obj.Remark = value.Remark + "(合同步骤，必选)";
                        obj.Deadline = value.Deadline;
                    }
                });

                var project_segments_ul = $('#project_add_segment');
                $.each(project_segments, function (index, value) {
                    var r = project_segment_template(value);
                    project_segments_ul.append(r);
                });
                $('#projectCreateDialog').find('.project_segment').find('input[type="checkbox"]').unbind('change').change(function (e) {
                    var control = $(e.currentTarget).parent().find('.datecontrol ,.contract_segment_principal_user_selector');
                    if ($(e.currentTarget).prop('checked')) {
                        control.show();
                    } else {
                        control.hide();
                    }

                });
                $('#projectCreateDialog').find('.project_segment').find('input[type="checkbox"]').trigger('change');
                $(".contract_segment_principal_user_select_btn").unbind('click').click(function (e) {
                    var cur = $(e.currentTarget).parent();
                    searchUser(function (userid, username) {
                        $('#projectCreateDialog').css({'overflow-x': 'hidden', 'overflow-y': 'auto'});
                        cur.find('.ContractSegmentPrincipalUser').html(username);
                        cur.find('.ContractSegmentPrincipalUserId').val(userid);
                    });
                });
                autodatepaser($('#projectCreateDialog').find('.project_segment'));
                $("#project_add_commit").unbind('click').click(function (e) {
                    var PrincipalUserId = $('#project_add_principal_user_id').val();
                    if (PrincipalUserId == null || PrincipalUserId == undefined || PrincipalUserId == "") {
                        alert("负责人不能为空");
                        return false;
                    }
                    var segments = [];
                    var projectSegment = $('#projectCreateDialog').find('.project_segment').find('input[type="checkbox"]:checked');
                    var lastDeadline = null;
                    $.each(projectSegment, function (index, value) {
                        var el = $(value);
                        var obj = {};
                        obj.Remark = el.val();
                        obj.Deadline = el.parent().find('.datecontrol').val();
                        obj.PrincipalUserId = el.parent().find('.ContractSegmentPrincipalUserId').val();
                        if (obj.PrincipalUserId == undefined || obj.PrincipalUserId == null) {
                            alert('请选择环节负责人');
                            throw new Error('请选择环节负责人');
                        }
                        if (obj.Deadline == null) {
                            alert('请输入合法的日期');
                            throw new Error('没有合法日期！')
                        }
                        if (lastDeadline != null && lastDeadline > obj.Deadline) {
                            alert('后置流程必须比前置流程时间晚');
                            throw new Error('后置流程必须比前置流程时间晚');
                        }
                        var contractSegmentId = el.parent().find('input[name="ContractSegmentId"]');
                        if (contractSegmentId.length == 1) {
                            obj.ContractSegmentId = +contractSegmentId.val();
                        }
                        obj.Segment = 1;
                        lastDeadline = obj.Deadline;
                        segments.push(obj);
                    });
                    $.ajax({
                        type: "POST",
                        url: "/platform/createProject",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({ContractId: contractId, Segments: segments, PrincipalUserId: PrincipalUserId, Title: $('#project_title').val(), Detail: $('#project_detail').val()}),
                        success: function (data) {
                            if (data.errorMsg == undefined) {
                                alertState("工程创建成功", "success");
                                $('#projectCreateDialog').modal('hide');
                                $('#editContractDialog,.fade .in').modal('hide');
                                $('body').removeClass('modal-open');
                                $('.modal-backdrop').remove();
                                return;
                            }
                            alertState("合同修改失败：" + data.errorMsg, "failed");
                        },
                        error: function () {
                            alertState("合同修改失败，网络异常", "failed");
                        }
                    });
                });
                $('#projectCreateDialog').modal();
            },
            error: function () {
                alertState("获取合同信息失败，网络异常", "failed");
            }
        });
    }

    var project_interface = {};
    project_interface.pageRouter = {
        '/projectPage': projectPage
    };
    project_interface.createProject = createProject;
    return project_interface;
});
