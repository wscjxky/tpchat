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
</head >


<style>

    h1{
        font-size: 30px;
        padding: 12px;
    }


</style>

<body ontouchstart>
<div class="page-title"  >
    <h2><span>我的建议</span><a href="<?php echo U('user/index');?>" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<div class="weui-panel weui-panel_access">
    <div class="weui-panel__hd">我的课程</div>
</div>
<div class="weui-panel__bd" style="margin-bottom: 15%">
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><a href="" class="weui-media-box weui-media-box_appmsg">

            <div class="weui-media-box__bd">
                <h2 style="padding: 5px" class="weui-media-box__title">建议：<?php echo ($v["content"]); ?></h2>
                <p style="padding: 5px"class="weui-media-box__desc" >时间：<?php echo ($v["createtime"]); ?></p>
                <p style="padding: 5px" class="weui-media-box__desc">平台回复：<?php echo ($v["reply"]); ?></p>
            </div>
        </a><?php endforeach; endif; else: echo "" ;endif; ?>
    <a href="/tpchat/index.php/Chat/User/addadvice" class="weui-btn weui-btn_primary" >提交建议</a>
</div>



</body>

<script>
    $(document).ready(function () {

    });

</script>
</html>

</body>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>