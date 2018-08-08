<?php if (!defined('THINK_PATH')) exit();?>
<html lang="en">
<head>
    <title>作品集锦</title>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <script src="<?php echo (JS_URL); ?>jquery.js"></script>

    <link rel="stylesheet" href="/tpchat/Public/bootstrap/css/bootstrap.css">
    <script rel="stylesheet" src="/tpchat/Public/bootstrap/js/bootstrap.js"></script>


    <link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />

    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
    <script src="<?php echo (JS_URL); ?>jquery-weui.js"></script>
    <script src="<?php echo (JS_URL); ?>fastclick.js"></script>
    <meta charset="UTF-8">
    <title>消息</title>

</head>
<html lang="en">


<body ontouchstart>
<div style="margin-bottom: 20%">

                <div class="weui-panel__bd"  >
                    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><a href="<?php echo ($v["confirm_url"]); ?>" class="weui-media-box weui-media-box_appmsg">
                            <div class="weui-media-box__hd">
                                <img class="weui-media-box__thumb" src="<?php echo ($v["image"]); ?>">
                            </div>
                            <div class="weui-media-box__bd">
                                <h4 class="weui-media-box__title"><?php echo ($v["title"]); ?></h4>
                                <p class="weui-media-box__desc"><?php echo ($v["admin_desc"]); ?></p>
                                <p class="weui-media-box__desc"><?php echo ($v["content"]); ?></p>
                                <p style="text-align: end" class="weui-media-box__desc"><?php echo ($v["createtime"]); ?></p>

                            </div>
                        </a><?php endforeach; endif; else: echo "" ;endif; ?>

                </div>



</div>
</body>
<!-- body 最后 -->



</html>