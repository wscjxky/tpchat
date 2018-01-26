 function isResponseDataAvailable(data) {
    if (data == null)
        return false;

    if (data.errorCode != null && data.errorCode == 3) {
        window.location.href = '/login#/loginPage';
        alert("您的账号已在其它地方登录，请尝试重新登录！", "info");
    }
    return (data.errorMsg == undefined);
}
var operLogs = [];

function alertState(msg, state) {
    var mydate = new Date();
    var t = mydate.toLocaleString();
    operLogs.push({msg: msg, level: state, time: t});
}
 function RequirementHandler() {
        var ContractSegment = {draft: 1, publish: 2, establish: 3, payRent: 4, review: 5, payall: 6, retainage: 7, finish: 8};
        this.reqPool = {};
        var cache_ = {requirements: {}, curPage: 1, IsService: null};
        var directToEdit = false;

        this.data = function(){
            return cache_;
        };
        this.init = function(){
            cache_.curPage = 1;
            cache_.curC1 = cache_.curC2 = 0;
            cache_.filter = 'all';
            cache_.requirements = {};
            cache_.IsService = $().retrieveSession().IsService;

            var params = $().GetParamsFromUrl();
            if (params.hasOwnProperty('filter'))
                cache_.filter = params['filter'];
            if (params.hasOwnProperty('c1'))
                cache_.curC1 = params['c1'];
            if (params.hasOwnProperty('c2'))
                cache_.curC2 = params['c2'];

            this.getRequirements(cache_.curPage);
        };
        this.getRequirements = function(page){ //获取需求列表
            cache_.curPage = page;
            var param = {Page: page, Category1: cache_.curC1, Category2: cache_.curC2, filter: cache_.filter};
            $.ajax({
                type: "POST",
                url: cache_.IsService ? "/platform/requirements" : "/platform/myRequirements",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(param),
                success: function (response) {
                    if (!isResponseDataAvailable(response)) {
                        alertState("获取需求数据失败.问题描述: " + response.errorMsg, "info");
                        return;
                    }
                    _cb_getRequirements(response);
                },
                error: function () {
                    alertState("获取需求信息失败，网络异常", "failed");
                }
            });
            function _cb_getRequirements(response){
                var requirements = response.Items;
                var category1 = response.Category1;
                var category2 = response.Category2;
                var CurUserId = $().retrieveSession().UserId;
                var pagination = $().calPagination(response.Page, response.Pages);
                cache_.curPage = response.Page;
                $.each(requirements, function (index, value) {
                    var followerCount = 0;
                    $(category1).each(function(i, v){
                        if (value.Category_1 == v.Id)
                            value.Type = v.Name;
                    });
                    $(category2).each(function(i, v){
                        if (value.Category_2 == v.Id)
                            value.Type += '+' + v.Name;
                    });
                    $(value.RequirementFollower).each(function(i, v){
                        if (!v.IsDeny)
                            followerCount++;
                        value.IsApplying = 0;
                        if (v.FollowerDomainId == $().retrieveSession().DomainId) {
                            value.IsApplying = v.Status;
                        }
                    });
                    value.followerCount = followerCount;
                    cache_.requirements[value.Id] = value;
                });

                var tem = Template.get("template/requirement/index.html");
                var r = tem({
                    IsService: $().retrieveSession().IsService,
                    requirements: requirements,
                    pagination: pagination,
                    category1: category1,
                    filter: cache_.filter,
                    curC1: cache_.curC1,
                    curC2: cache_.curC2,
                    CurUserId: CurUserId
                });
                $('#pageContent').html(r);

                $('.req-statusBar').unbind('click').click(function (e) {
                    $('.req-statusBar').removeClass('active');
                    $(e.currentTarget).addClass('active');
                    cache_.filter = $(e.currentTarget).attr('value');
                    $().GoToUrl('/requirementPage', {c1: cache_.curC1, c2: cache_.curC2, filter: cache_.filter});
                });
                $('.requirement-follower-portrait').unbind('click').click(function (e) {
                    window.open('/zone/' + $(e.currentTarget).attr('value'));
                });
                $('.edit-btn').unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr('value');
                    $().GoToUrl('#/requirement/' + id);
                });
                $('.view-btn').unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr('value');
                    $().GoToUrl('#/requirement/' + id);
                });
                $('.publish-btn').unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr('value');
                    var req = handler.getReq(id);
                    e.stopPropagation(); //阻止消息继续传播 by zhh on 2016-10-26
                    req.publish(null, function(bSuccess){
                        if (bSuccess)
                            handler.init();
                    });
                });
                $('.cancel-publish-btn').unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr('value');
                    var req = handler.getReq(id);
                    e.stopPropagation(); //阻止消息继续传播 by zhh on 2016-10-26
                    req.cancelPublish(function(bSuccess){
                    alert('meme');
                        if (bSuccess)
                            handler.init();
                    });
                });
                $('.cancel-apply-btn').unbind('click').click(function (e) {
                    e.stopPropagation(); //阻止消息继续传播 by zhh on 2016-10-27
                    if(!confirm('确认取消需求申请？'))
                        return;
                    var id = $(e.currentTarget).attr('value');
                    var req = handler.getReq(id);
                    req.cancelApply(function(bSuccess){
                        if (bSuccess)
                            handler.init();
                    });
                });

                var rp = $('#requirementPage');
                rp.find(".requirement_item").unbind('click').click(function (e) {
                    var id = $(e.currentTarget).find('.row_id').val();
                    var title = $(e.currentTarget).find(".requirement_title").text();
                    handler.showRequirement(id, true, title);
                });
                rp.find(".requirement_del_Btn").unbind('click').click(function (e) {
                    e.stopPropagation(); //阻止消息继续传播 by zhh on 2016-10-26
                    if (!confirm("是否确认删除该需求？"))
                        return false;
                    var id = $(e.currentTarget).attr('value');
                    handler.deleteRequirement(id, function(bSuccess){
                        if (bSuccess)
                            handler.init();
                    });
                    e.stopPropagation();
                });

                $('.pagination_index').unbind('click').click(function(e){
                    var page = parseInt($(e.currentTarget).attr('value'));
                    handler.getRequirements(page);
                });
                $('.pagination_prev').unbind('click').click(function(e){
                    var page = parseInt($(e.currentTarget).attr('value'));
                    handler.getRequirements(page);
                });
                $('.pagination_next').unbind('click').click(function(e){
                    var page = parseInt($(e.currentTarget).attr('value'));
                    handler.getRequirements(page);
                });

                $('.status-item').unbind('click').click(function(e){
                    var filter = $(e.currentTarget).attr('value');
                    $().GoToUrl('/requirementPage', {c1: 0, c2: 0, filter: filter});
                });
            }
        };
        this.getReq = function(id){
            var req;
            if (id in this.reqPool)
                req = this.reqPool[id];
            else
                req = this.createReq(id);
            this.reqPool[id] = req;
            return req;
        };
        this.directToEdit = function(id){
            directToEdit = true;
            $().GoToUrl('/requirement/' + id);
        };
        this.showRequirement = function(id){
            handler.clearLog(id);
            var req = this.getReq(id);
            req.init();
        };
        this.clearLog = function(id){
            $.ajax({
                type: "POST",
                url: '/platform/delMsg',
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({RequirementId: id}),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("修改需求日志状态失败.问题描述: " + data.errorMsg, "info");
                        return;
                    }
                    alertState("修改需求日志状态成功", "success");
                },
                error: function () {
                    alertState("修改需求日志状态失败，网络异常", "failed");
                }
            });
        };
        this.deleteRequirement = function(id, cb){
            $.ajax({
                type: "POST",
                url: "/platform/deleteRequirement",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({Id: id}),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("获取需求信息失败.问题描述: " + data.errorMsg, "info");
                        cb(false);
                        return;
                    }
                    alertState("删除需求完成", "success");
                    cb(true);
                },
                error: function () {
                    alertState("删除我的需求失败，网络异常", "failed");
                    cb(false);
                }
            });
        };
        this.createReq = function(id){
            var req = {};
            req.Id = id;
            req.newAttachFiles = [];
            req.data = {};

            req.init = function(){
                $("body,html").animate({scrollTop:0},200);
                req.newAttachFiles = [];

                $.ajax({
                    type: "POST",
                    url: $().retrieveSession().IsService ? "/platform/requirements" : "/platform/myRequirements",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({Id: req.Id}),
                    success: function (response) {
                        if (!isResponseDataAvailable(response)){
                            alertState("获取需求内容失败.问题描述: "+ response.errorMsg, "failed");
                            return;
                        }
                        cb_init(response[0]);
                    },
                    error: function () {
                        alertState("获取需求信息失败，网络异常", "failed");
                    }
                });
                function cb_init(response){
                    if (response.Status > 3){
                        Contract.StartContract(response);
                        return;
                    }
                    response.reqId = req.Id;
                    response.IsService = $().retrieveSession().IsService;
                    response.IsPublishButtonShow = !$().retrieveSession().IsService && response.CurSegment.Identity == 'draft';
                    response.IsCancelPublishShow = !$().retrieveSession().IsService && response.CurSegment.Identity == 'publish';
                    response.IsEditable = !$().retrieveSession().IsService && response.Status <= 2;
                    response.IsFollower = false;
                    response.SpecifyProducerNum = $.Object.count.call(response.specifyProducers);
                    response.producers = {};

                    if (!response.IsService){
                        $.each(response.specifyProducers, function(k, v) {
                            response.producers[v.Id] = v;
                            response.producers[v.Id].followed = false;
                        });
                        $(response.follower).each(function(i, f) {
                            response.producers[f.Follower.Domain.Id] = f.Follower.Domain;
                            response.producers[f.Follower.Domain.Id].followed = true;
                            response.producers[f.Follower.Domain.Id].applying = f.Status;
                        });
                    }

                    $(response.follower).each(function(i, f){
                        if (f.FollowerDomainId == $().retrieveSession().DomainId) {
                            response.IsFollower = true;
                            response.IsDeny = f.IsDeny;
                            response.IsApplying = f.Status;
                        }
                    });
                    $(response.RequirementAttachment).each(function(i, value){
                        req.newAttachFiles.push({
                            AttachmentId: value.Id,
                            Id: value.Object.Id,
                            Name: value.Object.Name,
                            Type: value.Object.Type,
                            Description: value.Description
                        })
                    });

                    req.data = response;
                    response.CurUserId = $().retrieveSession().UserId;
                    response.filter = $('#req_avtive_bar').attr('value'); //by zhh on 2016-10-24

                    var tem = Template.get('template/requirement/detail_nav.html');
                    var r = tem(response);
                    $('#pageContent').html(r);

                    //by zhh on 2016-10-24
                    $('.req-statusBar').unbind('click').click(function (e) {
                        $('.req-statusBar').removeClass('active');
                        $(e.currentTarget).addClass('active');
                        $().GoToUrl('/requirementPage', {c1: response.Category_1, c2: response.Category_2, filter: $(e.currentTarget).attr('value')});
                    });
                    $(".cSeg").unbind("click").click(function(){
                        var sg = $(this).children('input').val();
                        //if(response.Status<sg)return;
                        $(".cSeg").removeClass("active");
                        $(this).addClass("active");
                        switch (Math.floor(sg)){
                            case ContractSegment.draft:
                                req.toDraftSeg(response);
                                break;
                            case ContractSegment.publish:
                                req.toPublishSeg(response);
                                break;
                            case ContractSegment.establish:
                                req.toEstablishSeg(response);
                                break;
                        }
                    });

                    switch (Math.floor(response.Status)){
                        case ContractSegment.draft:
                            req.toDraftSeg(response);
                            break;
                        case ContractSegment.publish:
                            req.toPublishSeg(response);
                            break;
                        case ContractSegment.establish:
                            req.toEstablishSeg(response);
                            break;
                    }
                }
            };
            req.setCall = function(req){
                var selector = '#pageContent';
                $(selector).find('#edit-btn').unbind('click').click(function () {
                    req.edit();
                });
                $(selector).find('#publish-btn').unbind('click').click(function () {
                    req.publish(null, function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                });
                $(selector).find('#cancel-publish-btn').unbind('click').click(function () {
                    req.cancelPublish(function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                });
                $(selector).find('#followerReqBtn').unbind('click').click(function () {
                    req.apply(function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                    return false;
                });
                $(selector).find('#cancelFollowerReqBtn').unbind('click').click(function () {
                    req.cancelApply(function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                });
                $(selector).find('#addSchemeBtn').unbind('click').click(function () {
                    req.AddFollower(function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                    return false;
                });
                $(selector).find('.delSchemeBtn').unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr('value');
                    req.removeFollower(id,function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                    return false;
                });
                $(".editSchemeBtn").unbind('click').click(function (e) {
                    var followerId = $(e.currentTarget).attr('value');
                    var tem = Template.get('template/requirement/requirement_edit.html');
                    var vs = $('#requirementedit-modal');
                    if (vs.length == 0) {
                        $('#pageContent').append('<div id="requirementedit-modal" class="modal fade bs-example-modal-lg"></div>');
                    }
                    vs = $('#requirementedit-modal');
                    var follower = null;
                    $(req.data.follower).each(function(i, v){
                        if (v.Id == followerId){
                            follower = v;
                        }
                    });
                    vs.html(tem(follower));
                    vs.modal();
                    $('#cancelSchemeBtn').unbind('click').click(function(){
                        $("#requirementedit-modal").modal('hide');
                    });
                    $('#saveSchemeBtn').unbind('click').click(function(){
                        req.modifySchemeOrScript(followerId,function(bDone){
                            if(bDone)
                            {
                                $("#requirementedit-modal").modal('hide');
                                req.init();
                            }
                        });
                    });
                    $('#reapplySchemeBtn').unbind('click').click(function(){
                        $.ajax({
                            type: "POST",
                            url: "/platform/reapplyRequirementFollower",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                ReqId: req.Id,
                                FollowerId: followerId,
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alert("重新申请失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                alert("重新申请成功", "success");
                                req.init();
                            },
                            error: function () {
                                alert("重新申请失败，网络异常", "failed");
                            }
                        });

                        $("#requirementedit-modal").modal('hide');
                    });
                });
                $('.chatScheme').unbind('click').click(function (e) {
                    var followerId = $(e.currentTarget).attr('value');
                    $.ajax({
                        type: "POST",
                        url: "/platform/requirementReply",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            Id: req.Id,
                            PublisherId: $().retrieveSession().UserId,
                            FollowerId: followerId
                        }),
                        success: function (response) {
                            req.data.replys = response;
                            var tem = Template.get('template/requirement/applyScheme-comment.html');
                            var vs = $('#applyScheme-modal');
                            if (vs.length == 0) {
                                $('#pageContent').append('<div id="applyScheme-modal" class="modal fade bs-example-modal-lg"></div>');
                            }
                            vs = $('#applyScheme-modal');
                            vs.html(tem(req.data.replys));
                            vs.modal();
                            $('#applyScheme-send').click(function(){
                                req.reply($().retrieveSession().UserId,followerId);
                            });
                            $('.replyTextArea').unbind('keyup').keyup(function(e) {
                                if (e.keyCode == 13|| e.keyCode == 39) {
                                    req.reply($().retrieveSession().UserId,followerId);
                                }
                            });
                            $('#refresh-talk').unbind('click').click(function(e) {
                                req.getReply($().retrieveSession().UserId,followerId);
                            });
                        }
                    });
                });
                $(".applySchemeBtn").unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr('value');
                    req.applyScheme(true, id);
                });
                $(selector).find(".acceptReqProducer").unbind('click').click(function (e) {
                    var followerId = $(e.currentTarget).attr("value");
                    req.acceptReqProducer(followerId);
                    return false;
                });
                $(selector).find(".discussReqProducer").unbind('click').click(function (e) {
                    var followerId = $(e.currentTarget).attr("value");
                    req.acceptReqProducer(followerId);
                    return false;
                });
                $(selector).find(".denyReqProducer").unbind('click').click(function (e) {
                    if(!confirm('确认婉拒该制作商的申请？'))
                        return false;
                    var Id = $(e.currentTarget).attr("value");
                    req.denyReqProducer(Id, function(bSuccess){
                        if (bSuccess){
                            req.init();
                        }
                    });
                    return false;
                });
                $(selector).find('.producerHome').unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr("value");
                    window.open('/zone/' + id);
                });
                $('.deleteAttachment').unbind('click').click(function (e) {
                    var id = $(e.currentTarget).attr('value');
                    req.deleteAttachment(id, function(bSuccess){
                        if (bSuccess){
                            $(e.currentTarget).parent().parent()[0].outerHTML = '';
                            req.init();
                        }
                    });
                });
                $('.attachment_object').unbind('click').click(function(e){
                    var id = $(e.currentTarget).attr("value");
                    var obj = {};
                    $(req.data.RequirementAttachment).each(function(index, value){
                        if (value.Id == id)
                            obj = value.Object;
                    });
                    var path = obj.File.Path;
                    if (obj.Type == 0 || obj.Type == 2)
                        path = obj.File.VideoFile;
                    req.viewAttachment(obj.Name, path, obj.Type);
                });
                $('.download_attachment_object').unbind('click').click(function(e){
                    var id = $(e.currentTarget).attr("value");
                    var obj = {};
                    $(req.data.RequirementAttachment).each(function(index, value){
                        if (value.Id == id)
                            obj = value.Object;
                    });
                    var DownloadUrl=$.getDownloadURL(obj.File.FileCode,obj.Type);
                    $().downloadPermission(obj.Id, 'requirementAttachment', function(bSuccess){
                        if (bSuccess)
                            window.open(DownloadUrl);
                    });
                });
                //制作商添加附件
                $('#add_follower_attach').unbind('click').click(function(e){
                    Storage.filePickerDialog.open($('#fa_object_tree'), function (files) {
                        if (files.length == 0){
                            $("#fa_object_tree").html("");
                            return false;
                        }
                        $.ajax({
                            type: "POST",
                            url: '/platform/addFollowerAttachment',
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                FollowerId: req.data.follower[0].Id,
                                Files: files
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("申请该需求失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                init_follower_att(data);
                                alertState("申请该需求成功", 'success');
                            },
                            error: function () {
                                alertState("申请该需求失败，网络异常", "failed");
                            }
                        });
                        $("#fa_object_tree").html("");
                    });
                });

                if ($().retrieveSession().IsService && req.data.follower.length > 0)
                    init_follower_att(req.data.follower[0].FollowerAttachment);
                function init_follower_att(atts){
                    var tem = Template.get('template/requirement/follower_attachment.html');
                    $('#follower_attachs').html(tem({attachments: atts, IsService: true}));
                    $('.del_fa').unbind('click').click(function(e){
                        $.ajax({
                            type: "POST",
                            url: '/platform/delFollowerAttachment',
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                AttachmentId: $(e.currentTarget).attr('value')
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("申请该需求失败.问题描述: " + data.errorMsg, "info");
                                    return;
                                }
                                init_follower_att(data);
                                alertState("申请该需求成功", 'success');
                            },
                            error: function () {
                                alertState("申请该需求失败，网络异常", "failed");
                            }
                        });
                    })
                }

                if (!$().userHasRight("Req_Apply"))
                    $(selector).find("#followerReqBtn").css("display", "none");
                if (!$().userHasRight("Req_Message"))
                    $(selector).find(".reqReply").css("display", "none");
                if (!$().userHasRight("Req_Write"))
                    $(selector).find("#requirement_detail_dialog_edit_button").css("display", "none");

                if (directToEdit){
                    directToEdit = false;
                    req.edit();
                }
            }
            req.toDraftSeg = function(response){
                        var temphtml = 'template/requirement/detail_producer.html';
                        if(!$().retrieveSession().IsService)
                            temphtml = 'template/requirement/detail_customer.html';
                        var tem = Template.get(temphtml);
                        var r = tem(response);
                        var selector = '#detail-content';
                        $(selector).html(r);
                        req.setCall(req);
                    }
            req.toPublishSeg = function(response){
                        var temphtml = 'template/requirement/detail_producer.html';
                        if(!$().retrieveSession().IsService)
                            temphtml = 'template/requirement/detail_customer.html';
                        var tem = Template.get(temphtml);
                        var r = tem(response);
                        var selector = '#detail-content';
                        $(selector).html(r);
                        req.setCall(req);
                    }
            req.toEstablishSeg = function(response){
                        var temphtml = 'template/requirement/detail_producer_follower.html';
                        if(!$().retrieveSession().IsService)
                            temphtml = 'template/requirement/detail_customer_follower.html';
                        var tem = Template.get(temphtml);
                        var r = tem(response);
                        var selector = '#detail-content';
                        $(selector).html(r);
                        req.setCall(req);
                    }
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
            req.reply = function (producerId,followerId){
                var parentId = null;
                $.each(req.data.replys, function (i, reply) {
                    if ((producerId == reply.PublisherId || producerId == reply.DestUserId) && reply.ParentId == null) {
                        parentId = reply.Id;
                    }
                });
                $.ajax({
                    type: "POST",
                    url: "/platform/publishRequirementReply",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        RequirementId: req.Id,
                        Reply: $('.replyTextArea').val(),
                        ParentId: parentId,
                        DestUserId: $().retrieveSession().IsService ? req.data.PublisherId : producerId,
                        FollowerId: followerId
                    }),
                    success: function (data2) {
                        if (!isResponseDataAvailable(data2)) {
                            alertState("回复信息失败.问题描述: " + data2.errorMsg, "info");
                        }
                        req.getReply(producerId,followerId);
                        $('.replyTextArea').val('');
                    },
                    error: function () {
                        alertState("回复信息失败，网络异常", "failed");
                    }
                });
            };
            req.getReply = function(producerId, followerId){
                $.ajax({
                    type: "POST",
                    url: "/platform/requirementReply",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        Id: req.Id,
                        PublisherId: producerId,
                        FollowerId: followerId
                    }),
                    success: function (response) {
                        if (!isResponseDataAvailable(response)) {
                            alertState("获取留言板信息失败.问题描述: " + response.errorMsg, "info");
                            return;
                        }
                        req.data.replys = response;
                        var tem = Template.get('template/requirement/suggest.html');
                        var vs = $('#suggestion');
                        vs.html(tem(req.data.replys));
                        $('.chat-pannel').html(tem(req.data.replys));
                    }
                });
            };
            req.save = function(el_reqPage, cb){ // 保存需求
                if(checkInput(el_reqPage)==0) // 检查填写内容是否完整和正确
                    return;

                var specifyDomainIds = [];
                $.each(req.data.specifyProducers, function(key, value){
                    specifyDomainIds.push(key);
                });
                var category_1 = 0, category_2 = 0;
                $(req.data.category_1).each(function(i, v){
                    if (v.Name == $(el_reqPage).find('#video_category_1').val())
                        category_1 = v.Id;
                });
                $(req.data.category_2).each(function(i, v){
                    if (v.Name == $(el_reqPage).find('#video_category_2').val())
                        category_2 = v.Id;
                });
                var params = {
                    CatalogId: 0,
                    Title: $(el_reqPage).find("#requirement_title").val(),
                    Detail: $(el_reqPage).find("#requirement_detail").val(),
                    Amount: $(el_reqPage).find("#requirement_amount").val(),
                    Deadline: $(el_reqPage).find(".deadline").val(),
                    category_1: category_1,
                    category_2: category_2,
                    long:$(el_reqPage).find("#requirement_long").val(),
                    format:$(el_reqPage).find("#requirement_format").val(),
                    voice:$(el_reqPage).find("#voice").val(),
                    subtitle:$(el_reqPage).find("#subtitle").val(),
                    gbm:$(el_reqPage).find("#gbm").val(),
                    place:$(el_reqPage).find("#place").val(),
                    refer:$(el_reqPage).find("#refer").val(),
                    symbol:$(el_reqPage).find("#symbol").val(),
                    Status: 0,
                    specifyProducers: specifyDomainIds,
                    Attachments: req.newAttachFiles
                };
                if (req.Id != null)
                    params["Id"] = req.Id;
                $.ajax({
                    type: "POST",
                    url: "/platform/publishRequirement",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify(params),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("需求草稿保存失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("需求草稿保存成功", "success");
                        cb(true);
                    },
                    error: function () {
                        alertState("需求草稿保存失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.cancelPublish = function(cb){
                $.ajax({
                    type: "POST",
                    url: "/platform/publishRequirement",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        bCancel: true,
                        Id: req.Id
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("取消提交需求失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("取消提交需求成功", "success");
                        cb(true);
                    },
                    error: function () {
                        alertState("取消提交需求失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.publish = function(el_reqPage, cb){ // 提交需求
                var params;
                var specifyDomainIds = [];

                if (el_reqPage){ //处于编辑状态
                    if(checkInput(el_reqPage)==0)
                        return;
                    $.each(req.data.specifyProducers, function(key, value){
                        specifyDomainIds.push(key);
                    });
                    var category_1 = 0, category_2 = 0;
                    $(req.data.category_1).each(function(i, v){
                        if (v.Name == $(el_reqPage).find('#video_category_1').val())
                            category_1 = v.Id;
                    });
                    $(req.data.category_2).each(function(i, v){
                        if (v.Name == $(el_reqPage).find('#video_category_2').val())
                            category_2 = v.Id;
                    });
                    params = {
                        CatalogId: 0,
                        Title: $(el_reqPage).find("#requirement_title").val(),
                        Detail: $(el_reqPage).find("#requirement_detail").val(),
                        Amount: $(el_reqPage).find("#requirement_amount").val(),
                        Deadline: $(el_reqPage).find(".deadline").val(),
                        category_1: category_1,
                        category_2: category_2,
                        long:$(el_reqPage).find("#requirement_long").val(),
                        format:$(el_reqPage).find("#requirement_format").val(),
                        voice:$(el_reqPage).find("#voice").val(),
                        subtitle:$(el_reqPage).find("#subtitle").val(),
                        gbm:$(el_reqPage).find("#gbm").val(),
                        place:$(el_reqPage).find("#place").val(),
                        refer:$(el_reqPage).find("#refer").val(),
                        symbol:$(el_reqPage).find("#symbol").val(),
                        Status: 1,
                        Attachments: req.newAttachFiles,
                        specifyProducers: specifyDomainIds
                    };

                    if (req.Id)
                        params["Id"] = req.Id;
                }
                else{ //列表状态，不编辑
                    params = {
                        Status: 1,
                        Id: req.Id
                    };
                }

                $.ajax({
                    type: "POST",
                    url: "/platform/publishRequirement",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify(params),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("提交需求失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("提交需求成功", "success");
                        cb(true);
                    },
                    error: function () {
                        alertState("提交需求失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.acceptReqProducer = function(id){
                req.createContract(id, function(bSuccess, data){
                    if (bSuccess)
                        req.init();
                });
            };
            req.denyReqProducer = function(id, cb){
                $.ajax({
                    type: "POST",
                    url: "/platform/removeRequirementFollower",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ReqId: req.Id,
                        Id: id,
                        Deny: true
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("取消制作商申请失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("取消制作商申请成功", "success");
                        cb(true);
                    },
                    error: function () {
                        alertState("取消制作商申请失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.modifySchemeOrScript = function(id,cb){
                $.ajax({
                    type: "POST",
                    url: '/platform/saveReqScheme',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ReqId: req.Id,
                        Id: id,
                        Long: $('#requirement_long').val(),
                        Format: $('#requirement_format').val(),
                        Script: $('#contract_script').val(),
                        DepositPercent: $('#requirement_depositPercent').val(),
                        BasePrice: $('#basePrice').val(),
                        SchemePrice: $('#schemePrice').val(),
                        ShotPrice: $('#shotPrice').val(),
                        ActorPrice: $('#actorPrice').val(),
                        MusicPrice: $('#musicPrice').val(),
                        AEPrice: $('#aePrice').val()
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("修改需求方案失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                        }
                        else
                            cb(true);
                    },
                    error: function () {
                        alertState("修改需求方案失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.applyScheme = function(bApply, followerId){
                $.ajax({
                    type: "POST",
                    url: '/platform/applyReqScheme',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ReqId: req.Id,
                        Id: followerId,
                        Status: bApply
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("修改需求方案失败.问题描述: " + data.errorMsg, "info");
                        }
                        req.init();
                    },
                    error: function () {
                        alertState("修改需求方案失败，网络异常", "failed");
                    }
                });
            };
            req.createContract = function(followerId, cb){
                var follower = null;
                $.ajax({
                    type: "POST",
                    url: "/platform/getRequirementFollower",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({ReqId: req.Id}),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("取申请者信息失败: " + data.errorMsg, "info");
                            return;
                        }
                        alertState("取申请者信息成功", "success");
                        req.data.follower = data;
                        initConfirmContract();
                    },
                    error: function () {
                        alertState("合同创建失败", "failed");
                    }
                });

                function initConfirmContract(){
                    $(req.data.follower).each(function(i, v){
                        if (v.Id == followerId)
                            follower = v;
                    });

                    var tem = Template.get('template/requirement/confirmContract.html');
                    var vs = $('#viewSchemeOrScript');
                    if (vs.length == 0) {
                        $('#pageContent').append('<div id="viewSchemeOrScript" class="modal fade bs-example-modal-lg"></div>');
                    }
                    vs = $('#viewSchemeOrScript');
                    vs.html(tem({follower:follower, requirement: req.data}));
                    tem = Template.get('template/requirement/follower_attachment.html');
                    $('.fattachment').html(tem({attachments:follower.FollowerAttachment, IsService: $().retrieveSession().IsService}));
                    $('.down_fa').unbind('click').click(function(e){
                        var id = $(e.currentTarget).attr("value");
                        var obj = {};
                        $(follower.FollowerAttachment).each(function(index, value){
                            if (value.Id == id)
                                obj = value.Object;
                        });
                        var DownloadUrl=$.getDownloadURL(obj.File.FileCode,obj.Type);
                        window.open(DownloadUrl);
                    });
                    $('#refresh-talk').unbind('click').click(function(e) {
                        req.getReply(follower.FollowerProducerId,follower.Id);
                    });
                    req.getReply(follower.FollowerProducerId,follower.Id);
                    $('#sendMsg').unbind('click').click(function(e) {
                        var id = $(e.currentTarget).attr("value");
                        req.reply(id,follower.Id);
                    });
                    $('.replyTextArea').unbind('keyup').keyup(function(e) {
                        if (e.keyCode == 13|| e.keyCode == 39) {
                            var id = $(e.currentTarget).parent().parent().find('#sendMsg').attr("value");
                            req.reply(id,follower.Id);
                        }
                    });
                    $("#confirm").unbind('click').click(function (e) {
                        var followerId = $(e.currentTarget).attr('value');
                        $.ajax({
                            type: "POST",
                            url: "/platform/applyContract",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                RequirementId: req.Id,
                                ServiceUserId: follower.FollowerProducerId,
                                FollowerId: followerId
                            }),
                            success: function (data) {

                                if (!isResponseDataAvailable(data)) {
                                    alertState("合同创建失败: " + data.errorMsg, "info");
                                    cb(false, data);
                                    return;
                                }
                                alertState("合同创建成功", "success");
                                cb(true, data);
                            },
                            error: function () {
                                alertState("合同创建失败", "failed");
                                cb(false, data);
                            }
                        });
                        vs.modal('hide');
                    });
                    $("#cancel-confirm").unbind('click').click(function (e) {
                        var followerId = $(e.currentTarget).attr('value');
                        req.applyScheme(false, followerId);
                        vs.modal('hide');
                    });
                    $("#quit-confirm").unbind('click').click(function (e) {
                        vs.modal('hide');
                    });
                    vs.modal();
                }
            };
            req.viewSchemeOrScript = function(follower){
                var tem = Template.get('template/requirement/requirement_viewScheme.html');
                var vs = $('#viewSchemeOrScript');
                if (vs.length == 0) {
                    $('#pageContent').append('<div id="viewSchemeOrScript" class="modal fade bs-example-modal-lg"></div>');
                }
                vs = $('#viewSchemeOrScript');
                vs.html(tem({follower:follower}));
                $("#viewSchemeQuit").unbind('click').click(function (e) {
                    vs.modal('hide');
                });
                vs.modal();
            };
            req.apply = function(cb){ //申请需求
//                在main.js中
//                if ($().isExpireTime()) {
//                    alert('您的会费到期了，无法正常接单，请及时充值');
//                    $().GoToUrl('/session#/UpdataPage');
//                    return;
//                }
//                else if ($().retrieveSession().DomainPrepare){
//                    alert('暂时无法接单，请完善信息，并联系商影联盟工作人员，开启接单功能');
//                    return;
//                }
                $.ajax({
                    type: "POST",
                    url: '/platform/askRequirement',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ReqId: req.Id,
                        Command: "ask"
                    }),
                    success: function (data) {
                        console.log('yes');
                        if (!isResponseDataAvailable(data)) {
                            alertState("申请该需求失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("申请该需求成功", 'success');
                        cb(true);
                    },
                    error: function () {
                                        console.log('fuck');

                        alertState("申请该需求失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.cancelApply = function(cb){
                $.ajax({
                    type: "POST",
                    url: '/platform/askRequirement',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ReqId: req.Id,
                        Command: "cancel"
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("取消失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("取消申请成功", 'success');
                        cb(true);
                    },
                    error: function () {
                        alertState("取消申请失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.AddFollower = function(cb){ //增加方案
//                if ($().isExpireTime()) {
//                    alert('您的会费到期了，无法正常接单，请及时充值');
//                    $().GoToUrl('/session#/UpdataPage');
//                    return;
//                }
//                else if ($().retrieveSession().DomainPrepare){
//                    alert('暂时无法接单，请完善信息，并联系商影联盟工作人员，开启接单功能');
//                    return;
//                }
                $.ajax({
                    type: "POST",
                    url: '/platform/addRequirementFollower',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ReqId: req.Id
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("申请该需求失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("申请该需求成功", 'success');
                        cb(true);
                    },
                    error: function () {
                        alertState("申请该需求失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.removeFollower = function(id,cb){
                $.ajax({
                    type: "POST",
                    url: '/platform/removeRequirementFollower',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        ReqId: req.Id,
                        Id: id
                    }),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("取消申请该需求失败.问题描述: " + data.errorMsg, "info");
                            cb(false);
                            return;
                        }
                        alertState("取消申请该需求成功", 'success');
                        cb(true);
                    },
                    error: function () {
                        alertState("取消申请该需求失败，网络异常", "failed");
                        cb(false);
                    }
                });
            };
            req.deleteAttachment = function(id, cb){ // 删除需求附件
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
            req.toEditPage = function () { // 打开需求编辑页面
                var publishTab;
                var tem = Template.get("template/requirement/edit.html");
                var obj = req.data;
                publishTab = $("#requireDetail_" + req.Id);
                publishTab.html(tem(req.data));
                refreshProducerList();
                publishTab.find('#deadline').find('input').datepicker();
                publishTab.find("#requirement_add_dialog_title").text("编辑需求");
                publishTab.find("#requirement_title").val(obj.Title);
                publishTab.find("#requirement_detail").val(obj.Detail);
                publishTab.find("#requirement_amount").val(obj.Amount);
                publishTab.find(".deadline").val(obj.Deadline);
                publishTab.find("#requirement_long").val(obj.Long);
                publishTab.find("#requirement_format").val(obj.Format);
                publishTab.find("#voice").val(obj.Voice);
                publishTab.find("#subtitle").val(obj.Subtitle);
                publishTab.find("#gbm").val(obj.Gbm);
                publishTab.find("#place").val(obj.Place);
                publishTab.find("#refer").val(obj.Refer);
                publishTab.find("#symbol").val(obj.Symbol);

                showTip(publishTab);

                $.each(obj.RequirementAttachment, function ($index, $value) {
                    var tem = Template.get("template/requirement/requirement_attachment.html");
                    $('#re_attachments').append(tem({Attachments: [{AttachmentId: $value.Id, Id: $value.Object.Id, Name: $value.Object.Name, Type: $value.Object.Type, CreateTime: $value.Object.CreateTime, Description: $value.Description}]}));
                });
                initAttachment();
                req.initCategory(0, true);
                $('#requirement_file_getfile').unbind('click').click(function () {
                    Storage.filePickerDialog.open($('#re_objectTree'), function (files) {
                        var bRepeat = false;
                        var repeatFile = "";
                        try {
                            $(req.newAttachFiles).each(function (i, attachment) {
                                $(files).each(function (index, value) {
                                    if (attachment.Name == value.Name) {
                                        bRepeat = true;
                                        repeatFile = value.Name;
                                    }
                                })
                            });
                        }
                        catch(e){}
                        if (bRepeat) {
                            confirm("文件：" + repeatFile + "无法重复上传");
                            return;
                        }
                        $.each(files,function(n, value){
                            var tem = Template.get("template/requirement/requirement_attachment.html");
                            $('#re_attachments').append(tem({Attachments: [value]}));
                            req.newAttachFiles = $.merge(req.newAttachFiles, [value]);
                        });
                        initAttachment();
                        $("#re_objectTree").html("");
                        $("body,html").animate({scrollTop:$(".attachmentTable").offset().top}, 200);
                    });
                });
                $("#selectProducer").unbind('click').click(function(){
                    var rc = $(".requirement_content");
                    rc.css("display", "none");
                    Search.init(req.data.specifyProducers);
                    Search.show("", 'producer', $(".requirement_search_producer"), req.Id, function(bConfirm, data){
                        if (bConfirm){
                            $(data).each(function(index, value){
                                if (!value.bSelect)
                                    delete req.data.specifyProducers[value.Id];
                                else
                                    req.data.specifyProducers[value.Id] = value;
                            });
                            refreshProducerList();
                        }
                        $(".requirement_search_producer").html("");
                        rc.css("display", "block");
                        $("body,html").animate({scrollTop:0},200);
                    });
                });
                function initAttachment(){
                    $('.del_ad').unbind('click').click(function(e){
                        var attachId = $(e.currentTarget).attr('value');
                        var objId = $(e.currentTarget).attr('name');
                        if (!attachId)
                            refresh();
                        else{
                            req.deleteAttachment(attachId, function(bSuccess){
                                if (bSuccess)
                                    refresh();
                            });
                        }
                        function refresh(){
                            var delIndex = -1;
                            $(req.newAttachFiles).each(function(i, v){
                                if (v.Id == objId)
                                    delIndex = i;
                            });
                            req.newAttachFiles.splice(delIndex, 1);
                            var tem = Template.get("template/requirement/requirement_attachment.html");
                            $('#re_attachments').html(tem({Attachments: req.newAttachFiles}));
                            initAttachment();
                        }
                    });
                    $('.save_ad').unbind('click').click(function(e){
                        var id = $(e.currentTarget).attr("value");
                        var input = $("#input_ad_description_" + id);
                        var text = $("#ad_description_" + id);
                        var btn = $(e.currentTarget).find('span');

                        if (input.css("display") == 'none') {
                            input.val(text.text());
                            input.show();
                            btn.removeClass('glyphicon-edit');
                            btn.addClass('glyphicon-floppy-disk');
                            text.hide();
                        }
                        else{
                            input.hide();
                            text.text(input.val());
                            text.show();
                            btn.addClass('glyphicon-edit');
                            btn.removeClass('glyphicon-floppy-disk');
                            $(req.newAttachFiles).each(function(index, value){
                                if (value.Id == id)
                                    value.Description = input.val();
                            })
                        }
                    });
                }
                function refreshProducerList(){ //显示指定的供应商列表
                    var tem = Template.get("template/requirement/requirement_specifyProducer.html");
                    $("#specifyProducers").html(tem(req.data.specifyProducers));
                    $(".deleteProducer").unbind('click').click(function(e){
                        var id = $(e.currentTarget).attr('value');
                        delete req.data.specifyProducers[id];
                        refreshProducerList();
                    });
                }
            };
            req.initCategory = function(parentId, isLevelOne){
                var param = {};
                if (!isLevelOne)
                    $.extend(param, {ParentId: parentId});
                $.ajax({
                    type: "POST",
                    url: "/platform/videoCategory",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify(param),
                    success: function (response) {
                        if (!isResponseDataAvailable(response)) {
                            alertState("获取需求分类失败.问题描述: " + response.errorMsg, "info");
                            return;
                        }
                        var tem = Template.get("template/requirement/requirement_category.html");
                        if (isLevelOne) {
                            var el = $("#video_category_1");
                            el.html(tem(response));
                            req.data['category_1'] = response;
                            var cIndex = 0;
                            $(response).each(function(i,v){
                                if (v.Id == req.data.Category_1) {
                                    el.val(v.Name);
                                    cIndex = i;
                                }
                            });
                            req.initCategory(response[cIndex].Id, false);
                            el.change(function(){
                                var n = el.val();
                                $(response).each(function(i,v){
                                    if (v.Name == n)
                                        req.initCategory(v.Id, false);
                                });
                            });
                        }
                        else {
                            req.data['category_2'] = response;
                            el = $("#video_category_2");
                            el.html(tem(response));
                            $(response).each(function(i,v){
                                if (v.Id == req.data.Category_2)
                                    el.val(v.Name);
                            });
                        }
                    }
                });
            };
            req.parseDetail = function(detail, data){
                var groups = detail.split("@");
                for (var i = 0; i < groups.length; i++){
                    var temp = groups[i].split("$");
                    data[temp[0]] = temp[1];
                }
            };
            req.edit = function () {
                req.toEditPage();

                var temp ="#requireDetail_" + req.Id;
                $(temp).find('#requirement_add_commit').unbind("click").click(function () {
                    req.save(temp, function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                });
                $(temp).find('#requirement_add_publish').unbind("click").click(function () {
                    req.publish(temp, function(bSuccess){
                        if (bSuccess)
                            req.init();
                    });
                });
                $(temp).find('#requirement_add_cancel').unbind("click").click(function(){
                    req.init();
                });
            };

            return req;
        };
    }
function refreshHtml(){
    window.location.href=window.location.href
}
$('#ask-requirement-btn').unbind('click').click(function (e) {
                    if(!confirm('确认申请该需求吗？'))
                        return false;
    REQ.apply(function(bSuccess){
        if (bSuccess)
            REQ.init();
    });
    refreshHtml();
    return false;
});
$("#denyReqProducer").unbind('click').click(function (e) {
                    if(!confirm('确认婉拒该制作商的申请？'))
                        return false;
                    REQ.denyReqProducer(FOLLOWE_ID, function(bSuccess){
                        if (bSuccess){
                            REQ.init();
                        }
                    });
                    refreshHtml();
                    return false;
                });
$("#acceptReqProducer").unbind('click').click(function (e) {
                 if(!confirm('确认接受该制作商的申请并且支付预付款？'))
                    return false;
                        $.ajax({
                            type: "POST",
                            url: "/platform/applyContract",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                RequirementId: REQ_ID,
                                ServiceUserId: FOLLOWEProducerId,
                                FollowerId: FOLLOWE_ID
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("合同创建失败: " + data.errorMsg, "info");
                                    return;
                                }
                                alertState("合同创建成功", "success");
                            },
                            error: function () {
                                alertState("合同创建失败", "failed");
                            }
                        });


                 refreshHtml();

                 });
$("#comfirm-beforepay-btn").unbind('click').click(function (e) {
      if(!confirm('确认通过申请并支付预付款？'))
                    return false;
               $.ajax({
                    type: "POST",
                    url: "/mobile/pay_notify",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        Id: REQ_ID,

                    }),
                    success: function (data) {
                        if(data=='ok'){
                         alert('已成功通知！请等待平台提供审片')
                            refreshHtml();
                        }
                    },
                    error: function () {
                         alert('已成功通知！请等待平台提供审片')
                            refreshHtml();
                    }
                });
     });
$('#reject-video-btn').unbind('click').click(function(){
   if(!confirm('确认驳回该视频？'))
                    return false;
                $.ajax({
                    type: "POST",
                    url: "/platform/ContractAttachmentIsReject",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({AttachmentId: ATTACHMENT_ID}),
                    success: function (data) {
                        alert("成功驳回，请等待服务商处理");
                        refreshHtml();
                    },
                    error: function () {
                        alert("失败，网络异常");
                        refreshHtml();
                    }
                });
            });
$('#pass-video-btn').unbind('click').click(function(){
   if(!confirm('确认通过视频审核并且支付尾款？'))
          return false;
   api = "/platform/confirmContractReview";
                    $.ajax({
                        type: "POST",
                        url: api,
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            reqId:REQ_ID,
                            conId:CONTRACT_ID,
                            IsReject: false
                        }),
                        success: function (data) {

                             alert("成功通过！");
                            refreshHtml();

                        },
                        error: function () {
                            alert("失败，网络异常");
                           refreshHtml();

                                            }
                    });
        });
$("#comfirm-pay-btn").unbind('click').click(function (e) {
      if(!confirm('确认支付尾款？'))
                    return false;
               $.ajax({
                    type: "POST",
                    url: "/mobile/pay_notify",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        Id: REQ_ID,
                    }),
                    success: function (data) {
                        if(data=='ok'){
                         alert('已成功通知！请下载视频')
                            refreshHtml();
                        }
                    },
                    error: function () {
                         alert('已成功通知！请下载视频')
                        refreshHtml();
                    }
                });
     });

$("#ContractOver-btn").unbind('click').click(function (e) {
     if (!confirm("确认成片后，制作费用将会付给制作商，请确认已经下载成片"))
            return;
                        $.ajax({
                            type: "POST",
                            url: "/platform/ContractOver",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                conId: CONTRACT_ID,
                                reqId:REQ_ID
                            }),
                            success: function (data) {
                                refreshHtml();
                            },
                            error: function () {
                                alert("失败，网络异常");
                            }
                        });
     });



var REQ_ID = $('#request_id').attr('value');
var FOLLOWE_ID = $('#follower_id').attr('value');
var FOLLOWEProducerId=$('#follower_producer_id').attr('value')
var ATTACHMENT_ID=$('#checkAttachment_id').attr('value')
var CONTRACT_ID = $('#contract_id').attr('value');


var URL=window.location.href;
var HANDLER = new RequirementHandler();
var REQ = HANDLER.createReq(REQ_ID)

console.log(REQ_ID);
console.log(URL);
console.log(FOLLOWE_ID);
console.log(FOLLOWEProducerId);
console.log(ATTACHMENT_ID);
console.log(CONTRACT_ID);


