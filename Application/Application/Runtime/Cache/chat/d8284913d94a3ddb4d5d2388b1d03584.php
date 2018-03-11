<?php if (!defined('THINK_PATH')) exit();?>
<html lang="en">
<head>
    <title>活动推送</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <link href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

    <link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />
    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
    <script src="<?php echo (JS_URL); ?>jquery-weui.js"></script>
    <script src="<?php echo (JS_URL); ?>fastclick.js"></script>
    <meta charset="UTF-8">
    <title>消息</title>
</head>
<html lang="en">
<script>
    $(document).ready(function () {
        $('.weui-media-box').remove().sort(function(a,b) {
//排序，按照指定的规则,a-b来对标签进行排序
            var price1=$(a).find('p').next().next().text().substring(5,15);
            var price2=$(b).find('p').next().next().text().substring(5,15);
            return price1 < price2 ? 1 : -1;
        } ).each( function(i,e) {
//按照规则继续添加li
            $( '.weui-panel__bd' ).append( e );
        } );
    });

</script>

<body ontouchstart>


</div>
<div style="margin-bottom: 20%">
    <?php if($course != '' ): ?><div class="weui-panel__bd weui-panel_access"  >
            <div class="weui-panel__hd">最新活动</div>
            <?php if(is_array($course)): $i = 0; $__LIST__ = $course;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i; if($v["is_activity"] == 1): ?><a href="/tpchat/index.php/Chat/Index/course?courseid=<?php echo ($v["course_id"]); ?>" class="weui-media-box weui-media-box_appmsg">
                    <img  src="<?php echo (SHOW_URL); echo ($v["image"]); ?>" style="width: 40px;height: 40px;margin-bottom: 5% ">
                    <div class="weui-media-box__bd" style="margin-left: 5px">
                        <p class="weui-media-box__desc" style="font-weight:bold"><?php echo ($v["title"]); ?></p>
                        <p class="weui-media-box__desc" style="margin-top: 5px ;margin-bottom: 5px"><?php echo ($v["desc"]); ?></p>
                        <p class="weui-media-box__desc">活动时间：<?php echo ($v["starttime"]); ?></p>
                    </div>
                    </a><?php endif; endforeach; endif; else: echo "" ;endif; ?>
            <?php if(is_array($article)): $i = 0; $__LIST__ = $article;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i; if($v["is_activity"] == 1): ?><a href="<?php echo ($v["url"]); ?>" class="weui-media-box weui-media-box_appmsg">
                        <img  src="<?php echo (SHOW_URL); echo ($v["image"]); ?>" style="width: 40px;height: 40px;margin-bottom: 5% ">
                        <div class="weui-media-box__bd" style="margin-left: 5px">
                            <p class="weui-media-box__desc" style="font-weight:bold"><?php echo ($v["title"]); ?></p>
                            <p class="weui-media-box__desc" style="margin-top: 5px ;margin-bottom: 5px"><?php echo ($v["desc"]); ?></p>
                            <p class="weui-media-box__desc">活动时间：<?php echo ($v["createtime"]); ?></p>
                        </div>
                    </a><?php endif; endforeach; endif; else: echo "" ;endif; ?>
            <?php if($activity != ''): if(is_array($activity)): $i = 0; $__LIST__ = $activity;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i; if($v["publish_state"] == 1 ): ?><a href="/tpchat/index.php/Chat/Product/activity?title=<?php echo ($v["title"]); ?>" class="weui-media-box weui-media-box_appmsg">
                                <img  src="<?php echo (SHOW_URL); echo ($v["activity_image"]); ?>" style="width: 40px;height: 40px;margin-bottom: 5% ">
                                <div class="weui-media-box__bd" style="margin-left: 5px">
                                    <p class="weui-media-box__desc" style="font-weight:bold"><?php echo ($v["title"]); ?></p>
                                    <p class="weui-media-box__desc" style="margin-top: 5px ;margin-bottom: 5px"><?php echo ($v["content"]); ?></p>
                                    <!--<p class="weui-media-box__desc">活动时间：<?php echo ($v["starttime"]); ?>&nbsp-&nbsp<?php echo ($v["endtime"]); ?></p>-->
                                    <p class="weui-media-box__desc">活动时间：<?php echo ($v["createtime"]); ?></p>
                                </div>
                            </a><?php endif; endforeach; endif; else: echo "" ;endif; endif; ?>
            <!--<?php if(is_array($video)): $i = 0; $__LIST__ = $video;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?>-->
                    <!--<a href="/tpchat/index.php/Chat/Product/video?video_id=<?php echo ($v["video_id"]); ?>" class="weui-media-box weui-media-box_appmsg">-->
                        <!--<img  src="<?php echo (SHOW_URL); echo ($v["image"]); ?>" style="width: 40px;height: 40px;margin-bottom: 5% ">-->
                        <!--<div class="weui-media-box__bd" style="margin-left: 5px">-->
                            <!--<p class="weui-media-box__desc" style="font-weight:bold"><?php echo ($v["video_title"]); ?></p>-->
                            <!--<p class="weui-media-box__desc" style="margin-top: 5px ;margin-bottom: 5px"><?php echo ($v["admin_desc"]); ?></p>-->
                            <!--<p class="weui-media-box__desc">活动时间：<?php echo ($v["confirm_time"]); ?></p>-->
                        <!--</div>-->
                    <!--</a>-->
            <!--<?php endforeach; endif; else: echo "" ;endif; ?>-->
        </div><?php endif; ?>


    <!--<div class="weui-panel__bd weui-panel_access"  >-->
        <!--<?php if($activity != ''): ?>-->
            <!--<div class="weui-panel__hd">作品集锦</div>-->
        <!--<?php endif; ?>-->
        <!--<?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?>-->
            <!--<?php if($v["publish_state"] == 1 ): ?>-->
                <!--<a href="/tpchat/index.php/Chat/Product/video?video_id=<?php echo ($v["video_id"]); ?>" class="weui-media-box weui-media-box_appmsg">-->
                    <!--<img  src="<?php echo ($v["profile"]); ?>" style="width: 40px;height: 40px; margin-bottom: 60%">-->
                    <!--<div class="weui-media-box__bd" style="margin-left: 5px">-->
                        <!--<p class="weui-media-box__desc" style="font-weight:bold"><?php echo ($v["chatname"]); ?></p>-->
                        <!--<p class="weui-media-box__desc" style="margin-top: 5px ;margin-bottom: 5px"><?php echo ($v["admin_desc"]); ?></p>-->
                        <!--<p class="weui-media-box__desc"><?php echo ($v["content"]); ?></p>-->
                        <!--<img src="<?php echo (SHOW_URL); echo ($v["image"]); ?>" style="max-width: 200px;max-height: 200px">-->
                        <!--<p  style="margin-top: 5px" class="weui-media-box__desc"><?php echo ($v["createtime"]); ?></p>-->
                    <!--</div>-->
                <!--</a>-->
            <!--<?php endif; ?>-->
        <!--<?php endforeach; endif; else: echo "" ;endif; ?>-->
    <!--</div>-->

</div>
</body>
<!-- body 最后 -->

</html>