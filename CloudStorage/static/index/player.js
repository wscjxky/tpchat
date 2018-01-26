function checkBroweser(){
    var sUserAgent = navigator.userAgent.toLowerCase();
    var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
    var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
    var bIsMidp = sUserAgent.match(/midp/i) == "midp";
    var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
    var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
    var bIsAndroid = sUserAgent.match(/android/i) == "android";
    var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
    var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
    if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM)
        return 0;
    else
       return 1;
}
if (checkBroweser()==0){
    var sUserAgent = navigator.userAgent.toLowerCase();
    var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
    var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
    if (bIsIpad || bIsIphoneOs)
        var videoFilePath = $('#video_path').val().replace('123.57.157.64:8080','123.57.157.64:800');
    else
        var videoFilePath=$('#video_path').val();
    var flashvars=null ;
    var video=[videoFilePath+'->video/mp4']
    var support=['all'];
    var params={bgcolor:'#FFF',allowFullScreen:true,allowScriptAccess:'always',wmode:'transparent'};
    var flashvars={
        p:1,
        e:1
    };
    CKobject.embedHTML5('video_player','ckplayer_a1',960,560,video,flashvars,support);
}else{
    var videoFilePath=$('#video_path').val();
    var flashvars=null ;
    var params={bgcolor:'#FFF',allowFullScreen:true,allowScriptAccess:'always',wmode:'transparent'};
    var video=[videoFilePath+'->video/mp4'];
    flashvars={
        f:videoFilePath,
        c:0,
        b:1,
        k:'',
        n:'',
        h:'4',
        q:'start',
        p:1,
        h:4
    };
    CKobject.embedSWF('/static/script/player/ckplayer/ckplayer.swf','video_player','ckplayer_a1',960,560,flashvars,params);
}
$('#favorite').unbind('click').click(function(){
    CheckLogin(function(){
        $.ajax({
            type: "POST",
            url:"/favorVideo",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                ZoneItemId:$('#VideoInfo').val()
            }),
            success: function (data) {
                if(data.bSuccess)
                    $('#cb_info').text(' 已赞 ' + data.count);
            },
            error:function(){
                alert('请检查网络。');
            }
        });
    });
});
$('#collect_video').unbind('click').click(function(){
    CheckLogin(function () {
        $.ajax({
            type: "POST",
            url:"/collectVideo",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                ZoneItemId:$('#VideoInfo').val()
            }),
            success: function (data) {
                if(!data.bSuccess)
                    self.location='/login#/loginPage';
                else
                    $('#cb_collect_video').text(' 已收藏 ');
            },
            error:function(){
                alert('请检查网络。');
            }
        });
    });
});
$('#collect_producer').unbind('click').click(function(){
    CheckLogin(function () {
        $.ajax({
            type: "POST",
            url:"/collectProducer",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                DomainId:$('#VideoInfo_domain').val()
            }),
            success: function (data) {
                if(!data.bSuccess)
                    self.location='/login#/loginPage';
                else
                    $('#cb_collect_producer').text(' 已关注 ');
            },
            error:function(){
                alert('请检查网络。');
            }
        });
     });
});
$('#video-require').unbind('click').click(function(){
    $.cookie('newReq',true,{path:'/'});
    $.cookie('category_1',$('#zi-category_1').val(),{path:'/'});
    $.cookie('category_2',$('#zi-category_2').val(),{path:'/'});
    $.cookie('producerDomain',$('#VideoInfo_domain').val(),{path:'/'});
    $.cookie('refer_url',self.location,{path:'/'});
    $.cookie('refer_name',$('#refer_name').val(),{path:'/'});
    $.cookie('referPrice',$('#ReferPrice').val(),{path:'/'});
    $.cookie('tags',$('#tags').val(),{path:'/'});
    self.location='/submit';
});
$('#btn-comment').unbind('click').click(function(){
    $.ajax({
        type: "POST",
        url:"/addVideoComment",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            Content:$('#player-comment').val(),
            ObjectId:$('#VideoInfo_obj').val()
        }),
        success: function (data) {
            if(data.bSuccess != null)
                alert('评论失败，请检查网络。');
            else{
                $('#comment-area').html(data);
                $('#player-comment').val('');
            }
        },
        error:function(){
            alert('请检查网络。');
        }
    });
});