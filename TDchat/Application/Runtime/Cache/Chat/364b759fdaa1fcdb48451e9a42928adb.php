<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>

<html lang="en">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">

<script src="<?php echo (JS_URL); ?>jquery.js"></script>

<link rel="stylesheet" href="/tpchat/Public/bootstrap/css/bootstrap.css">
<script rel="stylesheet" src="/tpchat/Public/bootstrap/js/bootstrap.js"></script>
<style>
    p{
        margin: 0 0 0;
    }
</style>
<head>
    <meta charset="UTF-8">
    <title>实践课堂</title>
    
    <script src="<?php echo (JS_URL); ?>jquery.qrcode.min.js"  type="text/javascript"></script>
    <link href="/tpchat/Public/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <link href="/tpchat/Public/froala_editor/css/froala_editor.pkgd.min.css" rel="stylesheet" type="text/css" />
    <link href="/tpchat/Public/froala_editor/css/froala_style.min.css" rel="stylesheet" type="text/css" />
</head>
<script type="text/javascript">
    $(document).ready(function(){
        $("#qrcode").qrcode("http://www.jianpianzi.com/tpchat/index.php/chat/index/course?courseid=<?php echo ($data["course_id"]); ?>&aid=<?php echo ($aid); ?>").css("left","16%").css("top","20%");
    });
    function qrcode() {
        //二维码消失
        if($(".weui-panel__bd").css('opacity')==0){
            $(".weui-panel__bd").css('opacity','1');
            $("#qrcode").css('display','none');
        }
        else{
        $(".weui-panel__bd").css('opacity','0');
            $("#qrcode").css('display','block');

//        console.log("http://www.jianpianzi.com/tpchat/index.php/chat/index/course?title=<?php echo ($data["title"]); ?>&openid=<?php echo ($openid); ?>");
    }
    }
</script>
<body >
<div id="qrcode" style="position: fixed ;display: none"></div>
<div class="weui-panel__bd" style="padding: 5px"><?php echo ($data["content"]); ?></div>
        <ul class="weui-media-box__info" style="margin-bottom: 100px">
            <li class="weui-media-box__info__meta">适合年龄段：<?php echo ($data["age_limit"]); ?></li>
            <li class="weui-media-box__info__meta ">招收人数：<?php echo ($data["people_limit"]); ?></li>
        </ul>
<style>
    a{

        margin: 0 auto;
    }
</style>
<div class="weui-tabbar" style="text-align: center;position:fixed ;background:url('http://www.jianpianzi.com/tpchat/Public/img/nav_bar.png')" >
    <a href="tel:010-85388138#mp.weixin.qq.com">

        <img  src="<?php echo (IMG_URL); ?>nav_phone.png" alt="">

    </a>
    <a href="javascript:qrcode()"  style="display: none" >

        <img  src="<?php echo (IMG_URL); ?>nav_qrcode.png" alt="">
    </a>
    <a href="<?php echo ($trade_url); ?>" >

        <img  src="<?php echo (IMG_URL); ?>nav_register.png" alt="">

    </a>

</div>

</body>

<!-- body 最后 -->
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
<script src="<?php echo (JS_URL); ?>jquery-weui.js"></script>
<script src="<?php echo (JS_URL); ?>fastclick.js"></script>
</html>