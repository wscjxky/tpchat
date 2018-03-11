<?php if (!defined('THINK_PATH')) exit();?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <script src="<?php echo (JS_URL); ?>jquery.js"></script>
    <link rel="stylesheet" href="/tpchat/Public/bootstrap/css/bootstrap.css">
    <script rel="stylesheet" src="/tpchat/Public/bootstrap/js/bootstrap.js"></script>
    <link href="<?php echo (CSS_URL); ?>vendors.css" rel="stylesheet" />
    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>weui.min.css">
    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-weui.min.css">
    <script src="<?php echo (JS_URL); ?>jquery-weui.js"></script>
    <script src="<?php echo (JS_URL); ?>fastclick.js"></script>

    <meta charset="UTF-8">
</head>
<html lang="en">

<style>
    .content{
        padding: 15px;
    }
    .video{
        margin-top:20px;

    }
    h1{
        font-size: 30px
    }
    .weui-cell.weui-cell_vcode{
        position: fixed;
        bottom:0;
    }
    .weui-flex{
        padding-top: 10px;
    }
    .weui-panel.weui-panel_access{
        margin-top: 20px;
        background-color: #f9f9f9;
    }

    .order {
        height: 60px;
        line-height: 60px;
    }
    .order .line {
        display: inline-block;
        width: 38%;
        border-top: 1px solid #ccc ;
    }
    .order .txt {
        color: #686868;
        vertical-align: middle;
    }

</style>
<body ontouchstart>


<div class="content">
    <h1><?php echo ($data["video_title"]); ?></h1>
    <p style="padding-top: 5px"><?php echo ($data["confirm_time"]); ?>  <?php if($data["chatname"] == '' ): echo ($data["admin_username"]); ?>
        <?php else: ?>
        <?php echo ($data["chatname"]); endif; ?>
    </p>


    <div class="video">
        <?php if($data["confirm_url"] == '' ): ?><div style="background-color: #0c0c0c;width:100%;height:300px" frameborder="0"
                    src="asd" allowfullscreen>
            </div>
        <?php else: ?>
            <iframe frameborder="0" width="100%" height="300"
                    src="<?php echo ($data["confirm_url"]); ?>" allowfullscreen>
            </iframe><?php endif; ?>



    </div>
    <div class="weui-flex ">
        <div class="weui-flex__item">
            阅读 <?php echo ($data["view_count"]); ?>
        </div>

        <div class="weui-flex__item">
                <div style="float:right;">
                    <span  id="praise-num"><?php echo ($praise_count); ?></span>
                </div>

                <div style="float:right">
                    <div class="praise">
                <span id="praise">
                 <?php if($ispraise == 0 ): ?><img src="<?php echo (IMG_URL); ?>zan.png" id="praise-img" />
                     <?php else: ?>
                     <img src="<?php echo (IMG_URL); ?>yizan.png" id="praise-img" /><?php endif; ?>
                </span>
                        <span id="add-num"><em>+1</em></span>
                    </div>

                </div>

        </div>

    </div>


    <div class="weui-panel weui-panel_access">
        <div class="weui-panel__bd">
            <a  class="weui-media-box weui-media-box_appmsg">
                <div class="weui-media-box__hd">
                    <img class="weui-media-box__thumb" src="<?php echo ($data["profile"]); ?>">
                </div>
                <div class="weui-media-box__bd">
                    <?php if($data["chatname"] == '' ): ?><h4 class="weui-media-box__title"><?php echo ($data["admin_username"]); ?></h4>
                        <?php else: ?>
                        <h4 class="weui-media-box__title"><?php echo ($data["chatname"]); ?></h4><?php endif; ?>
                    <p class="weui-media-box__desc"><?php echo ($data["admin_desc"]); ?></p>
                </div>
            </a>
        </div>
    </div>

    <div class="order">
        <span style="white-space:pre">   </span><span class="line"></span>
        <span style="white-space:pre">   </span><span class="txt">留言</span>
        <span style="white-space:pre">   </span><span class="line"></span>
    </div>
    <div style="text-align: right">
        <a id="addcomment" style="color:#0d6aad;font-size: 16px" href="/tpchat/index.php/Chat/Product/addcomment">写留言</a>
    </div>
    <div class="weui-panel weui-panel_access">
        <div class="weui-panel__bd">
            <?php if(is_array($comments)): $i = 0; $__LIST__ = $comments;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><a  class="weui-media-box weui-media-box_appmsg">
                <div class="weui-media-box__hd">
                    <img class="weui-media-box__thumb" src="<?php echo ($v["profile"]); ?>">
                </div>
                <div class="weui-media-box__bd">
                    <h5 class="weui-media-box__title"><?php echo ($v["chatname"]); ?></h5>
                    <p class="weui-media-box__desc"><?php echo ($v["content"]); ?></p>
                    <p class="weui-media-box__desc"><?php echo ($v["createtime"]); ?></p>

                </div>
            </a><?php endforeach; endif; else: echo "" ;endif; ?>
        </div>
    </div>



</div>
</body>
<!-- body 最后 -->
<script>
    $(function(){
        $("#praise").click(function(){
            var praise_img = $("#praise-img");
            var text_box = $("#add-num");
            var praise_num = $("#praise-num");
            var num=parseInt(praise_num.text());
            if(praise_img.attr("src") == ("<?php echo (IMG_URL); ?>zan.png")) {
                $(this).html("<img src='<?php echo (IMG_URL); ?>yizan.png' id='praise-img' class='animation' />");
                praise_num.addClass("hover");
                text_box.show().html("<em class='add-animation'>+1</em>");
                $(".add-animation").addClass("hover");
                num += 1;
                praise_num.text(num);

                $.ajax({
                    type: 'post',
                    url: "/tpchat/index.php/Chat/Product/praise",
                    data: {
                    },
                    dataType: 'text',
                    success: function (data) {
                        console.log(data);
                    }
                });


            }
        });
    });

</script>
<style>
    /*动态点赞开始*/
    .praise{
        width:40px;
        height:40px;
    }
    #praise{
        width:40px;
        height:40px;
        margin:0 auto;
    }

    .praise img{
        width:18px;
        height:18px;
        display:block;
        margin: 0 auto;
    }
    .praise img.animation{
        animation: myfirst 0.5s;
        -moz-animation: myfirst 0.5s;	/* Firefox */
        -webkit-animation: myfirst 0.5s;	/* Safari 和 Chrome */
        -o-animation: myfirst 0.5s;	/* Opera */
    }
    #add-num{
        display:none;
    }
    #add-num .add-animation{
        color: #000;
        position:absolute;
        top:-15px;
        left: 10px;
        font-size: 15px;
        opacity: 0;
        filter: Alpha(opacity=0);
        -moz-opacity:0;
        animation: mypraise 0.5s ;
        -moz-animation: mypraise 0.5s ;	/* Firefox */
        -webkit-animation: mypraise 0.5s ;	/* Safari 和 Chrome */
        -o-animation: mypraise 0.5s ;	/* Opera */
        font-style:normal;
    }
    .praise .hover , #add-num .add-animation.hover , #praise-txt.hover{

        color: #EB4F38;
    }

    /*点赞图标放大动画开始*/
    @keyframes myfirst
    {
        0%{
            width:40px;
            height:40px;
        }
        50%{
            width:50px;
            height:50px;
        }
        100% {
            width:40px;
            height:40px;
        }
    }

    @-moz-keyframes myfirst /* Firefox */
    {
        0%{
            width:40px;
            height:40px;
        }
        50%{
            width:50px;
            height:50px;
        }
        100% {
            width:40px;
            height:40px;
        }
    }

    @-webkit-keyframes myfirst /* Safari 和 Chrome */
    {
        0%{
            width:40px;
            height:40px;
        }
        50%{
            width:50px;
            height:50px;
        }
        100% {
            width:40px;
            height:40px;
        }
    }

    @-o-keyframes myfirst /* Opera */
    {
        0%{
            width:40px;
            height:40px;
        }
        50%{
            width:50px;
            height:50px;
        }
        100% {
            width:40px;
            height:40px;
        }
    }
    /*点赞图标放大动画结束*/
    /*点赞数量加减动画开始*/
    @keyframes mypraise
    {
        0%{
            top:-15px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
        25%{
            top:-20px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        50%{
            top:-25px;
            opacity: 1;
            filter: Alpha(opacity=100);
            -moz-opacity:1;
        }
        75%{
            top:-30px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        100% {
            top:-35px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
    }

    @-moz-keyframes mypraise /* Firefox */
    {
        0%{
            top:-15px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
        25%{
            top:-20px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        50%{
            top:-25px;
            opacity: 1;
            filter: Alpha(opacity=100);
            -moz-opacity:1;
        }
        75%{
            top:-30px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        100% {
            top:-35px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
    }

    @-webkit-keyframes mypraise /* Safari 和 Chrome */
    {
        0%{
            top:-15px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
        25%{
            top:-20px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        50%{
            top:-25px;
            opacity: 1;
            filter: Alpha(opacity=100);
            -moz-opacity:1;
        }
        75%{
            top:-30px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        100% {
            top:-35px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
    }

    @-o-keyframes mypraise /* Opera */
    {
        0%{
            top:-15px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
        25%{
            top:-20px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        50%{
            top:-25px;
            opacity: 1;
            filter: Alpha(opacity=100);
            -moz-opacity:1;
        }
        75%{
            top:-30px;
            opacity: 0.5;
            filter: Alpha(opacity=50);
            -moz-opacity:0.5;
        }
        100% {
            top:-35px;
            opacity: 0;
            filter: Alpha(opacity=0);
            -moz-opacity:0;
        }
    }
    /*点赞数量加减动画结束*/
    /*动态点赞结束*/
</style></html>