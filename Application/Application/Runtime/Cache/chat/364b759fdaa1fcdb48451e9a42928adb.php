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
    function showAlert() {
        var message=confirm('本次活动您已报名。');
        if(message==true) {
            window.location.href = 'http://www.jianpianzi.com/tpchat/index.php/Chat/User/trade';
        }
    }
</script>
<body >
<div id="qrcode" style="position: fixed ;display: none"></div>
<div class="weui-panel__bd" style="padding: 10px"><?php echo ($data["content"]); ?></div>
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
    <?php if($agent == 0): else: ?>
        <a href="javascript:qrcode()" >
            <img  src="<?php echo (IMG_URL); ?>nav_qrcode.png" alt="">
        </a><?php endif; ?>

    <?php if($data["price"] != 0): ?><a href="/tpchat/index.php/Chat/Index/trade?course_id=<?php echo ($data["course_id"]); ?>" >
            <img  src="<?php echo (IMG_URL); ?>nav_register.png" alt="">
        </a>
        <?php else: ?>

        <?php if($activity_state != 0): ?><a href="javascript:showAlert()" >
                <img  src="<?php echo (IMG_URL); ?>nav_register.png" alt="">
            </a>
            <?php else: ?>
                    <a href="/tpchat/index.php/Chat/Index/enroll?course_id=<?php echo ($data["course_id"]); ?>" >
                        <img  src="<?php echo (IMG_URL); ?>nav_register.png" alt="">
                    </a><?php endif; endif; ?>

</div>

</body>

<!-- body 最后 -->
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
<script src="<?php echo (JS_URL); ?>jquery-weui.js"></script>
<script src="<?php echo (JS_URL); ?>fastclick.js"></script>
</html>