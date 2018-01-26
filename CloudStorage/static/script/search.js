define(['jquery', 'template', 'director'], function ($, Template) {
    function searchPage(){
        var selector = $("#functionalArea");
         if (selector.length == 0)
            selector = $('#pageContent');
        show($().GetParamsFromUrl()['search'], handler.eType["all"], selector, function(){
        });
    }
    // type：综合搜索，制作商选择
    // attachElement：搜索页依附的html元素
    // cb：业务逻辑的回调，回传查询后的结果
    function show(keyword, type, attachElement, reqId, cb){
        handler.show(keyword, type, attachElement, reqId, cb);
    }
    function init(specifyProducers){
        handler.init(specifyProducers);
    }
    function searchHandler(){
        var sh = {};
        sh.eType = {all: 'all', producer: 'producer'};
        sh.curType = sh.eType["all"];
        sh.searchPhase = "";
        sh.reqId = 0;
        sh.attachElement = $('#functionalArea');
        sh.specifyProducers = null;
        sh.init = function(specifyProducers){
            sh.specifyProducers = specifyProducers;
        };
        // data为search后结果
        sh.businessCB = function(bConfirm, data){};
        sh.show = function(keyword, type, attachElement, reqId, cb){
            sh.attachElement = attachElement;
            sh.businessCB = cb;
            sh.result = {};
            sh.curType = type;
            sh.reqId = reqId;
            sh.search(keyword);
        };
        sh.confirmSelect = function(){
            var cbData = [];
            $.each(sh.result, function(key, domain){
//                if (domain.bSelect)
                    cbData.push(domain);
            });
            sh.businessCB(true, cbData);
        };
        sh.cancelSelect = function(){
            sh.businessCB(false, sh.result);
        };
        sh.search = function(keyword){
            sh.searchPhase = keyword;
            $.ajax({
                type: "POST",
                url: '/cloud/search',
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({SearchKeyword: keyword, SearchType: sh.curType, reqId: sh.reqId}),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("搜索失败.问题描述:" + data.errorMsg, "failed");
                        return;
                    }
                    if (sh.curType == sh.eType['all']){
                        var tem = Template.get('template/search/search_all.html');
                        var test = tem(data);
                        var selector = sh.attachElement;
                        selector.html($.trim(test));
                    }
                    else{
                        tem = Template.get('template/search/search_producer.html');
                        test = tem(data);
                        selector = sh.attachElement;
                        selector.html($.trim(test));
                        $(data.domain).each(function(index, domain){
                            sh.result[domain.Id] = domain;
                            sh.result[domain.Id].bSelect = false;
                            if (sh.specifyProducers.hasOwnProperty(domain.Id)) {
                                sh.result[domain.Id].bSelect = true;
                                $('.producer_checkbox_' + domain.Id).prop('checked', true);
                            }
                        });
                    }
                    var searchInput = $('#searchaw-input');
                    $("#searchaw_btn").unbind('click').click(function () {
                        sh.search(searchInput.val());
                    });
                    searchInput.bind('keyup', function (event) {
                        if (event.keyCode == 13){
                            sh.search(searchInput.val());
                        }
                    });
                    $(".producer_checkbox").unbind('click').click(function(e){
                        var id = $(e.currentTarget).val();
                        sh.result[id].bSelect = false;
                        if ($(e.currentTarget).prop('checked'))
                            sh.result[id].bSelect = true;
                    });
                    $("#confirm_select").unbind('click').click(function(){
                        sh.confirmSelect();
                    });
                    $("#cancel_select").unbind('click').click(function(){
                        sh.cancelSelect();
                    });
                    $("#quitSearch").unbind('click').click(function(){
                        sh.cancelSelect();
                    });
                    searchInput.val(sh.searchPhase);
                },
                error: function () {
                    alertState("搜索失败失败,网络异常", "failed");
                }
            });
        };
        return sh;
    }
    var handler = searchHandler();

    var search_interface = {};
    search_interface.show = show;
    search_interface.init = init;
    search_interface.pageRouter = {
        '/searchPage/([^/]*)': searchPage
    };
    return search_interface;
});