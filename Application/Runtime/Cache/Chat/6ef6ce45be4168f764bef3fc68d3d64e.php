<?php if (!defined('THINK_PATH')) exit();?><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<script src="<?php echo (JS_URL); ?>jquery.js"></script>

<link rel="stylesheet" href="/tpchat/Public/bootstrap/css/bootstrap.css">
<script rel="stylesheet" src="/tpchat/Public/bootstrap/js/bootstrap.js"></script>


<link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />

<link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
<script src="<?php echo (JS_URL); ?>jquery-weui.js"></script>
<script src="<?php echo (JS_URL); ?>fastclick.js"></script>

<title>筑影学堂</title>
<style>
    .page-title{
        background-color:#dfdfdf
    }
    .arrow-left.backpage {
        margin-top: 4px
    }
    .weui-btn.weui-btn_primary{
        position: fixed; /*or前面的是absolute就可以用*/
        bottom: 0px;
        margin-left: 11%;
        margin-bottom:  5%;

        width: 75%;
    }
</style>


<!--<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">-->
<!--<meta name="format-detection" content="telephone=no">-->



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<style>
    .weui-cell{
        position:relative !important;
    }
</style>
<body>
<div class="page-title"  >
    <h2>我的作品<a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<iframe name="iframe" style="display: none"></iframe>
<form  class="weui-cells weui-cells_form"  method="post"   action="" target="iframe" style="margin-top: 9%">
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label" style="margin-top: 5px">作品标题：</label></div>
<div class="weui-cell__bd">
<input  type="text" name="video_title" id="video_title"  type="text" />
</div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">下载链接：</label></div>
<div class="weui-cell__bd">
<input class="weui-input" type="text" name="video_url">
</div>
</div>
    <div class="weui-cell" >
        <div class="weui-cell__hd" ><label class="weui-label">内容简介：</label></div>
        <div class="weui-cell__bd">
            <textarea  style="border:solid 1px #f5f5f5" class="weui-textarea" placeholder="请输入简介" rows="4" name="user_desc"> </textarea>
        </div>
    </div>

    <!--<div class="weui-cell">-->
        <!--<div class="weui-cell__hd">-->
            <!--<label class="weui-label">视频分类：</label></div>-->
        <!--<div class="weui-cell__bd">-->
        <!--<input class="weui-input" id="category" type="text"  name="video_category" />-->
    <!--</div>-->
    <!--</div>-->

    <div class="weui-cell">
    <div class="weui-cell__hd">
    <label class="weui-label">参与活动：</label></div>
        <div class="weui-cell__bd">
    <input class="weui-input" id="activity" type="text"  name="activity_title" />
    </div>
    </div>

<input style="display: none" name="openid" value="<?php echo ($open_id); ?>">
    <input style="display: none" name="chatname" value="<?php echo ($chatname); ?>">
    <input style="display: none" name="profile" value="<?php echo ($profile); ?>">

<button class="weui-btn weui-btn_primary"    >确定</button>
</form>

<!-- 将form表单提交的窗口指向隐藏的ifrmae,并通过ifrmae提交数据。 -->

</body>
<script>
//    $("#category").select({
//        title: "选择分类",
//        items: ["原创视频", "实践表演"]
//    });




    $(document).ready(function () {
        $(".weui-btn.weui-btn_primary").click(function(){
            $.alert({
                title: '',
                text: '提交成功，请等待审核...',
                onOK: function () {
                    window.location.href="/tpchat/index.php/Chat/User/video"
                    }
            });
        });
    });
</script>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>