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


<!--<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">-->
<!--<meta name="format-detection" content="telephone=no">-->



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="page-title"  >
    <h2>我的作品<a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<iframe name="iframe" style="display: none"></iframe>
<form  class="weui-cells weui-cells_form"  method="post"   action="" target="iframe" style="margin-top: 15%">
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">标题</label></div>
<div class="weui-cell__bd">
<input  type="text" name="video_title" id="video_title"  type="text" />
</div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">视频链接</label></div>
<div class="weui-cell__bd">
<input class="weui-input" type="text" name="video_url">
</div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">分类</label></div>
<div class="weui-cell__bd">
<input class="weui-input" id="category" type="text"  name="video_category" />
</div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">简介</label></div>
<div class="weui-cell__bd">
<textarea class="weui-textarea" placeholder="请输入简介" rows="4" name="user_desc"> </textarea>
<div class="weui-textarea-counter"><span>0</span>/200</div>
</div>
</div>
<input style="display: none" name="openid" value="<?php echo ($open_id); ?>">
<div class="weui-btn-area" style="margin-top: 20%">
<button class="weui-btn weui-btn_primary" style="bottom: 0; ;width: 100%" >确定</button>
</div>
</form>

<!-- 将form表单提交的窗口指向隐藏的ifrmae,并通过ifrmae提交数据。 -->

</body>
<script>
    $("#category").select({
        title: "选择分类",
        items: ["情景", "写实", "测试", "测试", "测试", "测试"],
        onChange: function(d) {
            console.log(this, d);
        },
        onClose: function() {
            console.log("close");
        },
        onOpen: function() {
            console.log("open");
        }
    });


    $(document).ready(function () {
        $(".weui-btn.weui-btn_primary").click(function(){
            $.alert({
                title: '成功',
                text: '提交成功，谢谢您的支持！',
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