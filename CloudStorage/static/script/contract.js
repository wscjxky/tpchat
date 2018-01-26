define(['jquery', 'template', 'storage', 'project', 'highchart'], function ($, Template, Storage, Project) {
        var cache_ = {};
        var ContractClass = {
            ContractSegment: {establish: 3, payRent: 4, review: 5, payall: 6, retainage: 7, finish: 8},
//            ContractSegStatus: {init: 0, applied: 1, confirmed: 2, rejected: 3},
//            ContractAttachType: {all: -1, exchange: 0, clip: 1, cutVideo: 2, renderVideo: 3, soundVideo: 4, finalVideo: 5, end: 6},
            ContractOrderType: {payRent: 0, payRest: 1},
            curPage: 1,
            create: function(){
                var contract = {};
                contract.id = 0;
                contract.data = {};
                contract.applySeg = function(req){
                    var api = "/platform/applyContractReview";
//                      if (segment.Segment == ContractClass.ContractSegment.payRent ||
//                            segment.Segment == ContractClass.ContractSegment.complete)
//                            api = "/platform/payContract";
                        $.ajax({
                            type: "POST",
                            url: api,
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                reqId:req.Id,
                                conId:req.ContractId
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("申请确认失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                window.location.reload();
                            },
                            error: function () {
                                alert("申请确认失败，网络异常");
                            }
                        });
                };
                contract.confirmSeg = function(req){
                    api = "/platform/confirmContractReview";
                    $.ajax({
                        type: "POST",
                        url: api,
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            reqId:req.Id,
                            conId:req.ContractId,
                            IsReject: false
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("确认行为失败.问题描述: " + data.errorMsg, "info");
                                return;
                            }
                            window.location.reload();
                        },
                        error: function () {
                            alert("确认行为失败，网络异常");
                        }
                    });
                };
                contract.rejectSeg = function(req){
                    var api = "platform/confirmContractReview";
                    $.ajax({
                        type: "POST",
                        url: api,
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            reqId:req.Id,
                            conId:req.ContractId,
                            IsReject: true
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("驳回行为失败.问题描述: " + data.errorMsg, "info");
                                return;
                            }
                            window.location.reload();
                        },
                        error: function () {
                            alert("驳回行为失败，网络异常");
                        }
                    });
                };
                contract.getMarkPoint = function(attachmentId,  cb){
                    $.ajax({
                        type: "POST",
                        url: "/platform/getMarkPoint",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            AttachmentId: attachmentId
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("取标记点失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            alertState("取标记点成功", "info");
                            cb(true, data);
                        },
                        error: function () {
                            alertState("取标记点失败，网络异常", "failed");
                            cb(false, data);
                        }
                    });
                };
                contract.addMarkPoint = function(attachmentId, time, content, cb){
                    $.ajax({
                        type: "POST",
                        url: "/platform/addMarkPoint",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            AttachmentId: attachmentId,
                            Time: time,
                            Content: content
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("添加标记点失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            alertState("添加标记点成功", "info");
                            cb(true, data);
                        },
                        error: function () {
                            alertState("添加标记点失败，网络异常", "failed");
                            cb(false, data);
                        }
                    });
                };
                contract.delMarkPoint = function(attachmentId, time, cb){
                    $.ajax({
                        type: "POST",
                        url: "/platform/delMarkPoint",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            AttachmentId: attachmentId,
                            Time: time
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("删除标记点失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            alertState("删除标记点成功", "info");
                            cb(true, data);
                        },
                        error: function () {
                            alertState("删除标记点失败，网络异常", "failed");
                            cb(false, data);
                        }
                    });
                };
                contract.initCheckAttachment = function(data, _cb_operAttachment){
                    var curAttachmentId = 0;
                    $('.check_deleteAttachment').unbind('click').click(function (e) {
                        var id = $(e.currentTarget).attr('value');
                        contract.delAttachment(id, _cb_operAttachment);
                    });
                    $('.check_addAttachment').unbind('click').click(function(e){
                        var elParent = $('.check_attachmentSelector_');
                        var elAttachment = $('.check_attachmentOther_');
                        contract.addAttachment(_cb_operAttachment, elAttachment, elParent);
                    });
                    $('.check_attachment_object').unbind('click').click(function(e){
                        var elParent = $('.check_attachmentViewer_');
                        var elAttachment = $('.defaultViewer');
                        var elMarkPoints = $('.check_markPointList');
                        var objInfo = contract.getAttachmentData($(e.currentTarget).attr("value"), data);
                        curAttachmentId = $(e.currentTarget).attr("value");
                        contract.getMarkPoint(curAttachmentId,  _cb_getMarkPoint);
                        function _cb_getMarkPoint(bSuccess, data){
                            if (!bSuccess)
                                return;
                            var tem = Template.get('template/contract/cSeg_attachment_markPoints.html');
                            var r = tem({MarkPoints: data, IsService: contract.data.IsService});
                            $('.markPoints_').html(r);
                            $('.delMarkPoint').unbind('click').click(function(e){
                                var time = $(e.currentTarget).attr("value");
                                contract.delMarkPoint(curAttachmentId, time, function(bSuccess, data){
                                    if (bSuccess)
                                        contract.getMarkPoint(curAttachmentId, _cb_getMarkPoint);
                                });
                                return false;
                            });
                            $('.markpointItem').unbind('click').click(function(e){
                                var time = $(e.currentTarget).find('.markpointTime').text();
                                time = TimeToSec(time);
                                $.videoSeek(time);
                                $.videoPause();
                            });
                            $('.addMarkPoint').unbind('click').click(function(e){
                                var content = $('.markPoint_input_').val();
                                var time = $('.markPoint_time_').text();
                                contract.addMarkPoint(curAttachmentId, time, content, function(bSuccess, data){
                                    if (bSuccess){
                                        contract.getMarkPoint(curAttachmentId, _cb_getMarkPoint);
                                    }
                                })
                            });
                            $('.yes').unbind('click').click(function(){
                                $.ajax({
                                    type: "POST",
                                    url: "/platform/ContractAttachmentIsPassed",
                                    dataType: "json",
                                    contentType: "application/json",
                                    data: JSON.stringify({AttachmentId: curAttachmentId}),
                                    success: function (data) {
                                        _cb_operAttachment(data);
                                    },
                                    error: function () {
                                        alert("失败，网络异常");
                                    }
                                });
                            });
                            $('.no').unbind('click').click(function(){
                                $.ajax({
                                    type: "POST",
                                    url: "/platform/ContractAttachmentIsReject",
                                    dataType: "json",
                                    contentType: "application/json",
                                    data: JSON.stringify({AttachmentId: curAttachmentId}),
                                    success: function (data) {
                                        _cb_operAttachment(data);
                                    },
                                    error: function () {
                                        alert("失败，网络异常");
                                    }
                                });
                            });
                            var markTime = '', markContent = '';
                            $(data).each(function(index, value){
                                var t = TimeToSec(value.Time);
                                markTime += (t + '|');
                                markContent += (value.Content + '|');
                            });
                            $.extend($().voSetup, $().voDefaultSetup({
                                name: objInfo.name,
                                path: objInfo.path,
                                type: objInfo.type,
                                el_hide: elAttachment,
                                el_show: elParent,
                                bHasSpace: false,
                                markPos: markTime,
                                marks: markContent,
                                cb: function(status){
                                    if (status == 'hide')
                                        elMarkPoints.hide();
                                    else
                                        elMarkPoints.show();
                                },
                                timeCB: function(t){
                                    var text = Number(t).formatTime();
                                    $(".markPoint_time_").text(text);
                                }
                            }));
                            $().ViewObject();
                        }
                    });
                    $('.check_downloadAttachment').unbind('click').click(function(e){
                        contract.downloadAttachment($(e.currentTarget).attr("value"), data);
                    });
                };
                contract.initAttachment = function(data, _cb_operAttachment){
                    var selector = $('#contract-content');
                    selector.find('.deleteAttachment').unbind('click').click(function (e) {
                        if(confirm("您确认要删除此文件吗？")){
                            var id = +$(e.currentTarget).attr('value');
                            contract.delAttachment(id, _cb_operAttachment);
                        }else
                            return;
                    });
                    selector.find('.addAttachment').unbind('click').click(function(e){
                        var elParent = $('.attachmentSelector_');
                        var elAttachment = $('.attachmentContainer_');
                        contract.addAttachment( _cb_operAttachment, elAttachment, elParent);
                    });
                    selector.find('.attachment_object').unbind('click').click(function(e){
                        var type = $(e.currentTarget).parent().attr("value");
                        var elParent = $(e.currentTarget).closest('.attachmentContainer_' + type).prev('.attachmentViewer_' + type);
                        var elAttachment = $(e.currentTarget).closest('.attachmentContainer_' + type);
                        var objInfo = contract.getAttachmentData($(e.currentTarget).attr("value"), data);
                        $.extend($().voSetup, $().voDefaultSetup({
                            name: objInfo.name,
                            path: objInfo.path,
                            type: objInfo.type,
                            el_hide: elAttachment,
                            el_show: elParent
                        }));
                        $().ViewObject();
                    });
                    selector.find('.downloadAttachment').unbind('click').click(function(e){
                        contract.downloadAttachment($(e.currentTarget).attr("value"), data);
                    });
                    selector.find('.saveAttachment').unbind('click').click(function(e){
                        var id = $(e.currentTarget).attr("value");
                        var destObjId = 0;
                        Storage.filePickerDialog.open($('.contractAttachments'), function (files) {
                            if (files && files.length > 0)
                                destObjId = files[0].Id;
                            $.ajax({
                                type: "POST",
                                url: "/cloud/saveToMyStorage",
                                dataType: "json",
                                contentType: "application/json",
                                data: JSON.stringify({
                                    attachmentId: id,
                                    destObjId: destObjId
                                }),
                                success: function (data) {
                                    if (!isResponseDataAvailable(data)) {
                                        alertState("保存到媒体库失败.问题描述: " + data.errorMsg, "info");
                                        alert('保存失败');
                                        return;
                                    }
                                    alert('保存成功');
                                    alertState("保存到媒体库成功", "info");
                                    $('.contractAttachments').html('');
                                },
                                error: function () {
                                    alertState("保存到媒体库失败，网络异常", "failed");
                                }
                            });
                        }, true);
                    });
                };
                contract.getAttachmentData = function(attachId, attachments){
                    var obj = {};
                    var result = {};
                    $(attachments).each(function(index, value){
                        if (value.Id == attachId)
                            obj = value.Object;
                    });
                    result["path"] = obj.File.Path;
                    if (obj.Type == 0 || obj.Type == 2)
                        result["path"] = obj.File.VideoFile;
                    result["type"] = obj.Type;
                    result["name"] = obj.Name;
                    return result;
                };
                contract.downloadAttachment = function(attachId, attachments){
                    var obj = {};
                    $(attachments).each(function(index, value){
                        if (value.Id == attachId)
                            obj = value.Object;
                    });
                    var DownloadUrl=$.getDownloadURL(obj.File.FileCode,obj.Type);
                    $().downloadPermission(obj.Id, 'contractAttachment', function(bSuccess){
                        if (bSuccess)
                            window.open(DownloadUrl);
                    })
                };
                contract.addAttachment = function( cbFun, el_hide, el_show){
                    el_hide.hide();
                    Storage.filePickerDialog.open(el_show, function (file) {
                        var param = {ContractId: contract.data.ContractId};
                        if (file.length == 0) {
                            hideSelector(el_hide, el_show);
                            return;
                        }
                        var bRepeat = false;
                        var repeatFile = "";
                        $(contract.data.attachments).each(function(i, attachment){
                            $(file).each(function(index, value){
                                if (attachment.Object.Name == value.Name){
                                    bRepeat = true;
                                    repeatFile = value.Name;
                                }
                            })
                        });
                        if (bRepeat) {
                            confirm("文件：" + repeatFile + "无法重复上传");
                            return;
                        }
                        param = $.extend({uploadFiles: file}, param);
                        $.ajax({
                            type: "POST",
                            url: "/platform/addContractAttachment",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(param),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    hideSelector(el_hide, el_show);
                                    return;
                                }
                                cbFun(data);
                                hideSelector(el_hide, el_show);

                            },
                            error: function () {
                                hideSelector(el_hide, el_show);
                            }
                        });
                    });
                    function hideSelector(org, selector){
                        selector.html("");
                        org.show();
                        $("body,html").animate({scrollTop:org.closest('.attachmentArea').offset().top}, 200);
                    }
                };
                contract.getAttachment = function( cbFun){
                    $.ajax({
                        type: "POST",
                        url: "/platform/getContractAttachment",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            conId: contract.data.ContractId
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("获取附件失败.问题描述: " + data.errorMsg, "info");
                                return;
                            }
                            cbFun(data);
//                            contract.data.attachments = data;
                        },
                        error: function () {
                            alertState("获取附件失败，网络异常", "failed");
                        }
                    });
                };
                contract.getDomainUser = function(cb){
                    $.ajax({
                        type: "POST",
                        url: '/share/getDomainInfo',
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({}),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("获取附件失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            cb(true, data);
                        },
                        error: function () {
                            alertState("获取附件失败，网络异常", "failed");
                        }
                    });
                };
                contract.delGroupUser = function(userId, cb){
                    $.ajax({
                        type: "POST",
                        url: '/platform/editContractUser',
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            UserId: userId,
                            ContractId: contract.id,
                            Operator: 'del'
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("删除合同用户失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            cb(true, data);
                        },
                        error: function () {
                            alertState("删除合同用户失败，网络异常", "failed");
                        }
                    });
                };
                contract.modifyGroupUser = function(userId, description, cb){
                    $.ajax({
                        type: "POST",
                        url: '/platform/editContractUser',
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            UserId: userId,
                            ContractId: contract.id,
                            Description: description,
                            Operator: 'modify'
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("修改合同用户备注失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            cb(true, data);
                        },
                        error: function () {
                            alertState("修改合同用户备注失败，网络异常", "failed");
                        }
                    });
                };
                contract.specifyResponser = function(userId, segId, cb){
                    $.ajax({
                        type: "POST",
                        url: '/platform/specifySegmentResponser',
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            UserId: userId,
                            SegmentId: segId
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("指定合同环节负责人失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            cb(true, data);
                        },
                        error: function () {
                            alertState("指定合同环节负责人失败，网络异常", "failed");
                        }
                    });
                };
                contract.addGroupUser = function(usersId, cb){
                    $.ajax({
                        type: "POST",
                        url: '/platform/editContractUser',
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            UsersId: usersId,
                            ContractId: contract.id,
                            Operator: 'add'
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("添加合同用户失败.问题描述: " + data.errorMsg, "info");
                                cb(false, data);
                                return;
                            }
                            cb(true, data);
                        },
                        error: function () {
                            alertState("添加合同用户失败，网络异常", "failed");
                        }
                    });
                };
                contract.delAttachment = function(id, cbFun){
                    $.ajax({
                        type: "POST",
                        url: "/platform/delContractAttachment",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({AttachmentId: id}),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("删除附件失败.问题描述: " + data.errorMsg, "info");
                                return;
                            }
                            cbFun(data);
                        },
                        error: function () {
                            alertState("删除附件失败，网络异常", "failed");
                        }
                    });
                };
                contract.initSeg = function(req){
                    var selector = $('.nav-cState');
                    $("#curseg"+req.Status).addClass("active");
                    selector.find('.apply_cSeg_btn').unbind('click').click(function (e) {
                        contract.applySeg(req);
                    });
                    selector.find('.confirm_cSeg_btn').unbind('click').click(function (e) {
                        contract.confirmSeg(req);
                    });
                    selector.find('.reject_cSeg_btn').unbind('click').click(function (e) {
                        contract.rejectSeg(req);
                    });
                    selector.find(".ContractOver").unbind("click").click(function(){
                        if (!confirm("确认成片后，制作费用将会付给制作商，请确认已经下载成片"))
                            return;
                        $.ajax({
                            type: "POST",
                            url: "/platform/ContractOver",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                conId: req.ContractId,
                                reqId:req.Id
                            }),
                            success: function (data) {
                                window.location.reload();
                            },
                            error: function () {
                                alert("失败，网络异常");
                            }
                        });
                    });
                    $(".cSeg").unbind("click").click(function(){
                        var sg = $(this).children('input').val();
                        if(req.Status<sg)return;
                        $(".cSeg").removeClass("active");
                        $(this).addClass("active");
                        switch (Math.floor(sg)){
                            case ContractClass.ContractSegment.establish:
                                contract.toEstablishSeg(req);
                                break;
                            case ContractClass.ContractSegment.payRent:
                                contract.toPayRentSeg(req);
                                break;
                            case ContractClass.ContractSegment.review:
                                contract.toReview(req);
                                break;
                            case ContractClass.ContractSegment.payall:
                                contract.toPayAll(req);
                                break;
                            case ContractClass.ContractSegment.retainage:
                                contract.toRetainage(req);
                                break;
                            case ContractClass.ContractSegment.finish:
                                contract.toEnd(req);
                                break;
                        }
                    });

                };
                contract.toSeg = function(req){
                    contract.data = req;
                    contract.data.activeSeg = req.Status;
                    contract.data.IsService = $().retrieveSession().IsService;
                    contract.data.DomainId = $().retrieveSession().DomainId;
                    contract.data.UserId = $().retrieveSession().UserId;
                    contract.data.filter = $('#req_avtive_bar').attr('value'); //by zhh on 2016-10-24

                    var tem = Template.get('template/contract/nav.html');
                    var r = tem(contract.data);
                    $('#pageContent').html(r);

                    contract.initSeg(req);
                    switch (Math.floor(req.Status)){
                        case ContractClass.ContractSegment.establish:
                            contract.toEstablishSeg(req);
                            break;
                        case ContractClass.ContractSegment.payRent:
                            contract.toPayRentSeg(req);
                            break;
                        case ContractClass.ContractSegment.review:
                            contract.toReview(req);
                            break;
                        case ContractClass.ContractSegment.payall:
                            contract.toPayAll(req);
                            break;
                        case ContractClass.ContractSegment.retainage:
                        case ContractClass.ContractSegment.finish:
                            contract.toRetainage(req);
                            break;
                    }

                    //by zhh on 2016-10-24
                    $('.req-statusBar').unbind('click').click(function (e) {
                        $('.req-statusBar').removeClass('active');
                        $(e.currentTarget).addClass('active');
                        $().GoToUrl('/requirementPage', {c1: req.Category_1, c2: req.Category_2, filter: $(e.currentTarget).attr('value')});
                    });
                };
                contract.toCreateSeg = function(segment){
                    var tem = Template.get('template/contract/cSeg_create.html');
                    var r = tem(contract.data);
                    var selector = '.contractState_' + contract.id;
                    $(selector).html(r);
                };
                contract.toEstablishSeg = function(req){
                    var tem = Template.get('template/contract/detail.html');
                    var r = tem(req);
                    $( '#contract-content').html(r);
                    $('.deleteAttachment').unbind('click').click(function (e) {
                        var id = $(e.currentTarget).attr('value');
                        req.deleteAttachment(id, function(bSuccess){
                            if (bSuccess){
                                $(e.currentTarget).parent().parent()[0].outerHTML = '';
                                window.location.reload();
                            }
                        });
                    });
                    tem = Template.get('template/requirement/suggest.html');
                    var vs = $('#c-suggestion');
                    if (req.replys == undefined)
                        req.replys = {};
                    vs.html(tem(req.replys));
                    req.deleteAttachment = function(id, cb){
                        $.ajax({
                            type: "POST",
                            url: "/platform/delRequirementAttachment",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                AttachmentId: id
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("删除需求附件失败.问题描述: " + data.errorMsg, "info");
                                    cb(false);
                                    return;
                                }
                                alertState('删除需求附件成功');
                                cb(true);
                            },
                            error: function () {
                                alertState("删除需求附件失败，网络异常", "failed");
                                cb(false);
                            }
                        });
                    };
                    $('.attachment_object').unbind('click').click(function(e){
                        var id = $(e.currentTarget).attr("value");
                        var obj = {};
                        $(req.RequirementAttachment).each(function(index, value){
                            if (value.Id == id)
                                obj = value.Object;
                        });
                        var path = obj.File.Path;
                        if (obj.Type == 0 || obj.Type == 2)
                            path = obj.File.VideoFile;
                        req.viewAttachment(obj.Name, path, obj.Type);
                    });
                    req.viewAttachment = function(name, path, type){
                        $.extend($().voSetup, $().voDefaultSetup({
                            name: name,
                            path: path,
                            type: type,
                            el_hide: $(".req_attachment_content"),
                            el_show: $('.req_attachment_viewer')
                        }));
                        $().ViewObject();
                    };
                    $('.download_attachment_object').unbind('click').click(function(e){
                        var id = $(e.currentTarget).attr("value");
                        var obj = {};
                        $(req.RequirementAttachment).each(function(index, value){
                            if (value.Id == id)
                                obj = value.Object;
                        });
                        var DownloadUrl=$.getDownloadURL(obj.File.FileCode,obj.Type);
                        $().downloadPermission(obj.Id, 'requirementAttachment', function(bSuccess){
                            if (bSuccess)
                                window.open(DownloadUrl);
                        });
                    });
                };
                contract.toPayRentSeg = function() {
                    $.ajax({
                        type: "POST",
                        url: "/platform/contractOrder",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            ContractId: contract.data.ContractId,
                            OrderType: ContractClass.ContractOrderType.payRent
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("支付请求失败.问题描述: " + data.errorMsg, "info");
                                return;
                            }
                            _cb_contractOrder(data);
                        },
                        error: function () {
                            alertState("支付请求失败，网络异常", "failed");
                        }
                    });
                    function _cb_contractOrder(data){
                        contract.data.rentOrder = data;
//                        contract.data.rentOrder["bCanPay"] = $().userHasRight("Con_Pay");
                        var tem = Template.get('template/contract/contract_deposit.html');
                        var r = tem({
                            data :contract.data,
                            IsService : $().retrieveSession().IsService
                        });
                        $('#contract-content').html(r);
                        var e_useCount = $("#UseCount");
//                        contract.initSeg(segment);
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
                            else if(data.PayUser.Domain.Count < e_useCount.val()){
                                e_useCount.focus();
                                if (data.PayUser.Domain.Count > data.Amount)
                                    e_useCount.val(data.Amount);
                                else
                                    e_useCount.val(data.PayUser.Domain.Count);
                            }
                            else if (data.Amount - e_useCount.val() < 0){
                                e_useCount.val(data.Amount);
                            }
                            $("#price").text((data.Amount - e_useCount.val()) + '元');
                        }
                        $('#payDeposit_btn').unbind('click').click(function (e) {
                            check_useCount();
                            var useAccount = e_useCount.val();
                            if (useAccount == '')
                                useAccount = 0;
                            $().alipayProcess(
                                '支付合同押金',
                                data.SerialNumber,
                                data.Id,
                                data.Amount,
                                useAccount,
                                data.Receiver.Domain.CompanyName,
                                function(bSuccess) {
                                    if (bSuccess)
                                        window.location.reload();
                                }
                            );
                        });
                        $('#denyDeposit_btn').unbind('click').click(function (e) {
                            $.ajax({
                                type: "POST",
                                url: "/platform/denyDeposit",
                                dataType: "json",
                                contentType: "application/json",
                                data: JSON.stringify({
                                    RequirementId: contract.data.Id,
                                    ServiceUserId: contract.data.ServiceUserId
                                }),
                                success: function (data) {
                                    if (!isResponseDataAvailable(data)) {
                                        alertState("反悔操作失败.问题描述: " + data.errorMsg, "info");
                                        return;
                                    }
                                    window.location.reload();
                                },
                                error: function () {
                                    alertState("反悔操作失败，网络异常", "failed");
                                }
                            });
                        });
                    }
                };
                contract.toReview = function(){
                    contract.getAttachment( _cb_getAttachment);
                    function _cb_getAttachment(data){
                        var tem = Template.get('template/contract/cSeg_checkAttachments.html');
                        var param = {
                            IsService:  $().retrieveSession().IsService,
                            bShowSegment: false,
                            bBoth: false,
                            bCustomer: false,
//                            不能定死 需要修改
                            bService: $().retrieveSession().IsService,
                            customerTitle: "需求方附件",
                            serviceTitle: "素材列表",
                            CustomerUserId: contract.data.CustomerUserId,
                            ServiceUserId: contract.data.ServiceUserId,
                            ServiceUserName: contract.data.ServiceUser.Domain.CompanyName,
                            ServiceUserDomainId: contract.data.ServiceUser.DomainId,
                            ContractAttachment: data,
                            bDownload: false,
                            bClose: true,
                            size: 1,
                            bApplying: contract.data.ApplyStatus,
                            activeSeg: contract.data.activeSeg
                        };
                        $('#contract-content').html(tem(param));
                        contract.initCheckAttachment(data, _cb_operAttachment);
                    }
                    function _cb_operAttachment(data){
                        contract.getAttachment(_cb_getAttachment);
                    }
                };
                contract.toPayAll = function(){
                    $.ajax({
                        type: "POST",
                        url: "/platform/contractOrder",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            ContractId: contract.data.ContractId,
                            OrderType: ContractClass.ContractOrderType.payRest
                        }),
                        success: function (data) {
                            if (!isResponseDataAvailable(data)) {
                                alertState("支付请求失败.问题描述: " + data.errorMsg, "info");
                                return;
                            }
                            _cb_contractOrder(data);
                        },
                        error: function () {
                            alertState("支付请求失败，网络异常", "failed");
                        }
                    });
                    function _cb_contractOrder(data){
                        contract.data.restOrder = data;
                        var tem = Template.get('template/contract/cSeg_payAll.html');
                        var r = tem(contract.data);
                        $('#contract-content').html(r);
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
                            else if(data.PayUser.Domain.Count < e_useCount.val()){
                                e_useCount.focus();
                                if (data.PayUser.Domain.Count > data.Amount)
                                    e_useCount.val(data.Amount);
                                else
                                    e_useCount.val(data.PayUser.Domain.Count);
                            }
                            else if (data.Amount - e_useCount.val() < 0){
                                e_useCount.val(data.Amount);
                            }
                            $("#price").text((data.Amount - e_useCount.val()) + '元');
                        }
                        $('#payAll_btn').unbind('click').click(function (e) {
                            check_useCount();
                            var useAccount = e_useCount.val();
                            if (useAccount == '')
                                useAccount = 0;
                            $().alipayProcess(
                                '支付合同尾款',
                                data.SerialNumber,
                                data.Id,
                                data.Amount,
                                useAccount,
                                data.Receiver.Domain.CompanyName,
                                function(bSuccess) {
                                    if (bSuccess)
                                        window.location.reload();
                                }
                            );
                        });
                        $('#denyPayAll_btn').unbind('click').click(function (e) {
                            $.ajax({
                                type: "POST",
                                url: "/platform/denyPayAll",
                                dataType: "json",
                                contentType: "application/json",
                                data: JSON.stringify({
                                    reqId: contract.data.Id,
                                    conId: contract.data.ContractId
                                }),
                                success: function (data) {
                                    if (!isResponseDataAvailable(data)) {
                                        alertState("反悔操作失败.问题描述: " + data.errorMsg, "info");
                                        return;
                                    }
                                    window.location.reload();
                                },
                                error: function () {
                                    alertState("反悔操作失败，网络异常", "failed");
                                }
                            });
                        });
                    }
                };


                contract.toRetainage = function(){
                    var tem = Template.get('template/contract/cSeg_submit.html');
                    var r = tem(contract.data);
                    $('#contract-content').html(r);
                    contract.getAttachment( _cb_getAttachment);
                    function _cb_getAttachment(data){
                        var tem = Template.get('template/contract/contract_attachments.html');
                        var param = {
                            IsService: contract.data.IsService,
                            bShowSegment: false,
                            bBoth: false,
                            bCustomer: false,
//                            不能定死 需要修改
                            bService: $().retrieveSession().IsService,
                            customerTitle: "需求方附件",
                            serviceTitle: "制作方附件",
                            CustomerUserId: contract.data.CustomerUserId,
                            ServiceUserId: contract.data.ServiceUserId,
                            ContractAttachment: data,
                            bDownload: true,
                            bClose: false,
                            size: 1
                        };
                        $('.attachment_area').html(tem(param));
                        $('#comment-producer').unbind('click').click(function(){
                            contract.toEnd(contract.data);
                        });
                        contract.initAttachment(data, _cb_operAttachment);
                    }
                    function _cb_operAttachment(data){
                        contract.getAttachment( _cb_getAttachment);
                    }
                };
                contract.toEnd = function(req){
                    var tem = Template.get('template/contract/finish.html');
                    var star = new Array(4);
                    for(var i=0;i<5;i++){
                        star[i] = i;
                    }
                    $( '#contract-content').html(tem({star:star,req:req,IsService:contract.data.IsService}));
                    var cs = req.Star;
                    $('.star').unbind('click').click(function(){
                        if ($(this).hasClass('glyphicon-star-empty')) {
                            $(this).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
                            cs = $(this).attr('value');
                        }
                        else {
                            $(this).removeClass('glyphicon-star').addClass('glyphicon-star-empty');
                            cs = $(this).attr('value') - 1;
                        }
                        $(this).prevAll('.star').removeClass('glyphicon-star-empty').addClass('glyphicon-star');
                        $(this).nextAll('.star').removeClass('glyphicon-star').addClass('glyphicon-star-empty');
                    });
                    $('#submit-comment').unbind('click').click(function(){
                        if(cs==0){
                            alert('点击星级完成总体评分');
                        }
                        $.ajax({
                            type: "POST",
                            url: "/platform/finishComment",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                reqId: contract.data.Id,
                                comment:$('#finish-comment').val(),
                                star:cs
                            }),
                            success: function (data) {
                                window.location.reload();
                            },
                            error: function () {
                                alert("支付请求失败，网络异常");
                            }
                        });
                    });
                };
                contract.initGroupUser = function(){
                    var tem = Template.get('template/contract/groupUser.html');
                    var r = tem(contract.data);
                    var selector = $('#' + contract.id);
                    selector.find('#contractUserGroup_' + contract.id).html(r);
                    selector.find('.saveContractUser').hide();
                    selector.find('.cancelModifyUser').hide();
                    selector.find('.input_userDes').hide();
                    selector.find('.addContractUserGroup').unbind('click').click(function(){
                        contract.getDomainUser(function(bSuccess, data){
                            if (bSuccess){
                                var tem = Template.get('template/contract/addGroupUser.html');
                                var vs = $('#addGroupUserModal');
                                if (vs.length == 0) {
                                    $('#pageContent').append('<div id="addGroupUserModal" class="modal fade bs-example-modal-sm"></div>');
                                }
                                vs = $('#addGroupUserModal');
                                $(data.Users).each(function(index, value){
                                    value['bChecked'] = false;
                                    $(contract.data.ContractUserGroup).each(function(i, v){
                                        if (value.Id == v.UserId)
                                            value.bChecked = true;
                                    });
                                });
                                vs.html(tem(data));
                                $("#addGroupUser_cancel").unbind('click').click(function () {
                                    vs.modal('hide');
                                });
                                $("#addGroupUser_commit").unbind('click').click(function () {
                                    var users = $('.searchUser_check').find('input:checked').parent().parent().find('.searchUser_id');
                                    var usersId = [];
                                    $(users).each(function(i, value){
                                        usersId.push($(value).text());
                                    });
                                    contract.addGroupUser(usersId, function(bSuccess, data){
                                        if (bSuccess){
                                            contract.data.ContractUserGroup = data;
                                            contract.initGroupUser();
                                        }
                                    });
                                    vs.modal('hide');
                                });
                                vs.modal();
                            }
                            else
                                selector.find('.buyDomain').show();
                        });
                    });
                    selector.find('.delContractUser').unbind('click').click(function(e){
                        var userId = $(e.currentTarget).parent().attr('value');
                        var userCount = 0;
                        $(contract.data.ContractUserGroup).each(function(i, v){
                            if ($().retrieveSession().DomainId == v.DomainId)
                                userCount++;
                        });
                        if (userCount <= 1) {
                            alert("至少需要一个合同成员!");
                            return;
                        }
                        contract.delGroupUser(userId, function(bSuccess, data){
                            if (bSuccess){
                                contract.data.ContractUserGroup = data;
                                $.each(contract.data.ContractSegment, function(key, value){
                                    if (value.ServiceResponser == userId){
                                        value.ServiceResponserName = '';
                                        value.ServiceResponserDes = '';
                                    }
                                    else if (value.CustomerResponser == userId){
                                        value.CustomerResponserName = '';
                                        value.CustomerResponserDes = '';
                                    }
                                });
                                contract.initGroupUser();
                            }
                        });
                    });
                    selector.find('.modifyContractUser').unbind('click').click(function(e){
                        var text = $(e.currentTarget).parent().parent().parent().find('.text_userDes');
                        var input = $(e.currentTarget).parent().parent().parent().find('.input_userDes');
                        var save = $(e.currentTarget).parent().find('.saveContractUser');
                        var cancel = $(e.currentTarget).parent().find('.cancelModifyUser');
                        var modify = $(e.currentTarget).parent().find('.modifyContractUser');
                        modify.hide();
                        text.hide();
                        input.val(text.text());
                        save.show();
                        cancel.show();
                        input.show();
                    });
                    selector.find('.saveContractUser').unbind('click').click(function(e){
                        var text = $(e.currentTarget).parent().parent().parent().find('.text_userDes');
                        var input = $(e.currentTarget).parent().parent().parent().find('.input_userDes');
                        var save = $(e.currentTarget).parent().find('.saveContractUser');
                        var cancel = $(e.currentTarget).parent().find('.cancelModifyUser');
                        var modify = $(e.currentTarget).parent().find('.modifyContractUser');
                        var userId = $(e.currentTarget).parent().attr('value');
                        contract.modifyGroupUser(userId, input.val(), function(bSuccess, data){
                            if (bSuccess){
                                contract.data.ContractUserGroup = data;
                                $.each(contract.data.ContractSegment, function(key, value){
                                    if (value.ServiceResponser == userId)
                                        value.ServiceResponserDes = input.val();
                                    else if (value.CustomerResponser == userId)
                                        value.CustomerResponserDes = input.val();
                                });
                                contract.initGroupUser();
                                input.hide();
                                save.hide();
                                cancel.hide();
                                text.text(input.val());
                                text.show();
                                modify.show();
                            }
                        });
                    });
                    selector.find('.cancelModifyUser').unbind('click').click(function(e){
                        var text = $(e.currentTarget).parent().parent().parent().find('.text_userDes');
                        var input = $(e.currentTarget).parent().parent().parent().find('.input_userDes');
                        var save = $(e.currentTarget).parent().find('.saveContractUser');
                        var cancel = $(e.currentTarget).parent().find('.cancelModifyUser');
                        var modify = $(e.currentTarget).parent().find('.modifyContractUser');
                        input.hide();
                        save.hide();
                        cancel.hide();
                        text.show();
                        modify.show();
                    });
                    selector.find('.modifyResponser').unbind('click').click(function(e){
                        var segmentId = $(e.currentTarget).attr('value');
                        var tem = Template.get('template/contract/specifyResponser.html');
                        var vs = $('#specifyResponserModal');
                        if (vs.length == 0) {
                            $('#pageContent').append('<div id="specifyResponserModal" class="modal fade bs-example-modal-sm"></div>');
                        }
                        vs = $('#specifyResponserModal');
                        var segment;
                        $(contract.data.ContractSegment).each(function(i, v){
                            if (segmentId == v.Id)
                                segment = v;
                        });
                        vs.html(tem({
                            DomainId: $().retrieveSession().DomainId,
                            Segment: segment,
                            ContractUserGroup: contract.data.ContractUserGroup
                        }));
                        $("#specifyResponser_cancel").unbind('click').click(function () {
                            vs.modal('hide');
                        });
                        $("#specifyResponser_commit").unbind('click').click(function () {
                            var userId = $('.specifyUser_check').find('input:checked').parent().parent().find('.specifyUser_id').text();
                            contract.specifyResponser(userId, segmentId, function(bSuccess, data){
                                if (bSuccess){
                                    $.each(contract.data.ContractSegment, function(key, value){
                                        if (value.Id == segmentId){
                                            if ($().retrieveSession().IsService){
                                                value.ServiceResponserDes = data.Description;
                                                value.ServiceResponser = data.UserId;
                                                value.ServiceResponserName = data.User.NickName;
                                            }
                                            else{
                                                value.CustomerResponserDes = data.Description;
                                                value.CustomerResponser = data.UserId;
                                                value.CustomerResponserName = data.User.NickName;
                                            }
                                        }
                                    });
                                    contract.initGroupUser();
                                }
                            });
                            vs.modal('hide');
                        });
                        vs.modal();
                    });
                    selector.find('.gotoUserCenter').unbind('click').click(function(){
                        $().GoToUrl('/UpdataPage');
                    });
                };
                contract.viewGroup = function(){
                    var uid = -1;
                    if (contract.data.activeReply){
                        uid = contract.data.activeReply;
                        contract.data.activeReply = -1;
                    }
                    var selector = $('#' + contract.id);
                    var tem = Template.get('template/contract/contract_reply.html');
                    selector.find('#addUser_' + contract.id).html(tem({data: contract.data, activeUser: uid}));
                    contract.viewReply(uid, true);
                    selector.find('.replyItem').unbind('click').click(function(e){
                        selector.find('.replyItem').removeClass('active');
                        $(e.currentTarget).addClass('active');
                        var id = $(e.currentTarget).attr('value');
                        contract.viewReply(id, false);
                    });
                };
                contract.viewReply = function(userId, bForce){
                    if (contract.data.replys == undefined)
                        contract.data.replys = {};
                    if (userId in contract.data.replys && !bForce) {
                        initReplyBoard();
                        return;
                    }
                    var param = {
                        Id: contract.id
                    };
                    if (userId != -1)
                        param['UserId'] = userId;
                    $.ajax({
                        type: "POST",
                        url: "/platform/contractReply",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify(param),
                        success: function (response) {
                            if (!isResponseDataAvailable(response)) {
                                alertState("获取留言板信息失败.问题描述: " + response.errorMsg, "info");
                                initReplyBoard();
                                return;
                            }
                            contract.data.replys[userId] = response;
                            initReplyBoard();
                        }
                    });
                    function initReplyBoard() {
                        var tem = Template.get('template/contract/replyBoard.html');
                        var r = tem({reply: contract.data.replys[userId], UserId: $().retrieveSession().UserId});
                        var selector = '#' + contract.id;
                        var dialog = $(selector).find('#contractUser_replayBoard');
                        dialog.html(r);
                        dialog.find('.replyBtn').unbind('click').click(function () {
                            reply();
                        });
                        dialog.find('.refreshBtn').unbind('click').click(function () {
                            contract.viewReply(userId, true);
                        });
                    }
                    function reply(){
                        var param = {
                            ContractId: contract.id,
                            Reply: $('.replyTextArea').val()
                        };
                        if (userId != -1)
                            param['DestUserId'] = userId;
                        $.ajax({
                            type: "POST",
                            url: "/platform/publishContractReply",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(param),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("回复信息失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                alertState("回复信息成功", "success");
                                contract.viewReply(userId, true);
                            },
                            error: function () {
                                alertState("回复信息失败，网络异常", "failed");
                            }
                        });
                    }
                };
                return contract;
            }
        };
        var contracts = {};
        var openContractId = 0;
        function parseDate(date) {
            var d = new Date(date);
            return d.Format("MM/dd/yyyy");
        }
        Template.helper("ContractStatusTranslator", function (Status) {
            var _status = {0: "已申请", 1: "商讨合同", 2: "申请确认", 3: "合同确认，等待付款", 4: "已确认，正在执行", 5: "成片获取", 6: "完成"};
            return _status[Status];
        });
        Template.helper('ContractStepTabWidth', function (ContractSegment) {
            var width = ContractSegment.size * 120;
            return width;
        });
        Template.helper('htmlEncode', function (content) {
            return htmlEncode(content);
        });
        Template.helper("renderContractAttachment", function (code,name) {
            return '<a href="/platform/downloadAttachment/'+code+'?DBToken='+$().retrieveSession().DBToken+'">'+name+'</a>';
        });
        Template.helper("ParseTime", parseDate);
        Template.helper("ParseTime2", function (date) {
            var d = new Date(date);
            return d.Format("yyyy-MM-dd");
        });
        function getCUserReplyBoard(contractId, contractUserId, data, bForce){
            if (contractUserId == undefined)
                return;
            data.ContractUserId = contractUserId;
            data.UserId = $().retrieveSession().UserId;
            if (data.replys == undefined)
                data.replys = {};
            if (contractId in data.replys && !bForce) {
                initReplyBoard();
                return;
            }
            $.ajax({
                type: "POST",
                url: "/platform/contractReply",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    Id: contractId
                }),
                success: function (response) {
                    if (!isResponseDataAvailable(response)) {
                        alertState("获取留言板信息失败.问题描述: " + response.errorMsg, "info");
                        initReplyBoard();
                        return;
                    }
                    data.replys[contractId] = response;
                    initReplyBoard();
                }
            });
            function initReplyBoard() {
                var tem = Template.get('template/contract/replyBoard.html');
                var r = tem(data);
                var temp = "#addUser_" + contractId;
                var dialog = $(temp).find('#contractUser_replayBoard');
                dialog.html(r);
                dialog.find('.replyBtn').unbind('click').click(function (e) {
                    reply();
                });
                dialog.find('.refreshBtn').unbind('click').click(function (e) {
                    getCUserReplyBoard(contractId, contractUserId, data, true);
                });
            }
            function reply(){
                $.ajax({
                    type: "POST",
                    url: "/platform/publishContractReply",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ContractId: contractId,
                        Reply: $('.replyTextArea').val()
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("回复信息失败.问题描述: " + data.errorMsg, "info");
                            return;
                        }
                        alertState("回复信息成功", "success");
                        getCUserReplyBoard(contractId, contractUserId, data, false);
                    },
                    error: function () {
                        alertState("回复信息失败，网络异常", "failed");
                    }
                });
            }
        }
        function StartContract(req) {
            var contract = ContractClass.create();
            contract.toSeg(req);
        }
        function tips(temp) {
            $(temp).find(".scheme-check").popover({
                trigger: 'focus',
                title: '<red>请选择是否要进行拍摄审核</red>',
                content: "方案是服务商提供的关于视频制作的具体实施计划，需求方可以要求服务商提供方案并加以审核",
                html: true
            });
            $(temp).find(".script-check").popover({
                trigger: 'focus',
                title: '<red>请选择是否要进行剪辑审核</red>',
                content: "脚本是服务商提供的关于视频制作的场景描述和拍摄手法等计划，需求方可以要求服务商提供脚本并加以审核",
                html: true
            });
            $(temp).find(".clip-check").popover({
                trigger: 'focus',
                title: '<red>请选择是否要进行包装审核</red>',
                content: "服务商提供其用于视频制作的素材文件，需求方可以要求服务商提供可读素材并加以审核",
                html: true
            });
            $(temp).find(".final-check").popover({
                trigger: 'focus',
                title: '<red>请选择是否要进行配音审核</red>',
                content: "服务商完成视频制作后需生成视频，并提供给需求方，需求方可以要求服务商提供成片并加以审核",
                html: true
            });
            $(temp).find(".end-check").popover({
                trigger: 'focus',
                title: '<red>请选择审核日期</red>',
                content: "完成配音审核后，需求方可以向服务商提出一些细微修改要求，并在服务商修改后进行最成片审核核，该审核通过后代表作品已经完成",
                html: true
            });
            $(temp).find(".deadline-check").popover({
                trigger: 'focus',
                title: '<red>请选择合同截止日期</red>',
                content: "需求方和服务商约定任务截止日期，以合同方式给予承诺",
                html: true
            });
        }
        var contract_interface = {};
        contract_interface.pageRouter = {
            '/contractPage': StartContract
        };
        contract_interface.StartContract = StartContract;
        return contract_interface;
});