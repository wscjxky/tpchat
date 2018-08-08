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
<div class="page-title"  >
    <h2><span>签到详情</span><a href="<?php echo U('user/index');?>" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<div class="weui-panel weui-panel_access">
    <div class="weui-panel__hd">我的签到</div>

</div>
<div class="weui-cells" style="margin-bottom: 20%">

    <?php if(is_array($course)): $i = 0; $__LIST__ = $course;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$course): $mod = ($i % 2 );++$i;?><h1 style="padding: 3%; ">课程标题：<?php echo ($course["title"]); ?></h1>
        <h1 style="padding: 3%; ">主讲：<?php echo ($course["speaker"]); ?></h1>
        <h1 style="padding: 3%; ">地点：<?php echo ($course["address"]); ?></h1>
        <h1 style="padding: 3%; ">开课时间：<?php echo ($course["starttime"]); ?></h1>
        <h1 style="padding: 3%; ">联系电话：<?php echo ($course["phone"]); ?></h1>
        <h1 style="padding: 3%; ">签到次数：<?php echo ($course["use_count"]); ?></h1>
        <h1 style="padding: 3%; ">最新签到时间：<?php echo ($course["createtime"]); ?></h1>
        <h1 style="padding: 3%; ">凭证码：<?php echo ($course["evidence"]); ?></h1><?php endforeach; endif; else: echo "" ;endif; ?>

</div>
</body>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>