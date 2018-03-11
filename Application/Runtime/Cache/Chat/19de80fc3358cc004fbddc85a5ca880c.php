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



<html>
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>cart.css">

<body>
<div id="course_id" style="display: none"><?php echo ($data["course_id"]); ?></div>

<div class= "weui-form-preview ">
    <div class= "weui-form-preview__hd ">
        <label class= "weui-form-preview__label ">总   价</label>
        <em class= "weui-form-preview__value " id="totalprice">100</em>
    </div>
    <div class= "weui-form-preview__bd ">
        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label  ">课程名字</label>
            <span class= "weui-form-preview__value " id="course_title"><?php echo ($data["title"]); ?></span>
        </div>


        <div id="count_m" class= "weui-form-preview__item " style="padding-top: 10px;padding-bottom: 10px">
            <label class= "weui-form-preview__label ">报名人数</label>
            <div id = "count_menu" >
                <a class="spcar-decrease spcar-disable"  data-act="dec" onclick="updateFunc(this)">-</a>
                <input type="tel" class="spcar-num"  id='people_count' value="1" />
                <a  class="spcar-increase "  data-act="inc" onclick="updateFunc(this)">+</a>
            </div>

        </div>

        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">课程单价</label>
            <span class= "weui-form-preview__value " id="eachprice"><?php echo ($data["price"]); ?></span>
        </div>

        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">可抵用积分</label>
                     <span class= "weui-form-preview__value " id="bonus">
                         <?php echo ($data["bonus_current"]); ?>
                     </span>
        </div>
        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">已享受折扣</label>
            <span class= "weui-form-preview__value " id="discount">0折</span>
        </div>



        <div class= "weui-form-preview__item ">
            <label class= "weui-form-preview__label ">应付金额</label>
            <span class= "weui-form-preview__value " id='final_price'style="font-size:22px;color: #bf0f0f ;font-weight:bold">100</span>
        </div>
    </div>
    <div class= "weui-form-preview__ft ">
        <a  class= "weui-form-preview__btn weui-form-preview__btn_primary "  id="submit" onclick="submit()">确认订单</a>
    </div>
    <input style="display: none" id="people_remain" value="<?php echo ($people_remain); ?>">
</div>

</body>
<script>
    $(document).ready(function () {
        countPrice();
        if(remain==0){
            $('#count_menu').remove();
            $('#count_m').append('<span class= "weui-form-preview__value " style="color: #bf0f0f">人数已满</span>');
            $('#submit').removeAttr('onclick');
        }
    });
    var discount=0.00;
    var remain=parseInt($('#people_remain').val());

    var eachprice=$('#eachprice').text();
    var count=$('#people_count').val();
    var bonus=$('#bonus').text();
    var final_price=parseInt(eachprice)-parseInt(bonus)+"";

    function countPrice(){
        eachprice=$('#eachprice').text();
        count=parseInt($('#people_count').val());
        bonus=$('#bonus').text();
        if(count>=2&&count<5) {
            discount = 0.98;
            $('#discount').text("98折")
        }
        else if(count>=5&&count<10) {
            discount = 0.95;
            $('#discount').text("95折")

        }

        else if(count>=10&&count<15) {
        discount = 0.9;
            $('#discount').text("9折")

        }else if(count>=15) {
        discount = 0.88;
            $('#discount').text("88折")

        }
        else{
            discount=0;
        }

        if(discount!==0) {
            console.log(discount);
            final_price = (parseInt(eachprice) * parseInt(count)) * discount - parseInt(bonus) + "";
            console.log(parseInt(final_price));
        }
        else
            final_price=(parseInt(eachprice)*parseInt(count))-parseInt(bonus)+"";

        $('#totalprice').text(parseInt(eachprice)*(count)+"");
        console.log(Math.round(final_price*100)/100);
        $('#final_price').text(Math.round(final_price)+"");

    }
    function updateFunc(obj) {
        var act=$(obj).attr('data-act');

        if(act=='dec'&&parseInt( $(obj).next().val())>1){
            $(obj).next().val(parseInt( $(obj).next().val()) -1);
            countPrice()
        }

        else if(act=='inc'&&parseInt( $(obj).prev().val())<remain)
        {
            $(obj).prev().val(parseInt( $(obj).prev().val()) +1);
            countPrice();
        }


    }

    function submit() {
        console.log('a');
        $.ajax({
            type : 'post',
            url : "/tpchat/index.php/Chat/Index/trade",
            data : {
                people_count:count,
                user_discount:discount,
                user_bonus:bonus,
                course_title:$('#course_title').text(),
                course_price:$('#eachprice').text(),
                total_price:$('#totalprice').text(),
                final_price:$('#final_price').text(),
                course_id:$('#course_id').text()

            },
            dataType : 'text',
            async:false,
            success : function(data){
                console.log(data);
                if(data) {
                    console.log('data'+data);
                    console.log($('#eachprice').text());
                    if($('#eachprice').text()=='0'){
                        $.alert({
                            title: '成功',
                            text: '恭喜您成功报名本次0元试听活动',
                            onOK: function () {
                                window.location.href='https://www.jianpianzi.com/tpchat/index.php/Chat/user/tradeinfo?trade_id='+data;
                            }
                        });

                    }
                    else{
                        window.location.href='https://www.jianpianzi.com/tpchat/index.php/home/jspay?trade_id='+data;
                    }
                }else{
                    console.log(data);
                }
            }

        });


    }



</script>

</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>