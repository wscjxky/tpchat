define(['jquery', 'template'], function ($, Template) {
    Template.helper("ParseTime", function (date) {
        var d = new Date(date);
        return d.Format("yyyy-MM-dd hh:mm");
    });

    function MsgCenter(){
        $.ajax({
            type: "POST",
            url: '/platform/getMsg',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({}),
            success: function (data) {
                console.log(typeof(data));
                console.log((data));
                var tem = Template.get('template/msgCenter/msgCenter.html');
                var t = tem(data);

                $('#pageContent').html($.trim(t));
                $('.new-msgTip').hide();
                action();
            }
        });
    }
    function action(){
        $('.newMsg-list a').unbind('click').click(function(e){
            var resourceType = $(e.currentTarget).attr('name');
            var resourceId = $(e.currentTarget).attr('value');
            if (resourceType == 'contract'){
                $().GoToUrl('/requirement/' + resourceId);
                delMsg(null, $(e.currentTarget).find('input').val(), false);
            }
            else if (resourceType == 'requirement'){
                window.location.href = '/session#/requirement/' + resourceId;
                delMsg(null, $(e.currentTarget).find('input').val(), false);
            }
        });
        $('.del_msg').unbind('click').click(function(e){
            delMsg($().retrieveSession().UserId, null, true);
        });
    }
    function delMsg(userId, msgId, bRefresh){
        var param = {};
        if (userId)
            param['UserId'] = userId;
        else if (msgId)
            param['MsgId'] = msgId;
        $.ajax({
            type: "POST",
            url: '/platform/delMsg',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function () {
                if (bRefresh)
                    MsgCenter();
            }
        });
    }

    var msgCenter_interface = {};
    msgCenter_interface.pageRouter = {
        '/msgCenter': MsgCenter
    };
    return msgCenter_interface
});