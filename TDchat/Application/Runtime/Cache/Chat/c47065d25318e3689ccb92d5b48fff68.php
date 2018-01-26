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
    <title>实践课堂</title>
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=DXzAydHPMSoI3jr04QHlOnriSReOMq9q"></script>

</head>
<script>$(document).ready(function() {
    //绑定下拉框change事件，当下来框改变时调用 SelectChange()方法
    $("select").change(function() {
        $type=$("select").find("option:selected").val();
        if($type=="address"){
            window.location.href="/tpchat/index.php/Chat/Index/sortcourse?type=address&x="+x+"&y="+y;
        }
        else {
            window.location.href="/tpchat/index.php/Chat/Index/sortcourse?type=starttime";
        }
    });
});
</script>
<style>
    .course_title{
        font-weight: bold;
        font-size: 15px;
        overflow: hidden;

    }
    .weui-media-box__desc{
        margin-top: 4px;
        font-weight: normal;
    }
    .weui-media-box__bd{
        margin-left: 16px;
    }
    .weui-media-box__desc_time{
        font-weight:bold!important;
        text-align: end;
        color: #C35B14;
        padding-right:18px;
        padding-left:18px;
        background-color: #E0E0E0;
        border-radius:10px;
        -webkit-border-radius:10px;
        -moz-border-radius :10px;

    }
    .weui-media-box_appmsg{
        margin-top: 10px;
        margin-bottom: 12px;
    }
    select{
        border-radius:15px;
        -webkit-border-radius:15px;
        -moz-border-radius :15px;
        height: 21px;
        width: auto;
        padding: 0 2%;
        margin: 0;
        color:white;
        font-size: 13px;
        text-align: center;
        margin-top: 2%;

        /*在选择框的最右侧中间显示小箭头图片*/
        background: -webkit-linear-gradient(left, #ffc931 , #fa6f6c); /* Safari 5.1 - 6.0 */
        background: -o-linear-gradient(right, #ffc931, #fa6f6c); /* Opera 11.1 - 12.0 */
        background: -moz-linear-gradient(right, #ffc931, #fa6f6c); /* Firefox 3.6 - 15 */
        background: linear-gradient(to right, #ffc931 , #fa6f6c); /* 标准的语法 */

        /*为下拉小箭头留出一点位置，避免被文字覆盖*/
        padding-right: 10px;
    }
    option{
        text-align:center;
    }

    /*清除ie的默认选择框样式清除，隐藏下拉箭头*/
    select::-ms-expand { display: none; }

    /* Default custom select styles */
    div.cs-select {
        display: inline-block;
        vertical-align: middle;
        position: relative;
        text-align: right;
        background: #fff;
        color: white;
        z-index: 100;
        width: 100%;
        max-width: 500px;
        font-weight: normal;


    }

    div.cs-select:focus {
        outline: none; /* For better accessibility add a style for this in your skin */
    }


    .cs-select span {
        display: block;
        position: relative;
        cursor: pointer;
        padding: 1em;
        white-space: nowrap;
        overflow: hidden;

        text-overflow: ellipsis;
        text-align: right;

    }

    /* Placeholder and selected option */
    .cs-select > span {

        padding-right: 3em;
    }

    .cs-select > span::after,
    .cs-select .cs-selected span::after {

        speak: none;
        position: absolute;
        top: 50%;
        -webkit-transform: translateY(-50%);
        transform: translateY(-50%);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .cs-select > span::after {

        content: '\25BE';
        right: 1em;
    }

    .cs-select .cs-selected span::after {
        content: '\2713';
        margin-left: 1em;
    }

    .cs-select.cs-active > span::after {
        -webkit-transform: translateY(-50%) rotate(180deg);
        transform: translateY(-50%) rotate(180deg);
    }

    /* Options */
    .cs-select .cs-options {
        position: absolute;
        overflow: hidden;
        width: 100%;
        background: #fff;
        visibility: hidden;
    }

    .cs-select.cs-active .cs-options {
        visibility: visible;
    }

    .cs-select ul {

        list-style: none;
        margin: 0;
        padding: 0;
        width: 100%;
    }

    .cs-select ul span {

        padding: 1em;
    }

    .cs-select ul li.cs-focus span {
        background-color: #ddd;
    }

    /* Optgroup and optgroup label */
    .cs-select li.cs-optgroup ul {
        padding-left: 1em;
    }

    .cs-select li.cs-optgroup > span {
        cursor: default;
    }

</style>
<body>
<div id="map" style="display: none"></div>

<div style="padding: 7px;padding-bottom: 18%;" >
    <div class="swiper-container swiper-container-horizontal" style="height: 200px;margin-bottom: 8%">
        <!-- Additional required wrapper -->
        <div class="swiper-wrapper" style="transform: translate3d(-2468px, 0px, 0px); transition-duration: 0ms;">
            <!-- Slides -->
            <?php if(is_array($banner)): $i = 0; $__LIST__ = $banner;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><div class="swiper-slide " data-swiper-slide-index="<?php echo ($i); ?>" ><a href="<?php echo ($v["url"]); ?>"><img src="<?php echo (SHOW_URL); echo ($v["image"]); ?>"/></a>
                </div><?php endforeach; endif; else: echo "" ;endif; ?>

        </div>                <!-- If we need pagination -->

    </div>

    <div style="padding: 8px"><i style="color: #ff5d01;font-size: 20px;font-weight: bold;padding: 2px;">实践课程</i>
        <select  style="float: right" class="cs-select cs-skin-elastic">
            <option value="address">地点</option>

            <option value="starttime" >时间</option>

        </select>
    </div>





    <div class="weui-panel__bd" >
        <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><div  class="weui-media-box weui-media-box_appmsg"style='padding: 5px'>
            <img style='width: 90px;height: 62px;vertical-align: top;margin-bottom: 15px'  src="
                 {Think.const.SHOW_URL}<?php echo ($v["image"]); ?>">
            <div class="weui-media-box__bd">
                <a  href='Chat/index/course?courseid=<?php echo ($v["course_id"]); ?>' class='course_title'>
                    <?php echo ($v["title"]); ?></a>

                <p class="weui-media-box__desc"  >
                    <?php echo ($v["starttime"]); ?></p>

                <p class='weui-media-box__desc' >
                    <?php echo ($v["address"]); ?></p>

                <p style='text-align: end'><i class='weui-media-box__desc_time'> ¥<?php echo ($v["price"]); ?></i>
                </p>

            </div>
            </div><?php endforeach; endif; else: echo "" ;endif; ?>
    </div>

</div>

</body >
<!-- body 最后 -->
<style>
    a{

        margin: 0 auto;
    }


</style>
<div class="weui-tabbar" style="text-align: center;
position:fixed ;background:url('http://www.jianpianzi.com/tpchat/Public/img/nav_bar.png')" >
    <a href="/tpchat/index.php/Chat">

        <img  src="<?php echo (IMG_URL); ?>nav_index.png" alt="">

    </a>
    <a href="/tpchat/index.php/Chat/log"   >

        <img  src="<?php echo (IMG_URL); ?>nav_message.png" alt="">
    </a>
    <a href="/tpchat/index.php/Chat/user" >

        <img  src="<?php echo (IMG_URL); ?>nav_user.png" alt="">

    </a>

</div>

<script src="<?php echo (JS_URL); ?>jquery.js"></script>
<script src="<?php echo (JS_URL); ?>jquery-weui.min.js"></script>
<script>
    var map = new BMap.Map('map');
    //单击获取点击的经纬度

    var point = new BMap.Point(116.424822,39.914492);
    map.centerAndZoom(point,12);

    var geolocation = new BMap.Geolocation();
    var x,y;
    geolocation.getCurrentPosition(function(r){
        if(this.getStatus() == BMAP_STATUS_SUCCESS){
            var mk = new BMap.Marker(r.point);
            map.addOverlay(mk);
            map.panTo(r.point);
            x=r.point.lng;
            y=r.point.lat;
        }
        else {
            alert('failed'+this.getStatus());
        }
    },{enableHighAccuracy: true})
</script>

<script src="<?php echo (JS_URL); ?>swiper.js"></script>
<script>     $(".swiper-container").swiper({
    loop: true,
    autoplay: 4000
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