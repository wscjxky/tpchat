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
<?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><div  class="weui-media-box weui-media-box_appmsg">

    <div class="weui-media-box__hd">
        <img src="http://www.cunpianzi.com/tpchat/Public/upload/image/logo.jpg" style="margin-bottom:66%;width:40px;height:40px">
    </div>
    <div class="weui-media-box__bd">
        <div class="weui-media-box__title" style="font-size: 12px">
            <?php echo ($v["admin_username"]); ?>
        </div>
        <p style="margin-top: 10px;margin-bottom: 10px" class="weui-media-box__desc">
            <?php echo ($v["content"]); ?></p>
        <p  onclick="window.location.href='http://www.baidu.com'" style="margin-top: 10px;margin-bottom: 5px;color: blue;font-size: 12px" class="weui-media-box__desc">
            戳我链接</p>
        <p class="weui-media-box__desc" >
            <?php echo ($v["createtime"]); ?></p>

    </div>
</div><?php endforeach; endif; else: echo "" ;endif; ?>

<style>
    a{

        margin: 0 auto;
    }


</style>
<div class="weui-tabbar" style="text-align: center;
position:fixed ;background:url('http://www.cunpianzi.com/tpchat/Public/img/nav_bar.png')" >
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