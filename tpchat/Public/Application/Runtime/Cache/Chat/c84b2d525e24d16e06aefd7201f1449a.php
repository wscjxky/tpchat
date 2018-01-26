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
    <title>实践课堂</title>
</head>
<script>
    var clickBool=0;
    function sort() {
        var ul = $(".weui-panel__bd");
        var lis = $(".weui-panel__bd a");
        var ux = [];
        for (var i = 0; i < lis.length; i++) {
            var tmp = {};
            tmp.dom = lis.eq(i);

            tmp.date = new Date(lis.eq(i).find("p").eq(1).html());
            ux.push(tmp);
        }
        if(clickBool===0) {
            ux.sort(function (a, b) {
                var myDate = new Date();
                var year = myDate.getYear();
                if (a.date.getYear < year && b.date.getYear == year) {
                    return true;
                }
                return b.date - a.date;
            });
            clickBool=1;
        }
        else{
            ux.sort(function (a, b) {
                var myDate = new Date();
                var year = myDate.getYear();
                if (a.date.getYear < year && b.date.getYear == year) {
                    return true;
                }
                return a.date - b.date;
            });
            clickBool=0;
        }
        $('.weui-panel__bd a').remove();
        //重新填写排序好的内容
        for (var i = 0; i < ux.length; i++) {
            ul.append(ux[i].dom);
        }

    }

</script>
<style>


</style>
<!--background: #f9f9f9;-->
<body ontouchstart >
<div style="margin-bottom: 20%;padding: 11px;" >
    <div class="swiper-container swiper-container-horizontal" style="height: 200px">
                <!-- Additional required wrapper -->
                <div class="swiper-wrapper" style="transform: translate3d(-2468px, 0px, 0px); transition-duration: 0ms;">
                    <!-- Slides -->
                    <?php if(is_array($banner)): $i = 0; $__LIST__ = $banner;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><div class="swiper-slide " data-swiper-slide-index="<?php echo ($i); ?>" ><a href="<?php echo ($v["url"]); ?>"><img src="<?php echo (SHOW_URL); echo ($v["image"]); ?>"/></a>
                        </div><?php endforeach; endif; else: echo "" ;endif; ?>

                </div>                <!-- If we need pagination -->
                <div class="swiper-pagination swiper-pagination-bullets"><span class="swiper-pagination-bullet"></span><span class="swiper-pagination-bullet swiper-pagination-bullet-active"></span><span class="swiper-pagination-bullet"></span></div>
            </div>

            <div style="padding: 8px"><i style="color: #C35B14;font-size: 23px;
            padding: 2px;">实践课程</i>
                <div class="btn-group" style="position:relative;float: right;width:18%;">
                    <button  style="" class="btn btn-default btn-sm dro
                    pdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true"
                            aria-expanded="false" >
                        排序<span class="caret"  ></span>
                    </button>
                    <ul class="dropdown-menu"  style="width: 10px">
                        <li><a href="javascript:sort();">时间</a></li>
                        <li><a href="javascript:;">地点</a></li>
                    </ul>
                </div>
            </div>

                <div class="weui-panel__bd"  >

                    <div>
                        <img src="<?php echo (IMG_URL); ?>/course1.png">
                    </div>
                    <div>
                        <img src="<?php echo (IMG_URL); ?>/course2.png">
                    </div>
                    <div>
                        <img src="<?php echo (IMG_URL); ?>/course3.png">
                    </div>
                </div>
    <div class="weui-loadmore">
        <i class="weui-loading"></i>
        <span class="weui-loadmore__tips">正在加载</span>
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
    var loading = false;
    var index=10;
    loadmore();
    function loadmore() {
        $.ajax({
            type: 'post',
            url: "/tpchat/index.php/Chat/Index/ajaxCourse",
            data: {
                index: index
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

<script src="<?php echo (JS_URL); ?>swiper.js"></script>
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