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
<html>
 <head> 
  <meta charset="UTF-8" /> 
  <link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />
  <link href="<?php echo (CSS_URL); ?>center.css" rel="stylesheet" />

 </head>
 <style>
  h2{
   margin-top:6px;
  }
  .username{
   margin-top: 10px;
  }
 </style>
 <body ontouchstart >
<div class="wraper">
   <div class="user-center">
    <div class="center-inner">
     <div class="my-info">
      <a href="/tpchat/index.php/Chat/User/userinfo">
       <div class="avatar">
        <img src="<?php echo ($data["profile"]); ?>">
       </div>
       <div class="visitor">
        <p class="username"><?php echo ($data["username"]); ?></p>

       </div> </a>
     </div>
     <div class="order-item" style="margin-top: 10px">
      <div class="module-title">
       <h2 ><a class="link-area" href="/tpchat/index.php/Chat/User/trade">我的课程
        <span class="fr gray666">查看全部课程</span><i class="arrow-right"></i></a></h2>
      </div>
      <div class="module-title nomar">
       <h2><a class="link-area" href="/tpchat/index.php/Chat/User/register">我的签到<span class="fr gray666"></span><i class="arrow-right"></i></a></h2>
      </div>
     </div>

     <div class="module-title ">
      <h2 class="service" data-service="true"><a href="/tpchat/index.php/Chat/User/point" class="link-area">我的积分</a><i class="arrow-right"></i></h2>
     </div>
     <div class="module-title nomar">
      <h2 class="service" data-service="true"><a href="/tpchat/index.php/Chat/User/cash" class="link-area">我的提现</a><i class="arrow-right"></i></h2>
     </div>
     <div class="module-title">
      <h2><a class="link-area address" href="/tpchat/index.php/Chat/User/video">我的作品<i class="arrow-right"></i></a></h2>

     </div>
     <div class="module-title nomar">
      <h2 class="service" data-service="true"><a href="/tpchat/index.php/Chat/User/advice" class="link-area">我的建议</a><i class="arrow-right"></i></h2>

     </div>
    </div>
   </div>
</div>

<style>
    a{

        margin: 0 auto;
    }


</style>
<div class="weui-tabbar" style="text-align: center;
position:fixed ;background:url('https://www.jianpianzi.com/tpchat/Public/img/nav_bar.png')" >
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

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>