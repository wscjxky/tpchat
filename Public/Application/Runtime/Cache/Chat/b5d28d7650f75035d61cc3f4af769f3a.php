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
    <h2>意见<a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<iframe name="iframe" style="display: none"></iframe>
<form  class="weui-cells weui-cells_form"  method="post"   action="" target="iframe" style="margin-top: 20%">



        <div class="weui-cell__bd">
            <textarea class="weui-textarea" placeholder="发表对课程的看法和新课程的设置建议等" rows="10" name="content"></textarea>
            <div class="weui-textarea-counter"><span>0</span>/256</div>
        </div>
    </div>
    <input style="display: none" name="openid" value="<?php echo ($open_id); ?>">
    <div class="weui-btn-area" style="margin-top: 20%">
        <button class="weui-btn weui-btn_primary" type="submit" style="bottom: 0;  ;width: 100%" >确定</button>
    </div>
</form>

<!-- 将form表单提交的窗口指向隐藏的ifrmae,并通过ifrmae提交数据。 -->

</body>
<script>


    $(document).ready(function () {
        $(".weui-btn.weui-btn_primary").click(function(){
            $.alert({
                title: '成功',
                text: '提交成功，谢谢您的支持！',
                onOK: function () {
                    window.location.href="/tpchat/index.php/Chat/User/advice"
                }
            });
        });
    });
</script>
</html>

<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>