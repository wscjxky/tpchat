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
<body ontouchstart>
<div class="page-title"  >
    <h2><span>我 的 提 现</span><a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>
</div>
<div class="weui-cells" style="margin-top:15%">
    <div class="weui-cell">
        <div class="weui-cell__bd">
            <p  >当前可提现金</p>
        </div>
        <div class="weui-cell__ft" id='cash_current'><?php echo ($data["cash_current"]); ?></div>
    </div>
    <div class="weui-cell">
        <div class="weui-cell__bd">
            <p>总共赚取的现金</p>
        </div>
        <div class="weui-cell__ft"><?php echo ($data["cash_total"]); ?></div>
    </div>
    <div class="weui-cell">
    <div class="weui-cell__bd">
        <p>已提的现金</p>
    </div>
    <div class="weui-cell__ft"><?php echo ($data["cash_cost"]); ?></div>
</div>
    <div class="weui-cell">
        <div class="weui-cell__bd">
            <p>申请提现金额</p>
        </div>
        <div  id='cash_submit' class="weui-cell__ft"><?php echo ($data["cash_submit"]); ?></div>
    </div>
</div>

<a  href="javascript:cash_submit();" class="weui-btn weui-btn_primary open-popup" data-target="#full">提        现</a>
<div id="full" class='weui-popup__container' >
    <div class="weui-popup__modal" >
        <div class="weui-msg"style="position:fixed;margin-top: 25%">
            <div class="weui-msg__icon-area"><i class="weui-icon-success weui-icon_msg"></i></div>
            <div class="weui-msg__text-area">
                <h2 id='message'  class="weui-msg__title">操作成功</h2>
                <p class="weui-msg__desc">################我们的工作人员会尽快与您取得联系哦################<a href="https://mp.weixin.qq.com/mp/pro
                file_ext?action=home&__biz=MzU1MTE4Njk0NQ==&scene=124#wechat_redirect">筑影学堂</a></p>
            </div>
            <div class="weui-msg__opr-area">
                <p class="weui-btn-area">
                    <a href="javascript:;" class="weui-btn weui-btn_primary close-popup">知道了</a>
                </p>
            </div>

        </div>
    </div>
</div>
<script>
    function cash_submit(){





        console.log($('#cash_submit').html());
        if($('#cash_submit').html()=='0') {
            $('#message').html("操作成功");
            $.ajax({
                type: 'post',
                url: "/tpchat/index.php/Chat/User/cash",
                data: {
                    cash_submit: $('#cash_submit').html(),
                    cash_current: $('#cash_current').html()
                },
                dataType: 'text',
                success: function (data) {
                    console.log(data);
                    if (data) {
                        $('#cash_submit').html(data);
                        $('#cash_current').html('0');
                    }
                    else {

                    }
                }
            });
        }
        else{
            $('#message').html("请您不要着急哦");
        }

    }</script>
</body>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>