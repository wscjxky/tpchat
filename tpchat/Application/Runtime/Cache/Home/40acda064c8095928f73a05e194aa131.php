<?php if (!defined('THINK_PATH')) exit();?><html>
<meta http-equiv="content-type" content="text/html;charset=utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>筑影学堂</title>

<link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">

<script src="<?php echo (JS_URL); ?>jquery.js"></script>
<script>



</script>
<script>
</script>
<body>


<div class= "weui-form-preview ">
  
    <div class= "weui-form-preview__bd ">
        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">课程名字</label>
            <span class= "weui-form-preview__value "><?php echo ($data["course_title"]); ?></span>
        </div>


        <div class= "weui-form-preview__item " style="padding-top: 10px;padding-bottom: 10px">
            <label class= "weui-form-preview__label ">报名人数</label>
            <span class= "weui-form-preview__value " ><?php echo ($data["people_count"]); ?></span>
        </div>

        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">课程单价</label>
            <span class= "weui-form-preview__value " id="eachprice"><?php echo ($data["course_price"]); ?></span>
        </div>

        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">节省金额</label>
            <span class= "weui-form-preview__value " id="bonus"><?php echo ($data["cheap_price"]); ?></span>
        </div>



        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">应付金额</label>
            <span class= "weui-form-preview__value " style="font-size:22px;color: #bf0f0f ;font-weight:bold"><?php echo ($data["final_price"]); ?></span>
        </div>
    </div>
    <div class= "weui-form-preview__ft ">
        <a  class= "weui-form-preview__btn weui-form-preview__btn_primary " href= "javascript:callpay()">立即支付</a>
    </div>
</div>
</body>