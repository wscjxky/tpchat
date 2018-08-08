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
<body>
<div class="page-title"  style="position: relative"  >
    <h2>意见<a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<iframe name="iframe" style="display: none"></iframe>
<form method="post"   action="" target="iframe" style="">
        <div style="padding: 5%" class="weui-cell__bd">
            <textarea class="weui-textarea" placeholder="发表对课程的看法和新课程的设置建议等" rows="10" name="content"></textarea>
        </div>
    </div>
    <input style="display: none" name="openid" value="<?php echo ($open_id); ?>">
    <input style="display: none" name="chatname" value="<?php echo ($chatname); ?>">

    <div class="weui-btn-area" style="margin-top: 20%">
        <button class="weui-btn weui-btn_primary" type="submit"  >确定</button>
    </div>
</form>

<!-- 将form表单提交的窗口指向隐藏的ifrmae,并通过ifrmae提交数据。 -->

</body>
<script>


    $(document).ready(function () {
        $(".weui-btn.weui-btn_primary").click(function(){
            $.alert({
                title: '',
                text: '提交成功，谢谢您的支持！',
                onOK: function () {
                    window.location.href="/tpchat/index.php/Chat/User/advice"
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