<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <title>课程签到</title>
    <script src="<?php echo (JS_URL); ?>jquery.js"></script>

    <link rel="stylesheet" href="/tpchat/Public/bootstrap/css/bootstrap.css">
    <script rel="stylesheet" src="/tpchat/Public/bootstrap/js/bootstrap.js"></script>


    <link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />

    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
    <script src="<?php echo (JS_URL); ?>jquery-weui.js"></script>
    <script src="<?php echo (JS_URL); ?>fastclick.js"></script>


</head>
<body>
<form method="post" action="#" style="margin-top: 30%">
    <p style="text-align: center"><?php echo ($chatname); ?>学员您好</p>

    <div class="weui-cells__title">凭证</div>
    <div class="weui-cells">
    <div class="weui-cell">
        <div class="weui-cell__bd">
            <input class="weui-input" style="height:10%" type="text" name="evidence" placeholder="请输入凭证">
            <input style="display: none" value="<?php echo ($openid); ?>">
        </div>
    </div>
</div>
<button style="margin-top: 10%" type="submit" class="weui-btn weui-btn_primary">确认</button>
</form>
</body>
</html>