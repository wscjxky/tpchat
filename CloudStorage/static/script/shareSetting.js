define(['jquery', 'template'], function ($, Template) {
        var cache_ = {};
        //初始化
        function init(data) {
            cache_.objectId = data.objectId;
            cache_.cb = data.cb_shareObjectDone;
            fetchShare();
        }
        function fetchShare(){
            $.ajax({
                type: "POST",
                url: "/cloud/getStorageShareObject",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({ObjectId: cache_.objectId}),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("取消共享对象操作失败.问题描述: " + data.errorMsg, "failed");
                        return;
                    }
                    //显示共享设置
                    cache_.shareDomains = data;
                    var tem = Template.get('template/share/share_domain_add_dialog.html');
                    var test = tem(data);
                    var dialog = $('#share_domain_add_dialog');
                    if (dialog.length == 0) {
                        $('#pageContent').append('<div id="share_domain_add_dialog" class="modal fade bs-example-modal-md"></div>');
                        dialog = $('#share_domain_add_dialog');
                    }
                    dialog.html($.trim(test));
                    dialog.modal();
                    //搜索用户键盘回车事件
                    $("#share_domain_add_search_input").bind('keyup', function (event) {
                        if (event.keyCode == 13)
                            addShare_searchDomain($("#share_domain_add_search_input").val());
                    });
                    //搜索用户按钮事件
                    $("#share_domain_add_search_btn").unbind("click").click(function () {
                        addShare_searchDomain($("#share_domain_add_search_input").val());
                    });
                    //确认添加按钮事件
                    $("#share_domain_add_commit").unbind("click").click(function () {
                        addShareDomain_add();
                    });
                    initShareDomain(data);
                    dialog.modal();
                    //添加共享域
                    function addShareDomain_add() {
                        //查找是否有选中域
                        var domains = [];
                        var checks = $('.domain_check').find('input');
                        $(checks).each(function(k, v){
                            if ($(v).is(':checked'))
                                domains.push($(v).attr('value'));
                        });
                        var bDownload = $('#share_domain_add_right_download').is(':checked');
                        var bWrite = $('#share_domain_add_right_write').is(':checked');
                        $.ajax({
                            type: "POST",
                            url: "/cloud/storageShareObject",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                ObjectId: cache_.objectId,
                                DomainId: domains,
                                DownloadPermission: bDownload,
                                WritePermission: bWrite
                            }),
                            success: function (data) {
                                if (!isResponseDataAvailable(data))
                                    alertState("添加共享对象操作失败.问题描述: " + data.errorMsg, "failed");
                                cache_.cb(true);
                            },
                            error: function () {
                                alertState("添加共享对象操作失败，网络异常", "failed");
                            }
                        });
                        dialog.modal('hide');
                        dialog.empty();
                    }
                    function cancelShare(domainId) {
                        $.ajax({
                            type: "POST",
                            url: "/cloud/delStorageShareObjectDomain",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({ObjectId: cache_.objectId, DomainId: domainId}),
                            success: function (data) {
                                if (!isResponseDataAvailable(data)) {
                                    alertState("取消共享对象操作失败.问题描述: " + data.errorMsg, "failed");
                                    return;
                                }
                                initShareDomain(data);
                            },
                            error: function () {
                                alertState("取消共享对象操作失败，网络异常", "failed");
                            }
                        });
                    }
                    //搜索用户
                    function addShare_searchDomain(domainName) {
                        $.ajax({
                            type: "POST",
                            url: "/share/searchDomain",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({KeyWord: domainName}),
                            success: function (data) {
                                var tem = Template.get('template/share/share_domain_select.html');
                                var test = tem(data);
                                $("#share_domain_add_search_after").html($.trim(test));
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
                    function initShareDomain(data){
                        cache_.shareDomains = data;
                        var tem = Template.get('template/share/share_domains.html');
                        var test = tem(data);
                        $('#selectedDomains').html($.trim(test));
                        //确认添加按钮事件
                        $(".removeShareDomain").unbind("click").click(function (e) {
                            cancelShare($(e.currentTarget).attr('value'));
                        });
                    }
                },
                error: function () {
                    alertState("取消共享对象操作失败，网络异常", "failed");
                }
            });
        }
        var shareSetting_interface = {};
        shareSetting_interface.initSetting = init;
        return shareSetting_interface;
    }
);