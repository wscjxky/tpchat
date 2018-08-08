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


<!--<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">-->
<!--<meta name="format-detection" content="telephone=no">-->



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<style>

</style>
<body>
<div class="page-title"  >
    <h2><span>课程详情</span><a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>

<div class="weui-cells" style="margin-top: 16%;">
    <h1 style="padding: 3%; ">课程标题：<?php echo ($course["title"]); ?></h1>
    <h1 style="padding: 3%; ">子标题：<?php echo ($course["subtitle"]); ?></h1>
    <h1 style="padding: 3%; ">主讲：<?php echo ($course["speaker"]); ?></h1>
    <h1 style="padding: 3%; ">地点：<?php echo ($course["address"]); ?></h1>
    <h1 style="padding: 3%; ">开课时间：<?php echo ($course["starttime"]); ?></h1>
    <h1 style="padding: 3%; ">联系电话：<?php echo ($course["phone"]); ?></h1>


</div>

<div class="weui-cells">
    <?php if($data["trade_state"] == 已支付 ): if(is_array($evidencelist)): $i = 0; $__LIST__ = $evidencelist;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><div class="weui-cell weui-cell_access">
                <div class="weui-cell__bd">
                    <p><?php echo ($v); ?></p>
                </div>

            </div><?php endforeach; endif; else: echo "" ;endif; ?>
        <div style="text-align:center "class="weui-cell__ft">
            长按复制凭证码
        </div>
        <?php else: ?>
            <a class="weui-cell weui-cell_access" href="/tpchat/index.php/home/jspay?trade_id=<?php echo ($data["trade_id"]); ?>">
                <button class="weui-form-preview__btn weui-form-preview__btn_primary" >您还没有支付呢，点击立即支付</button>
            </a><?php endif; ?>




</div>
</body>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>