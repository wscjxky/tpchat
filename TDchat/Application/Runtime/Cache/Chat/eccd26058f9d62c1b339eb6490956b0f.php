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
    <h2><span>签到</span><a href="<?php echo U('user/index');?>" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<div class="weui-panel weui-panel_access">
    <div class="weui-panel__hd">我的签到</div>

</div>
<div class="weui-panel__bd" style="margin-bottom: 20%">
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><a  href="/tpchat/index.php/Chat/User/registerinfo?evidence_id=<?php echo ($v["evidence_id"]); ?>" class="weui-media-box weui-media-box_appmsg">
            <div class="weui-media-box__hd">
                <img class="weui-media-box__thumb" src="<?php echo (SHOW_URL); echo ($v["image"]); ?>">
            </div>
            <div class="weui-media-box__bd">
                <h4 class="weui-media-box__title"><?php echo ($v["title"]); ?></h4>
                <p class="weui-media-box__desc" >凭证 ： <?php echo ($v["evidence"]); ?></p>
                <p class="weui-media-box__desc"  style="text-align: end">已签到次数 ：<?php echo ($v["use_count"]); ?></p>
                <p class="weui-media-box__desc" style="text-align: end" >最新签到时间<?php echo ($v["createtime"]); ?></p>
            </div>
        </a ><?php endforeach; endif; else: echo "" ;endif; ?>
</div>
<script>

</script>
</body>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>