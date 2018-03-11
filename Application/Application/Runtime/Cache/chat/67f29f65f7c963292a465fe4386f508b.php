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
<body ontouchstart>
<div class="page-title"  >
    <h2><span>我 的 积 分</span><a  href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<div class="weui-cells" style="margin-top:15%">
    <div class="weui-cell">
        <div class="weui-cell__bd">
            <p>当前可用积分</p>
        </div>
        <div class="weui-cell__ft"><?php echo ($data["bonus_current"]); ?></div>
    </div>
    <div class="weui-cell">
        <div class="weui-cell__bd">
            <p>已获取的积分总额</p>
        </div>
        <div class="weui-cell__ft"><?php echo ($data["bonus_total"]); ?></div>
    </div><div class="weui-cell">
    <div class="weui-cell__bd">
        <p>已消费的积分总额</p>
    </div>
    <div class="weui-cell__ft"><?php echo ($data["bonus_cost"]); ?></div>
</div>
</div>
</body>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>