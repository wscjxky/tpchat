<?php if (!defined('THINK_PATH')) exit();?><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>

<link href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">

<script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

<link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />

<link rel="stylesheet" href="https://cdn.bootcss.com/weui/1.1.2/style/weui.min.css">
<link rel="stylesheet" href="https://cdn.bootcss.com/jquery-weui/1.2.0/css/jquery-weui.min.css">

<!-- body 最后 -->
<script src="https://cdn.bootcss.com/jquery/1.11.0/jquery.min.js"></script>
<script src="https://cdn.bootcss.com/jquery-weui/1.2.0/js/jquery-weui.min.js"></script>

<!-- 如果使用了某些拓展插件还需要额外的JS -->
<script src="https://cdn.bootcss.com/jquery-weui/1.2.0/js/swiper.min.js"></script>
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
    <title>我的校外课</title>
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=DXzAydHPMSoI3jr04QHlOnriSReOMq9q"></script>

</head>
<style>
    body{
        font-size: 12px;
    }
</style>
<script>


//    function sort() {
//        var ul = $(".weui-panel__bd");
//        var lis = $(".weui-panel__bd div");
//        var ux = [];
//        for (var i = 0; i < lis.length; i++) {
//            var tmp = {};
//            tmp.dom = lis.eq(i);
//
//            tmp.date = new Date(lis.eq(i).find("p").eq(1).html());
//            ux.push(tmp);
//        }
//        if(clickBool===0) {
//            ux.sort(function (a, b) {
//                var myDate = new Date();
//                var year = myDate.getYear();
//                if (a.date.getYear < year && b.date.getYear == year) {
//                    return true;
//                }
//                return b.date - a.date;
//            });
//            clickBool=1;
//        }
//        else{
//            ux.sort(function (a, b) {
//                var myDate = new Date();
//                var year = myDate.getYear();
//                if (a.date.getYear < year && b.date.getYear == year) {
//                    return true;
//                }
//                return a.date - b.date;
//            });
//            clickBool=0;
//        }
//        $('.weui-panel__bd div').remove();
//        //重新填写排序好的内容
//        for (var i = 0; i < ux.length; i++) {
//            ul.append(ux[i].dom);
//        }
//
//    }

    $(document).ready(function() {
//        $.ajax({
//            type: 'post',
//            url: "/tpchat_git/index.php/Chat/Index/sortcourse",
//            data: {
//                type: 'address',
//                x: x,
//                y: y
//            },
//            dataType: 'json',
//            success: function (data) {
//                if (data.status == 'finish') {
//                    $('.weui-panel__bd').html(data.data);
//                    console.log(data);
//                }
//            }
//        });

        //绑定下拉框change事件，当下来框改变时调用 SelectChange()方法
        $(".select_address").change(function() {
                console.log(x + y);
                var type = $("select").find("option:selected").val();
            console.log(type);
            console.log($(".select_category").val());

            if (type == "address") {

                $.ajax({
                        type: 'post',
                        url: "/tpchat_git/index.php/Chat/Index/sortcourse",
                        data: {
                            type: 'address',
                            category_name:$(".select_category").val(),
                            big_category:big_category,
                            x: x,
                            y: y
                        },
                        dataType: 'json',
                        success: function (data) {
                            if (data.status == 'finish') {
                                $('.weui-panel__bd').html(data.data);
                                console.log(data);
                            }
                        }
                    });

//                window.location.href="/tpchat_git/index.php/Chat/Index/sortcourse?type=address&x="+x+"&y="+y;
                }
                else{
                    $.ajax({
                        type: 'post',
                        url: "/tpchat_git/index.php/Chat/Index/sortcourse",
                        data: {
                            category_name:$(".select_category").val(),
                            big_category:big_category,

                            type: 'starttime'
                        },
                        dataType: 'json',
                        success: function (data) {
                            if (data.status == 'finish') {
                                $('.weui-panel__bd').html(data.data);
                                console.log(data.data);

                                return;
                            }
                        }
                    });
                }

        });


        $(".select_category").change(function() {
            console.log($(this).val());
                $.ajax({
                    type: 'post',
                    url: "/tpchat_git/index.php/Chat/Index/sortCategory",
                    data: {
                        category_name:$(this).val(),
                        big_category:big_category,

                    },
                    dataType: 'json',
                    success: function (data) {
                        $('.weui-panel__bd').html(data.data);
                    }
                });

            });

    });

</script>
<style>
    a:link {
        text-decoration: none;
    }
    .hiden{
        visibility: hidden;
    }
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
        padding:2px 18px 3px 18px;
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
        border-radius:0;
        -webkit-border-radius:0;
        height: 26px;
        width: auto;
        padding: 0 2%;
        margin: 0;
        color:#999;
        font-size: 13px;
        text-align: center;
        margin-top: 2%;

        /*在选择框的最右侧中间显示小箭头图片*/


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

    .tabimage{
        height: 25px;
        width: auto;

    }
    .weui-navbar{
        text-align:center;
        position: initial;
        border:1px solid #eb7537;
        height:auto;
        width:100%;
        color: #eb7537;
        border-radius:25px;
        -moz-border-radius:25px; /* 老的 Firefox */
    }
    .weui-navbar__item{
        padding:5px 0 5px 0;
        color: #eb7537;
        position: initial;

    }
    .weui-navbar__item.weui-bar__item--on{
        -webkit-border-radius:20px;
        -moz-border-radius :20px;
        background-color: #eb7537;;
        color: white;
    }
    .weui-navbar+.weui-tab__bd{
        padding-top: 6px!important;
    }

</style>

<!--background: #f9f9f9;-->
<body ontouchstart >
<div id="map" style="display: none"></div>
<div style="padding: 7px;padding-bottom: 18%;" >
    <div class="swiper-container swiper-container-horizontal" style="height: 200px;margin-bottom:0.5% ">
                <!-- Additional required wrapper -->
                <div class="swiper-wrapper" style="transform: translate3d(-2468px, 0px, 0px); transition-duration: 0ms;">
                    <!-- Slides -->
                    <?php if(is_array($banner)): $i = 0; $__LIST__ = $banner;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><div class="swiper-slide " data-swiper-slide-index="<?php echo ($i); ?>" ><a href="<?php echo ($v["url"]); ?>"><img src="<?php echo (SHOW_URL); echo ($v["image"]); ?>"/></a>
                        </div><?php endforeach; endif; else: echo "" ;endif; ?>

                </div>
            </div>
                <!--<div class="btn-group" style="position:relative;float: right;width:18%;">-->
                    <!--<button  style="" class="btn btn-default btn-sm dro-->
                    <!--pdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true"-->
                            <!--aria-expanded="false" >-->
                        <!--排序<span class="caret"  ></span>-->
                    <!--</button>-->
                    <!--<ul class="dropdown-menu"  style="width: 10px">-->
                        <!--<li><a href="javascript:sort();">时间</a></li>-->
                        <!--<li><a href="javascript:;">地点</a></li>-->
                    <!--</ul>-->
                <!--</div>-->
            <!--</div>-->

    <div class="weui-tab">
        <div class="weui-navbar">
            <div class="weui-navbar__item weui-bar__item--on" href="#tab1">
                <img class="tabimage" src="<?php echo (IMG_URL); ?>speech_down.png">
                    <span>专题活动</span>

            </div>
            <div class="weui-navbar__item" href="#tab2">
                <img class="tabimage" src="<?php echo (IMG_URL); ?>class_nor.png">
                    <span>实践课程</span>


            </div>
            <div class="weui-navbar__item" href="#tab3">
                <img class="tabimage" src="<?php echo (IMG_URL); ?>activity_nor.png">
                    <span>游历游学</span>
            </div>

        </div>
        <div class="weui-tab__bd">
            <div id="tab1" class="weui-tab__bd-item weui-tab__bd-item--active">
                <div >
                    <i class="hiden"  style="color: #ff5d01;font-size: 20px;font-weight: bold;padding: 2px;">筑影学堂</i>
                    <div style="float: right;padding-top: 5px;width:30%;margin-right: 4%">
                        <select class="select_address"  style="float: right" class="cs-select cs-skin-elastic">
                            <option value="address">地点最近</option>
                            <option value="starttime" >时间最新</option>

                        </select>


                    </div>

                    <div style="float: right;padding-top: 5px;width:28%;">
                        <select class="select_category" style="float: right" class="cs-select cs-skin-elastic">
                            <option value="">所有类型</option>
                            <?php if(is_array($small_category)): $i = 0; $__LIST__ = $small_category;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><option value="<?php echo ($v["category_name"]); ?>"><?php echo ($v["category_name"]); ?></option><?php endforeach; endif; else: echo "" ;endif; ?>
                            </select>
                    </div>


                </div>

                <div class="weui-panel__bd" >
                </div>
                <!--<div class="weui-loadmore">-->
                    <!--<i class="weui-loading"></i>-->
                    <!--<span class="weui-loadmore__tips">正在加载</span>-->
                <!--</div>-->
            </div>

            <div id="tab2" class="weui-tab__bd-item">
                <div style="">
                    <i class="hiden" style="color: #ff5d01;font-size: 20px;font-weight: bold;padding: 2px;">筑影学堂</i>
                    <div style="float: right;padding-top: 5px;width:30%;margin-right: 4%">
                        <select class="select_address"  style="float: right" class="cs-select cs-skin-elastic">
                            <option value="address">地点最近</option>
                            <option value="starttime" >时间最新</option>

                        </select>


                    </div>

                    <div style="float: right;padding-top: 5px;width:28%;">
                        <select class="select_category" style="float: right" class="cs-select cs-skin-elastic">
                            <option value="">所有类型</option>
                            <?php if(is_array($small_category)): $i = 0; $__LIST__ = $small_category;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><option value="<?php echo ($v["category_name"]); ?>"><?php echo ($v["category_name"]); ?></option><?php endforeach; endif; else: echo "" ;endif; ?>
                        </select>
                    </div>
                </div>
                <div class="weui-panel__bd" ></div>
            </div>

            <div id="tab3" class="weui-tab__bd-item">
                <div style="">
                    <i class="hiden"  style="color: #ff5d01;font-size: 20px;font-weight: bold;padding: 2px;">筑影学堂</i>
                    <div style="float: right;padding-top: 5px;width:30%;margin-right: 4%">
                        <select class="select_address"  style="float: right" class="cs-select cs-skin-elastic">
                            <option value="address">地点最近</option>
                            <option value="starttime" >时间最新</option>

                        </select>


                    </div>

                    <div style="float: right;padding-top: 5px;width:28%;">
                        <select class="select_category" style="float: right" class="cs-select cs-skin-elastic">
                            <option value="">所有类型</option>
                            <?php if(is_array($small_category)): $i = 0; $__LIST__ = $small_category;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><option value="<?php echo ($v["category_name"]); ?>"><?php echo ($v["category_name"]); ?></option><?php endforeach; endif; else: echo "" ;endif; ?>
                        </select>
                    </div>


                </div>
                <div class="weui-panel__bd" ></div>

            </div>
        </div>
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
position:fixed ;background:url('https://www.jianpianzi.com/tpchat/Public/img/nav_bar.png')" >
    <a href="/tpchat_git/index.php/Chat">

        <img  src="<?php echo (IMG_URL); ?>nav_index.png" alt="">

    </a>
    <a href="/tpchat_git/index.php/Chat/log"   >

        <img  src="<?php echo (IMG_URL); ?>nav_message.png" alt="">
    </a>
    <a href="/tpchat_git/index.php/Chat/user" >

        <img  src="<?php echo (IMG_URL); ?>nav_user.png" alt="">

    </a>

</div>


<script>
    //点击函数执行结束之后再会发生active的切换
    var big_category="专题活动";

    $(document).ready(function(){
        $(".weui-navbar__item").click(function(){
            console.log($(this).children('img').attr('src'));

            //根据大类加载数据
            var tab=$(this).attr('href');
            console.log(tab);
            if(tab.indexOf('1')>=0){
                big_category="专题活动";
                loadmore(big_category);
            }
            else if(tab.indexOf('2')>=0){
                big_category="实践课程";
                loadmore(big_category);

            }
            else{
                big_category="游历游学";
                loadmore(big_category);

            }
            console.log(big_category);

            //重置select
            $(".select_address").val("address");
            $(".select_category").val("");

            //改变当前点击的按钮
            var curr_image=$(this).children('img');
            var curr_image_src=curr_image.attr('src');
            curr_image.attr('src',curr_image_src.replace('nor','down'));
            //改变之前点击的按钮
            var before_image=$(".weui-navbar__item.weui-bar__item--on").children('img');
            var before_image_src=before_image.attr('src');
            before_image.attr('src',before_image_src.replace('down','nor'));
//            $(".weui-navbar__item").each(function(){
//                console.log($(this).hasClass('weui-bar__item--on'));
//                if(!$(this).hasClass('weui-bar__item--on')){
//                    console.log($(this).children('img').attr('src'));
//                    $(this).children('img').attr('src',curr_image_src.replace('down','nor'));
//                }
//            });


        });
    });
</script>

<script>
    var map = new BMap.Map('map');
    //单击获取点击的经纬度
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
<script>
    var loading = false;
    var index=10;
    loadmore("专题活动");

    function loadmore($big_category) {
        $.ajax({
            type: 'post',
            url: "/tpchat_git/index.php/Chat/Index/ajaxCourse",
            data: {
//                index: index,
                index:30,
                big_category:$big_category
            },
            dataType: 'json',
            success: function (data) {
                if(data.status=='finish'){
                    $('.weui-panel__bd').html(data.data);
                    $(document.body).destroyInfinite();
                    $(".weui-loadmore").hide();
                    return;
                }
                console.log(data.data);
                $('.weui-panel__bd').html(data.data);
                index+=20;
                loading = false;
            }
        });
    }

    $(document.body).infinite().on("infinite", function() {
        console.log('s');
        if(loading) return;
        loading = true;
//        loadmore();

    });
</script>

<script>     $(".swiper-container").swiper({
    loop: true,
    autoplay: 4000
});
</script>

</html>

<title>筑影学堂</title>
<script>
    $(function() {
        FastClick.attach(document.body);
    });
</script>