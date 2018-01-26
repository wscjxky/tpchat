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
</head>
<style>
    .weui-cell{
        position:relative !important;
    }
</style>
<body>
<!--<div class="page-title"  >-->
    <!--<h2>填写信息<a href="javascript:history.go(-1)" style="top: 30%;" class="arrow-left backpage"></a></h2>-->
<!--</div>-->
<iframe name="iframe" style="display: none"></iframe>
<form  class="weui-cells weui-cells_form"  method="post"   action="" target="iframe" style="margin-top:15%">
    <div class="weui-cell">
        <div class="weui-cell__hd"><label class="weui-label" style="margin-top: 5px">用户名：</label></div>
        <div class="weui-cell__bd">
        <input  value="<?php echo ($username); ?>" name="username" id="video_title"  type="text" />
    </div>
    </div>

    <div class="weui-cell weui-cell_vcode">
        <div class="weui-cell__hd">
            <label class="weui-label">手机号</label>
        </div>
        <div class="weui-cell__bd">
            <input name='phone' id='phone' class="weui-input" type="tel" placeholder="请输入手机号">
        </div>
        <div class="weui-cell__ft">
            <a class="weui-vcode-btn">获取验证码</a>
        </div>
    </div>

    <div class="weui-cell">
        <div class="weui-cell__hd"><label class="weui-label" style="margin-top: 5px">验证码：</label></div>
        <div class="weui-cell__bd">
            <input  value="<?php echo ($code); ?>" name="code" id="code"  type="text" />
        </div>
    </div>


    <input style="display: none" name="user_id" value="<?php echo ($user_id); ?>">

<a class="weui-btn weui-btn_primary"  id="submit"  onclick="submit()">确定</a>
</form>

<!-- 将form表单提交的窗口指向隐藏的ifrmae,并通过ifrmae提交数据。 -->

</body>
<script>
    function submit() {
        if($('#code').val()==null||''){
            $.alert({
                title: '请填写完整'
            });
        }
        else{
            $.ajax({
                type: 'post',
                url: "/tpchat/index.php/Chat/Index/enroll",
                data: {
                    phone:$('#phone').val(),
                    code:$('#code').val()
                },
                dataType: 'text',
                async: false,
                success: function (data) {
                    if(data=='error'){
                        $.alert({
                            title: '失败',
                            text: '验证码错误'

                        });
                    }
                    if (data) {
                        console.log('data' + data);
                        $.alert({
                            title: '成功',
                            text: '恭喜您成功报名本次0元试听活动',
                            onOK: function () {
                                window.location.href = '/tpchat/index.php/Chat/user/tradeinfo?trade_id=' + data;
                            }
                        });
                    }

                }
            });
        }


    }
    function checkmobile() {
        var sMobile = $('#phone').val();
        var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;
        if (!myreg.test(sMobile)) {
            $.alert({
                text: "不是完整的11位手机号或者正确的手机号前七位"});
            return false;
        }
        else {

            return true;
        }
    }

    $(document).ready(function () {
        $(".weui-vcode-btn").click(function () {
            if(checkmobile()) {

                console.log('c'+$('#phone').val());
                $(this).unbind();


                $.ajax({
                    type: 'post',
                    url: "/tpchat/index.php/Chat/Index/enroll",
                    data: {
                        phone:$('#phone').val(),

                        req_code: 1
                    },
                    dataType: 'text',
                    async: false,
                    success: function (data) {
                        if (data) {
                            console.log('data' + data);
                            $('#code').val(data);

                        }

                    }
                });
            }
        });



    });
</script>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>