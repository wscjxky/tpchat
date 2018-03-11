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



<html lang="en">
<head>
    <title>最新活动</title>
</head>
<style>
    body{

    }
    .course_title{
        font-weight: bold;
        font-size: 16px;
        overflow: hidden;

        text-overflow: ellipsis;

        display: -webkit-box;

        -webkit-box-orient: vertical;

        -webkit-line-clamp: 1;

    }
    .weui-media-box__bd{
        margin-left: 18px;
    }
    .weui-media-box_appmsg{
        margin-bottom: 24px;
    }
    .weui-panel__bd{
        margin-bottom: 20%;
    }
    .weui-media-box__desc{
        margin-top: 4px;
    }
</style>

<body ontouchstart >
<div class="weui-panel__bd" style='padding: 8px'>
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><div  class="weui-media-box weui-media-box_appmsg" style='padding: 5px'>
                <img style='width: 85px;height: 65px;vertical-align: top;margin-top: 6px'  src="<?php echo (SHOW_URL); echo ($v["image"]); ?>">
                <div class="weui-media-box__bd">
                    <a  href='/tpchat/index.php/Chat/Product/video?video_id=<?php echo ($v["video_id"]); ?>' class="course_title">
                        <?php echo ($v["video_title"]); ?></a>
                    <p class="weui-media-box__desc"  >
                        <?php echo ($v["admin_desc"]); ?>
                    </p>
                    <p class="weui-media-box__desc"  >
                        <?php echo ($v["chatname"]); ?>     <?php echo ($v["confirm_time"]); ?>   <span style="float: right">点赞数：<?php echo ($v["praise_count"]); ?></span> </p>


                </div>
            </div><?php endforeach; endif; else: echo "" ;endif; ?>
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