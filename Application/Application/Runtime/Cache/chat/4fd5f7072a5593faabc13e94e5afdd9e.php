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
    <title>实践课堂</title>
</head>


<body ontouchstart>
<div style="margin-bottom: 20%">

            <div style="padding: 8px"><i style="color: #999;padding: 8px;
    font-size: 28px;">作品集锦</i>

            </div>

                <div class="weui-panel__bd"  >
                    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i; if($v["publish_state"] == 1 ): ?><a href="<?php echo ($v["url"]); ?>" class="weui-media-box weui-media-box_appmsg">
                                <div class="weui-media-box__hd">
                                    <img class="weui-media-box__thumb" src="<?php echo ($v["image"]); ?>">
                                </div>
                                <div class="weui-media-box__bd">
                                    <h4 class="weui-media-box__title"><?php echo ($v["title"]); ?></h4>
                                    <p class="weui-media-box__desc"><?php echo ($v["content"]); ?></p>

                                </div>
                            </a><?php endif; endforeach; endif; else: echo "" ;endif; ?>

                </div>



</div>
</body>
<!-- body 最后 -->



</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>