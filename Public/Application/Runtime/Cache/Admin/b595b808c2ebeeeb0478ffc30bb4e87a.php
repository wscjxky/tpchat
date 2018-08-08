<?php if (!defined('THINK_PATH')) exit();?>
<head>
    <meta charset="UTF-8">
    <title>Shopa</title>
    <script src="<?php echo (JS_URL); ?>jquery.js"></script>
    <!-- Tell the browser to be responsive to screen width -->
    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
    <!-- Bootstrap 3.3.4 -->
    <link href="/tpchat/Public/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <!-- FontAwesome 4.3.0 -->
    <link href="/tpchat/Public/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <!-- Ionicons 2.0.0 --
    <link href="https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css" rel="stylesheet" type="text/css" />
    <!-- Theme style -->
    <!-- iCheck -->
    <link href="/tpchat/Public/plugins/iCheck/flat/blue.css" rel="stylesheet" type="text/css" />
    <script src="/tpchat/Public/js/layer/layer-min.js"></script><!-- 弹窗js 参考文档 http://layer.layui.com/-->
    <link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-confirm.min.css">
    <script  src="<?php echo (JS_URL); ?>jquery-confirm.min.js"></script>

    <style>
        table{

        }
    </style>
    <script>
        function delfunc(obj){
            console.log($(obj));
            console.log($(obj).attr('data-url'));

            layer.confirm('确认删除？', {
                    btn: ['确定','取消'] //按钮
                }, function(){
                    $.ajax({
                        type : 'post',
                        url : $(obj).attr('data-url'),
                        data : {act:$(obj).attr('data-act'),
                            id:$(obj).attr('data-id')},
                        dataType : 'json',
                        success : function(data){
                            console.log(data);
                            if(data==1){
                                layer.msg('操作成功', {icon: 1});
                                $(obj).parent().parent().remove();
                            }
                            else if(data==2){
                                layer.msg('请先清空所属该角色的管理员', {icon: 1});
                            }
                            else{
                                layer.msg(data, {icon: 2,time: 2000});
                            }
                        }
                    })
                }, function(index){
                    layer.close(index);
                    return false;// 取消
                }
            );
        }</script>
</head>


<!doctype html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">

    <title>订单管理</title>
    <!--<script type="text/javascript">-->
        <!--var SITEURL = window.location.host +'/index.php/admin';-->
    <!--</script>-->

    <link href="/tpchat/Public/static/css/main.css" rel="stylesheet" type="text/css">
    <link href="/tpchat/Public/static/js/jquery-ui/jquery-ui.min.css" rel="stylesheet" type="text/css">
    <link href="/tpchat/Public/static/font/css/font-awesome.min.css" rel="stylesheet" />
    <script type="text/javascript" src="/tpchat/Public/static/js/jquery-ui/jquery-ui.min.js"></script>
    <script type="text/javascript" src="/tpchat/Public/static/js/jquery.cookie.js"></script>
    <script type="text/javascript" src="<?php echo (ADMIN_JS_URL); ?>admin.js"></script>
    <script type="text/javascript" src="/tpchat/Public/static/js/jquery.validation.min.js"></script>
</head>
<body style='overflow:auto ;'>

<div class="admincp-header">


    <div id="foldSidebar"><i class="fa fa-outdent " title="展开/收起侧边导航"></i></div>
    <!--<div class="admincp-name" onClick="javascript:openItem('welcome|Index');">-->
        <!--&lt;!&ndash; <h2 style="cursor:pointer;">TPshop2.0<br>平台系统管理中心</h2> &ndash;&gt;-->
    <!--</div>-->

    <div class="admincp-header-r">
        <ul class="operate nc-row">
            <li></li>

            <li><a class="login-out show-option" href="/tpchat/index.php/Admin/Index/logout" title="安全退出管理中心">&nbsp;</a></li>
        </ul>
    </div>
    <div class="clear"></div>
</div>
<div class="admincp-container unfold">
    <div class="admincp-container-left">
        <div class="top-border"><span class="nav-side"></span><span class="sub-side"></span></div>

        <div id="admincpNavTabs_index" class="nav-tabs" style="display: block!important;">

            <dl>
                <dt><a href="javascript:void(0);"><span class="ico-shop-1"></span><h3>订单</h3>
                </a></dt>
                <dd class="sub-menu">
                    <ul>
                        <li><a href="javascript:void(0);" data-param="index|Trade">订单列表</a></li>
                        <li><a href="javascript:void(0);" data-param="log|Trade">订单统计</a></li>
                    </ul>
                </dd>
            </dl>
            <dl>
                <dt><a href="javascript:void(0);"><span class="ico-shop-0"></span><h3>课程</h3>
                </a></dt>
                <dd class="sub-menu">
                    <ul>
                        <li><a href="javascript:void(0);" data-param="index|Course">课程列表</a></li>
                        <!--<li><a href="javascript:void(0);" data-param="log|Course">课程日志</a></li>-->
                    </ul>
                </dd>
            </dl>
            <dl>
                <dt>
                    <a href="javascript:void(0);"><span class="ico-system-3"></span><h3>视频</h3>
                </a>
                </dt>
                <dd class="sub-menu">
                    <ul>
                        <li><a href="javascript:void(0);" data-param="index|Video">视频列表</a></li>
                        <!--<li><a href="javascript:void(0);" data-param="log|Course">课程日志</a></li>-->
                    </ul>
                </dd>
            </dl>

            <dl>
                <dt><a href="javascript:void(0);"><span class="ico-system-4"></span><h3>权限</h3></a></dt>
                <dd class="sub-menu">
                    <ul>
                        <li><a href="javascript:void(0);" data-param="index|Admin">管理员列表</a></li>
                        <li><a href="javascript:void(0);" data-param="role|Admin">角色管理</a></li>
                        <li><a href="javascript:void(0);" data-param="log|Admin">日志管理</a></li>

                    </ul>
                </dd>
            </dl>
            <dl>
                <dt><a href="javascript:void(0);"><span class="ico-system-1"></span><h3>用户</h3></a></dt>
                <dd class="sub-menu">
                    <ul>
                        <li><a href="javascript:void(0);" data-param="index|User">用户列表</a></li>
                        <li><a href="javascript:void(0);" data-param="message|User">消息管理</a></li>
                    </ul>
                </dd>
            </dl>
            <dl>
                <dt>
                    <a href="javascript:void(0);"><span class="ico-system-5"></span><h3>单页面</h3>
                </a>
                </dt>
                <dd class="sub-menu">
                    <ul>
                        <li><a href="javascript:void(0);" data-param="index|Module">首页banner</a></li>
                        <li><a href="javascript:void(0);" data-param="article|Module">文章管理</a></li>
                        <li><a href="javascript:void(0);" data-param="advice|Module">建议管理</a></li>
                    </ul>
                </dd>
            </dl>
        </div>


</div>
    <div class="admincp-container-right">
        <div class="top-border"></div>
        <iframe src="" id="workspace" name="workspace" style="overflow: visible;" frameborder="0" width="100%" height="94%" scrolling="yes" onload="window.parent"></iframe>
    </div>
</div>
</body>

</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

</body>
</html>