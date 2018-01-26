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
</style>


<!--<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">-->
<!--<meta name="format-detection" content="telephone=no">-->



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>

<body ontouchstart>
<style>
    /*span{*/
        /*float: right ;*/

    /*}*/
    /*p{*/
        /*font-size: 15px;*/
        /*padding: 3px*/
    /*}*/
    h1{
        font-size: 30px;
        padding: 12px;
    }
    /*li{*/
        /*list-style-type:none;*/
        /*border-bottom:1px solid #0c0c0c ;*/
        /*padding: 2px*/
    /*}*/
</style>
<div class="page-title"  >
    <h2>我的作业<a href="<?php echo U('user/index');?>" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<div class="weui-panel__bd" style="margin-top: 15%;margin-bottom: 15%">
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><a href="<?php echo ($v["confirm_url"]); ?>" class="weui-media-box weui-media-box_appmsg">
            <div class="weui-media-box__bd">
                <h4 class="weui-media-box__desc">作业标题：<?php echo ($v["video_title"]); ?></h4>
                <p class="weui-media-box__desc">下载链接：<?php echo ($v["video_url"]); ?></p>
                <p class="weui-media-box__desc">视频分类：<?php echo ($v["video_category"]); ?></p>

                <p class="weui-media-box__desc" >内容简介：<?php echo ($v["user_desc"]); ?></p>
                <p class="weui-media-box__desc" >审核状态：<?php echo ($v["check_status"]); ?></p>

                <p class="weui-media-box__desc" >平台评论：<?php echo ($v["admin_comment"]); ?></p>
                <p class="weui-media-box__desc" >平台打分：<?php echo ($v["score"]); ?></p>

            </div>
        </a><?php endforeach; endif; else: echo "" ;endif; ?>
    <a href="/tpchat/index.php/Chat/User/addvideo" class="weui-btn weui-btn_primary" style="bottom: 0;position: fixed ;width: 100%">上传</a>

</div>



</body>

<script>
    $(document).ready(function () {

    });

</script>
</html>


<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>