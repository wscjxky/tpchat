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
    <link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />
    <link href="<?php echo (CSS_URL); ?>center.css" rel="stylesheet" />

</head>
<script>

    $(document).ready(function() {

        $(document).on('click', '#changPhone', function () {
            var config = {
                title: "修改手机号",
                text:'<div class="weui-cell weui-cell_vcode">'+
'<div class="weui-cell__ft"><input type="text" class="weui-input"  placeholder="手机号"/></div></div>'+
' <div class="weui-cell weui-cell_vcode">\n' +
'    <div class="weui-cell__bd">\n' +
'      <input id="inputphone" class="weui-input" type="tel" placeholder="验证码">\n' +
'    </div>\n' +
'    <div class="weui-cell__ft">\n' +
'      <a ><button  class="weui-vcode-btn">获取验证码</button></a>' +
'    </div>\n' +
'  </div>',
                buttons: [
                    {
                        text: "取消",
                        className: "default"
                    },
                    {
                        text: "确定",
                        className: "primary",
                        onClick: function () {
                            $('#phone').text($('#inputphone').val());
                            $.alert('修改成功!');

                        }
                    }

                ],
                autoClose: true //点击按钮自动关闭对话框，如果你不希望点击按钮就关闭对话框，可以把这个设置为false
            };
            $.modal(config);
        });
    });
</script>
<style
    >
    p{
        font-size: 15px;
        text-align: end;
    }
</style>
<body>
<div class="wraper">
    <div class="user-center">
        <div class="center-inner">
            <div class="my-info" >
                <a >
                    <div class="avatar" >
                        <img src="<?php echo ($data["profile"]); ?>">
                    </div></a></div></div></div></div>


<div class="weui-cells weui-cells_form">

    <div class="weui-cell">
        <div class="weui-cell__hd"><label class="weui-label">微信号</label></div>
        <div class="weui-cell__bd">
            <p class="weui-input" type="number" ><?php echo ($data["chatname"]); ?></p>
        </div>
    </div>
    <div class="weui-cell">
        <div class="weui-cell__hd"><label class="weui-label">用户名</label></div>
        <div class="weui-cell__bd">
            <p class="weui-input" type="number"><?php echo ($data["username"]); ?></p>
        </div>
    </div>
    <div class="weui-cell ">
        <div class="weui-cell__hd">
            <label class="weui-label">手机号</label>
        </div>
        <div class="weui-cell__bd">
            <p class="weui-input" type="number" id="phone"><?php echo ($data["phone"]); ?></p>
        </div>
    </div>
    <div class="weui-cell ">
        <div class="weui-cell__hd"><label class="weui-label">地址</label></div>
        <div class="weui-cell__bd">
            <p class="weui-cells_form" type="number"><?php echo ($data["province"]); ?>    <?php echo ($data["city"]); ?></p>
        </div>
    </div>

    <div class="weui-cell">
        <div class="weui-cell__hd"><label class="weui-label">用户级别</label></div>
        <div class="weui-cell__bd">
            <p class="weui-input"><?php echo ($data["user_level"]); ?></p>
        </div>
    </div>

    <div class="weui-cell">
        <div class="weui-cell__hd"><label class="weui-label">账户与安全</label></div>
        <div class="weui-cell__bd">
            <p id="changPhone" class="weui-input">修改手机号</p>
        </div>
    </div>
</div>
</body>
</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>