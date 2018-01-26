<?php if (!defined('THINK_PATH')) exit();?><meta http-equiv="content-type" content="text/html;charset=utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>微信支付样例-支付</title>

<link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>cart.css">

<script src="<?php echo (JS_URL); ?>jquery.js"></script>
<script>
    function countPrice(){
        var eachprice=$('#eachprice').text();
        var count=$('#people_count').val();
        var bonus=$('#bonus').text();
        $('#totalprice').text(parseInt(eachprice)*parseInt(count)+"");
        $('#final_price').text(parseInt(eachprice)*parseInt(count)-parseInt(bonus)+"");
        console.log(parseInt(bonus));

    }
    function updateFunc(obj) {
        var act=$(obj).attr('data-act');
        if(act=='dec'&&parseInt( $(obj).next().val())>1){
            $(obj).next().val(parseInt( $(obj).next().val()) -1);
            countPrice()
        }
        else if(act=='inc'&&parseInt( $(obj).prev().val())<50)
        {
            $(obj).prev().val(parseInt( $(obj).prev().val()) +1);
            countPrice();
        }


    }


</script>
<script>
</script>
<body>


<div class= "weui-form-preview ">
    <div class= "weui-form-preview__hd ">
        <label class= "weui-form-preview__label ">总   价</label>
        <em class= "weui-form-preview__value " id="totalprice" >100</em>
    </div>
    <div class= "weui-form-preview__bd ">
        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">课程名字</label>
            <span class= "weui-form-preview__value "><?php echo ($data["title"]); ?></span>
        </div>
        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">课程子标题</label>
            <span class= "weui-form-preview__value ">名字名字名字</span>
        </div>

        <div class= "weui-form-preview__item " style="padding-top: 10px;padding-bottom: 10px">
            <label class= "weui-form-preview__label ">报名人数</label>
            <a class="spcar-decrease spcar-disable"  data-act="dec" onclick="updateFunc(this)">-</a>
            <input type="tel" class="spcar-num"  id='people_count'value="1" />
            <a  class="spcar-increase "  data-act="inc" onclick="updateFunc(this)">+</a>        </div>

        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">课程单价</label>
            <span class= "weui-form-preview__value " id="eachprice"><?php echo ($data["price"]); ?></span>
        </div>

        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">可抵用积分</label>
            <span class= "weui-form-preview__value " id="bonus">100</span>
        </div>



        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">应付金额</label>
            <span class= "weui-form-preview__value " id="final_price">100</span>
        </div>
    </div>
    <div class= "weui-form-preview__ft ">
        <a class= "weui-form-preview__btn weui-form-preview__btn_default " href= "javascript: ">操作</a>
        <a  class= "weui-form-preview__btn weui-form-preview__btn_primary " onclick="callpay()">立即支付</a>
    </div>
</div>

</body>