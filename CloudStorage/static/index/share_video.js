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
    CKobject.embedHTML5('video_player','ckplayer_a1',800,300,video,flashvars,support);
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

$('#share-video').click(function(e){
    $('.shareBox').show();
    $('#share-video').css('display', 'none');
    $('#cancel-share-video').css('display', 'inline-block');
    $.ajax({
        type: "POST",
        url: "/cloud/shareVideo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({BShare: true, ObjectId: parseInt($(e.currentTarget).attr('value'))}),
        success: function (data) {
        },
        error: function () {
        }
    });
});
$('#cancel-share-video').click(function(e){
    $('.shareBox').hide();
    $('#share-video').css('display', 'inline-block');
    $('#cancel-share-video').css('display', 'none');
    $.ajax({
        type: "POST",
        url: "/cloud/shareVideo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({BShare: false, ObjectId: parseInt($(e.currentTarget).attr('value'))}),
        success: function (data) {
        },
        error: function () {
        }
    });
});