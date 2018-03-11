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
    <h2><span>我 的 课 程</span><a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<div class="weui-panel weui-panel_access">
    <div class="weui-panel__hd">我的课程</div>

</div>
<div class="weui-panel__bd" style="margin-bottom: 20%">

    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><a  href="<?php echo U('user/tradeinfo');?>?trade_id=<?php echo ($v["trade_id"]); ?>" class="weui-media-box weui-media-box_appmsg">
            <div class="weui-media-box__hd">
                <img class="weui-media-box__thumb" src="<?php echo (SHOW_URL); echo ($v["image"]); ?>">
            </div>
            <div class="weui-media-box__bd">
                <h4 class="weui-media-box__title"><?php echo ($v["title"]); ?></h4>
                <p class="weui-media-box__desc">支付状态：<?php echo ($v["trade_state"]); ?></p>
                <?php if($v["trade_state"] == 已支付 ): ?><p class="weui-media-box__desc" >凭证 ： <?php echo ($v["evidence"]); ?></p><?php endif; ?>
                <p class="weui-media-box__desc"  style="text-align: end">¥ <?php echo ($v["final_price"]); ?></p>
                <p class="weui-media-box__desc" style="text-align: end" ><?php echo ($v["trade_createtime"]); ?></p>


            </div>
        </a ><?php endforeach; endif; else: echo "" ;endif; ?>

</div>
<style>
    a{

        margin: 0 auto;
    }


</style>
<div class="weui-tabbar" style="text-align: center;
position:fixed ;background:url('http://www.jianpianzi.com/tpchat/Public/img/nav_bar.png')" >
    <a href="/tpchat/index.php/Chat">

        <img  src="<?php echo (IMG_URL); ?>nav_index.png" alt="">

    </a>
    <a href="/tpchat/index.php/Chat/log"   >

        <img  src="<?php echo (IMG_URL); ?>nav_message.png" alt="">
    </a>
    <a href="/tpchat/index.php/Chat/user" >

        <img  src="<?php echo (IMG_URL); ?>nav_user.png" alt="">

    </a>

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