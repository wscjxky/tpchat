var server = '/';

function htmlEncode(string){
    var str = string;
    if (str){
        str = str.replace(/\r\n/g,'</br>');
        str = str.replace(/\n/g,'</br>');
        str = str.replace(/\r/g,'</br>');
        str = str.replace(/ /g,"&nbsp;");
    }
    return str;
}

Number.prototype.formatTime=function(){
    // 计算
    var h=0,i=0,s=parseInt(this);
    if(s>60){
        i=parseInt(s/60);
        s=parseInt(s%60);
        if(i > 60) {
            h=parseInt(i/60);
            i = parseInt(i%60);
        }
    }
    // 补零
    var zero=function(v){
        return (v>>0)<10?"0"+v:v;
    };
    return [zero(h),zero(i),zero(s)].join(":");
};

function TimeToSec(time){
    var group = time.split(':');
    var hour = parseInt(group[0]);
    var min = parseInt(group[1]);
    var sec = parseInt(group[2]);
    return hour * 60 * 60 + min * 60 + sec;
}

var operLogs = [];
function alertState(msg, state) {
    var mydate = new Date();
    var t = mydate.toLocaleString();
    operLogs.push({msg: msg, level: state, time: t});
}

function msgAlert(msg){
    $('#top_msgalert').text(msg);
    $('#top_msgalert').slideDown();
    $('#top_msgalert').unbind('click').click(function(){
        window.location.href = '/session#/msgCenter';
        $('#top_msgalert').slideUp();
    })
}

//查看http调用返回的值是否为有效值
function isResponseDataAvailable(data) {
    if (data == null)
        return false;

    if (data.errorCode != null && data.errorCode == 3) {
        window.location.href = '/login#/loginPage';
        alert("您的账号已在其它地方登录，请尝试重新登录！", "info");
    }
    return (data.errorMsg == undefined);
}

function newGuid() {
    var id = "";
    for (var i = 1; i <= 32; i++) {
        var n = Math.floor(Math.random() * 16.0).toString(16);
        id += n;
        if ((i == 8) || (i == 12) || (i == 16) || (i == 20))
            id += "-";
    }
    return id;
}

require.config(
    {
        baseUrl: "static/script",//{{ url_for('.static', filename='script') }}
        paths: {
            "jquery": "//cdn.bootcss.com/jquery/2.0.0/jquery.min", //"jquery-1.11.1/jquery-1.11.1.min"
            "jqueryCookie": "//cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie",
            "jquery-ui": "//cdn.bootcss.com/jqueryui/1.11.2/jquery-ui.min", //"jquery-ui-1.11.2/jquery-ui.min"
            "bootstrap": "//cdn.bootcss.com/bootstrap/3.3.4/js/bootstrap.min", //"bootstrap-3.2.0/dist/js/bootstrap"
            "jstree": "//cdn.bootcss.com/jstree/3.1.0/jstree.min",
            "highchart": "//cdn.bootcss.com/highcharts/4.0.4/highcharts", //"Highcharts-4.0.1/js/highcharts"
            "jcrop": "//cdn.bootcss.com/jquery-jcrop/0.9.12/js/jquery.Jcrop.min",
            "zclip": "//cdn.bootcss.com/zclip/1.1.2/jquery.zclip.min",

            "sortElement": "sortElement/jquery.sortElements",
            "JcropWarp": "JcropWarp/JcropWarp",
            "context-menu": "context-menu/bootstrap-contextmenu",
            'md5': "md5/jQuery.md5",
            "director": "director/director.min",

            "file-input": "fileInput/file-input",
            "uploadify": "uploadify/jquery.uploadify.min",
            "webuploader" : "swfupload/Scripts/webuploader.min",
            "newuploader" : "swfupload/Scripts/newuploader",
            //"swfupload" : "swfupload/Scripts/swfupload",
            //"webuploader": "http://cdn.staticfile.org/webuploader/0.1.1/webuploader",

            "ckplayer":"player/ckplayer/ckplayer.min", //"player/ckplayer/ckplayer"
            "offlights":"player/js/offlights",

            "template": "template/template",
            'storage': "storage",
            "UserInfo": "UserInfo",
            'login': "login",
            'updata': "updata",
            'shareSetting': "shareSetting",
            'contract': "contract",
            "requirement": "requirement",
            "msgCenter": "msgCenter",
            "search": "search",
            "management":"management"
        },
        shim: {
            'webuploader':{
            deps : ['jquery']
            },
            'newuploader' : {
            deps : ['jquery', 'storage','webuploader']
            },
            'template': {
                exports: 'template'
            },
            'director': {
                exports: 'Router'
            },
            'jquery-ui': {
                deps: ['jquery']
            },
            'bootstrap': {
                deps: ['jquery']
            },
            'file-input': {
                deps: ['bootstrap', 'jquery']
            },
            'context-menu': {
                deps: ['bootstrap', 'jquery']
            },
            'uploadify': {
                deps: ['jquery']
            },
            'login': {
                deps: ['jquery', 'template', 'bootstrap', 'jquery-ui']
            },
            'updata': {
                deps: ['jquery', 'template']
            },
            'shareSetting': {
                deps: ['jquery', 'template']
            },
            'md5': {
                deps: ['jquery']
            },
            'requirement': {
                deps: ['jquery', 'template', 'storage']
            },
            'contract': {
                deps: ['jquery', 'template']
            },
            'msgCenter': {
                deps: ['jquery', 'template']
            },
            'highchart': {
                deps: ['jquery']
            },
            "jstree": {
                deps: ['jquery']
            },
            "sortElement": {
                deps: ['jquery']
            },
            "jcrop": {
                deps: ['jquery']
            },
            "zclip": {
                deps: ['jquery']
            }
        }, waitSeconds: 200
    });

require(['jquery','template','director','storage','login','UserInfo','updata','requirement','contract', 'msgCenter','search','management', 'webuploader', 'bootstrap','jquery-ui','uploadify','jstree','newuploader','ckplayer','offlights', 'jqueryCookie'],
    function ($,template,Router,Storage,Login,UserInfo,Updata,Requirement,Contract,MsgCenter,Search,Management,Webuploader) {
        var b_name = navigator.appName;
        var b_version = navigator.appVersion;
        var version = b_version.split(";");
        var trim_version = version.length > 1 ? version[1].replace(/[ ]/g, "") : null;

        if (trim_version == "MSIE9.0" || trim_version == "MSIE8.0" || trim_version == "MSIE7.0" || trim_version == "MSIE6.0") {
            if (confirm("IE浏览器版本过低，可能不能正常显示页面，请更新IE浏览器至IE10以上版本或下载第三方浏览器（Chrome、Firefox、傲游、猎豹等）！\r\n立即下载浏览器（Firefox）以便使用本系统？")) {
                window.location = 'https://www.mozilla.org/zh-CN/firefox/new/';
            }
        }

        var routers = {};
        var pageRouter = Storage.pageRouter;
        for (k in pageRouter)
            routers[k] = pageRouter[k];

        pageRouter = Login.pageRouter;
        for (k in pageRouter)
            routers[k] = pageRouter[k];

        pageRouter = UserInfo.pageRouter;
        for (k in pageRouter)
            routers[k] = pageRouter[k];

        pageRouter = Updata.pageRouter;
        for (k in pageRouter)
            routers[k] = pageRouter[k];

        pageRouter = Requirement.pageRouter;
        for (k in pageRouter)
            routers[k] = pageRouter[k];

        pageRouter = Contract.pageRouter;
        for (k in pageRouter)
            routers[k] = pageRouter[k];

        pageRouter = Search.pageRouter;
        for (k in pageRouter)
        routers[k] = pageRouter[k];

        pageRouter = MsgCenter.pageRouter;
        for (k in pageRouter)
        routers[k] = pageRouter[k];

        pageRouter = Management.pageRouter;
        for (k in pageRouter)
        routers[k] = pageRouter[k];

        Date.prototype.Format = function (fmt) {
            var o = {
                "M+": this.getMonth() + 1,                      //月
                "d+": this.getDate(),                           //日
                "h+": this.getHours(),                          //时
                "m+": this.getMinutes(),                        //分
                "s+": this.getSeconds(),                        //秒
                "q+": Math.floor((this.getMonth() + 3) / 3),   //季度
                "S": this.getMilliseconds()                     //毫秒
            };
            if (/(y+)/.test(fmt))
                fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
            for (var k in o)
                if (new RegExp("(" + k + ")").test(fmt))
                    fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
            return fmt;
        };
        template.helper("FloatFormat", function (float) {
            return Math.round(float*100)/100;
        });

        InitSwfuploadComponent(null, null, Webuploader);
        $.fn.downloadPermission = function(objId, context, cb){
            $.ajax({
                type: "POST",
                url: "/cloud/getDownloadPermission",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    Id: objId,
                    Context: context
                }),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("无下载权限.问题描述: " + data.errorMsg, "info");
                        cb(false);
                        return;
                    }
                    cb(true);
                },
                error: function () {
                    cb(false);
                }
            })
        };

        $.fn.voDefaultSetup = function(data){
            return $.extend({
                name: "",
                path: "",
                type: "",
                el_hide: null,
                el_show: null,
                bHasSpace: true,
                cb: null,
                markPos: "",
                marks: "",
                timeCB: null
            }, data);
        };
        $.fn.voSetup = {};
        var lastSetup = {};

        $.fn.ViewObject = function(){
            if (lastSetup.el_show){
                lastSetup.el_show.html("");
                lastSetup.el_show.css("display", "none");
                lastSetup.el_hide.show();
                if (lastSetup.cb)
                    lastSetup.cb("hide");
            }
            $.extend(lastSetup, $().voSetup);
            var tem = template.get('template/storage/objectViewer.html');
            var data = {objectType : lastSetup.type, objectName: lastSetup.name, bHasSpace: lastSetup.bHasSpace};
            var test = tem(data);
            lastSetup.el_show.html($.trim(test));
            lastSetup.el_show.css("display", "block");
            lastSetup.el_hide.hide();
            $(".quitObjectViewer").unbind("click").click(function(){
                lastSetup.el_show.html("");
                lastSetup.el_show.css("display", "none");
                lastSetup.el_hide.show();
                if (lastSetup.cb)
                    lastSetup.cb("hide");
                lastSetup = {};
            });
            if (lastSetup.type == 0){
                var width = parseInt(lastSetup.el_show.find('.objectViewerContent').css("width"));
                var height = width * 9 / 16;
                $.viewVideo(lastSetup.path, lastSetup.name, width, height, lastSetup.markPos, lastSetup.marks, lastSetup.timeCB);
                if (lastSetup.cb)
                    lastSetup.cb("show");
            }
            else if (lastSetup.type == 1){
                var ip = $("#imagePlayer");
                ip.attr("src",lastSetup.path);
                ip.css("max-width", lastSetup.el_show.find('.objectViewerContent').css("width"));
                if (lastSetup.cb)
                    lastSetup.cb("show");
            }
            else if (lastSetup.type == 2){
                var index = lastSetup.path.lastIndexOf('.');
                var prefix = 'pdf';
                if (index != -1){
                    prefix = lastSetup.path.substr(index + 1, lastSetup.path.length);
                }
                var pp = $("#pdfPlayer");
                var tt = $("#txtPlayer");
                pp.hide();
                tt.hide();
                if (prefix == 'pdf'){
                    var url = "script/pdf/web/viewer.html?file=" + lastSetup.path;
                    pp.attr("src", url);
                    pp.css("width", lastSetup.el_show.find('.objectViewerContent').css("width"));
                    pp.css("height", "1000px");
                    pp.show();
                }
                else if (prefix == 'txt'){
                    tt.attr("src", lastSetup.path);
                    tt.css("width", lastSetup.el_show.find('.objectViewerContent').css("width"));
                    tt.css("height", "1000px");
                    tt.show();
                }
                if (lastSetup.cb)
                    lastSetup.cb("show");
            }
        };
        $.fn.GetParamsFromUrl = function(){
            var index = window.location.href.indexOf('?');
            var params = {};
            var paramsUrl = window.location.href.substr(index + 1, window.location.length);
            var paramUrl = paramsUrl.split("&");
            var temp;
            if (index != -1){
                for (var i = 0; i < paramUrl.length; i++){
                    temp = paramUrl[i].split("=");
                    params[temp[0]] = temp[1];
                }
            }
            return params;
        };
        $.fn.GoToUrl = function(url, extraParams){
            var param = url;
            var connect = '?';
            if (extraParams){
                $.each(extraParams, function(key, value){
                    param = param + connect + key + '=' + value;
                    connect = '&';
                });
            }
            window.location.hash = param;
        };
        $.fn.calPagination = function calPagination(curPage, totalPages){
            var pagination = {
                hasNext: true,
                hasPrev: true,
                nextPage: null,
                prevPage: null,
                pages: [],
                currentPage: curPage
            };
            var step = 5;
            var temp = (curPage % 10) % step;
            if (temp == 0)
                temp = step;
            var offset = 1 - temp;
            for (var i = 0; i < step; i ++, offset ++){
                if (curPage + offset == totalPages)
                    pagination["hasNext"] = false;
                if (curPage + offset == 1)
                    pagination["hasPrev"] = false;
                if (curPage + offset >= 1 && curPage + offset <= totalPages)
                    pagination["pages"].push(curPage + offset);
                if (i == 0)
                    pagination["prevPage"] = curPage + offset - 1;
                if (i == step - 1)
                    pagination["nextPage"] = curPage + offset + 1;
            }
            return pagination;
        };
        $.fn.getOperLog = function(){
            return operLogs;
        };
        $.fn.clearOperLog = function(){
            operLogs = [];
        };
        $.fn.alipayProcess = function(subject, serialNumber, orderId, amount, useAccount, destUser, cb){
            $.ajax({
                type: "POST",
                url: "/platform/aliPay",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    Subject: subject,
                    UseAccount: useAccount,
                    Description: serialNumber,
                    OrderId: orderId
                }),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("支付请求失败.问题描述: " + data.errorMsg, "info");
                        alert('系统支付流程遇到错误，请联系平台管理员核实问题!');
                        return;
                    }
                    if (!data['bSuccess']) {
                        alert(data['description']);
                        return;
                    }
                    if (data['bAlipay']){
                        var tem = template.get('template/confirmPayBill.html');
                        var r = tem({
                            Title: subject,
                            SerialNumber: serialNumber,
                            Amount: parseFloat(amount),
                            UseAccount: parseFloat(useAccount),
                            DestUser: destUser
                        });
                        var sel = $('#beforePay_confirmBill');
                        sel.html(r);
                        sel.modal();
                        $('#payConfirm_btn').unbind('click').click(function(){
                            window.open(data['description']);
                            sel.modal('hide');
                            _cb_payConfirm();
                        });
                        $('#cancelConfirm_btn').unbind('click').click(function(){
                            sel.modal('hide');
                        });
                    }
                    else
                        cb(true);
                },
                error: function () {
                    alertState("支付请求失败，网络异常", "failed");
                }
            });
            function _cb_payConfirm() {
                var tem = template.get('template/contract/contract_payConfirm.html');
                var sel = $('#afterPay_confirmBill');
                sel.html(tem());
                $("#payConfirm_finish_btn").unbind('click').click(function () {
                    sel.modal('hide');
                    cb(true);
                });
                $("#payConfirm_failed_btn").unbind('click').click(function () {
                    sel.modal('hide');
                });
                sel.modal();
            }
        };

        $.fn.tryRetrieveSession = function(cb){
            $.ajax({
                type: "POST",
                url: "/cloud/retrieveSession",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({DBToken: $.cookie('DBToken')}),

                success: function (data) {
                    if (data.errorCode != null) { //未登录
                        getSession_cb(true, false, data);
                        return;
                    }
                    else{ //已登录
                        getSession_cb(true, true, data);
                    }
                },
                error: function () {
                    alertState("用户登录失败,网络异常", "failed");
                }
            });

            //检查session后的处理函数，由tryRetrieveSession调用
            function getSession_cb(bSuccess, hasSession, data){
                if (bSuccess && hasSession) { //已登录
                    $.fn.retrieveSession = function(){
                        return data;
                    };
                    $.fn.userHasRight = function(identity){
                        if (!data.DomainInUse)
                            return true;
                        return data.UserRights[identity];
                    };
                    $.fn.isExpireTime = function(){
                        var curDate = new Date();
                        var expireTime = new Date(data.ExpireTime);
                        return curDate.getTime() > expireTime.getTime();
                    };

                    afterLogin(); //登录后的初始化
                    cb(true);
                }else if (bSuccess){ //未登录
                    cb(false);
                }

                //初始化前端路由
                Router(routers).init();
            }

            //登录完成和页面刷新后的初始化，由getSession_cb调用
            function afterLogin(){
                var userSession = $().retrieveSession();
                userSession.IsManagement = false;

                if (!$().userHasRight("Sto_ReadOnly"))
                    $("#myStorage").css("display", "none");
                if (!$().userHasRight("Req_ReadOnly"))
                    $("#requirement_page").css("display", "none");
                if (!$().userHasRight("Con_ReadOnly"))
                    $("#contract_page").css("display", "none");
                if (!$().userHasRight("Man_ReadOnly"))
                    $("#domainManage").css("display", "none");
                if (!$().userHasRight("Per_ReadOnly"))
                    $("#modifyUserInfo_page").css("display", "none");

                //header设置
                $('#top_username').text(userSession.NickName);
                $('#top_management').text(userSession.IsService?"交易管理":"需求管理");
                $('#top_collection').href = "/collection/"+userSession.userId;
                $('#top_userzone').show();

                $("#Logout").unbind('click').click(function () {
                    $.ajax({
                        type: "POST",
                        url: "/cloud/logout",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                        }),
                        error: function () {
                            alert("网络连接失败，请检查网络");
                        },
                        success: function () {
                            $.cookie('newReq','',{expires: -1});
                            $.cookie('category_1','',{expires: -1});
                            $.cookie('category_2','',{expires: -1});
                            $.cookie('producerDomain','',{expires: -1});
                            location.href = '/';
                        }
                    });
                });

                var query_mutex = 0;
                function longQuery(){
                    if(query_mutex > 0)
                        return;
                    query_mutex ++;
                    $.ajax({
                        type: "POST",
                        url: '/platform/longQuery',
                        dataType: "json",
                        contentType: "application/json",
                        timeout: 15000,
                        data: JSON.stringify({}),
                        error: function () {
                            query_mutex --;
                            window.setTimeout(function(){longQuery();}, 10000);
                        },
                        success: function (data) {
                            query_mutex --;
                            if (data.status == 'newMsg') {
                                $('.new-msgTip').show();
                                msgAlert(data.latestMsg);
                                window.setTimeout(function(){$('#top_msgalert').slideUp()}, 5000);
                            }
                            window.setTimeout(function(){longQuery();}, 10000);
                        }
                    });
                }
                longQuery();
            };
        };

        //检查是否已登录
        $().tryRetrieveSession(function(bSuccess){
            if (!bSuccess) { //未登录，转到登录界面
                window.location.href = '/login#/loginPage';
            }
        });

        $.extend({
            Object: {
                count: function( p ) {
                    p = p || false;

                    return $.map( this, function(o) {
                        if( !p ) return o;

                        return true;
                    } ).length;
                }
            }
        });
    }
);
