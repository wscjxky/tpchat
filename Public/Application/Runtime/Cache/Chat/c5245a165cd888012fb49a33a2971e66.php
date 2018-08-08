<?php if (!defined('THINK_PATH')) exit();?>
<html lang="en">
<head>
    <title>消息</title>

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
<body>
<div class="weui-cells" style="margin-bottom: 150px">
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><a href="<?php echo ($v["link"]); ?>" class="weui-cell" style="font-size: 25px">
        <div class="weui-cell__bd">
            <p><?php echo ($v["content"]); ?></p>
            <p style="font-size: 1px"> <?php echo ($v["createtime"]); ?></p>

        </div>
        <div class="weui-cell__ft" style="font-size: 6px">
            <?php if(($v.openid=='')): ?>系统消息
            <?php else: ?> 个人消息<?php endif; ?>
        </div>
    </a><?php endforeach; endif; else: echo "" ;endif; ?>
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
</body>
</html>