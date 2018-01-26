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
    <script src="/tpchat/Public/js/layer/layer.js"></script><!-- 弹窗js 参考文档 http://layer.layui.com/-->
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


<html>
<script type="text/javascript" src="/tpchat/Public/static/js/jquery.js"></script>
<link rel="stylesheet" type="text/css" href="/tpchat/Public/bootstrap/css/bootstrap.css">

<link href="/tpchat/Public/plugins/daterangepicker/daterangepicker-bs3.css" rel="stylesheet" type="text/css" />
<script src="/tpchat/Public/plugins/daterangepicker/moment.min.js" type="text/javascript"></script>
<script src="/tpchat/Public/plugins/daterangepicker/daterangepicker.js" type="text/javascript"></script>
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-confirm.min.css">
<script  src="<?php echo (JS_URL); ?>jquery-confirm.min.js"></script>
<script src="<?php echo (JS_URL); ?>jquery.qrcode.min.js"  type="text/javascript"></script>
<style>
    .layui-layer.layui-anim.layui-layer-page{
        top:150px !important;
    }
</style>
<script>
    $(document).ready(function() {

        $(".btn.btn-danger").click(function () {
            var doc=$(this);
            console.log($(this));
            var p_doc= doc.parent().parent().parent().parent();
            $.confirm({
                title: '确认删除?',
                content: "确认",
                type: 'green',
                buttons: {
                    ok: {
                        text: "确认",
                        btnClass: 'btn-primary',
                        keys: ['enter'],

                        action: function(){
                            console.log(p_doc);

                            $.post("/tpchat/index.php/Admin/Course/delCourse",
                                {
                                    course_id:p_doc.attr('id')
                                },
                                function(data,status){
                                console.log(data);
                                    if (data=='ok'){

                                        p_doc.remove();
                                    }
                                    else{
                                        $('body').html(data);
                                    }
                                });
                        }
                    },
                    cancel:{
                        text: "取消",
                        btnClass: 'btn-danger',
                        keys: ['enter'],
                        action: function(){
                        }}
                }
            });

        });

        $(".btn.btn-danger").click(function () {
            var doc=$(this);
            console.log($(this));
            var p_doc= doc.parent().parent().parent().parent();
            $.confirm({
                title: '确认删除?',
                content: "确认",
                type: 'green',
                buttons: {
                    ok: {
                        text: "确认",
                        btnClass: 'btn-primary',
                        keys: ['enter'],

                        action: function(){
                            console.log(p_doc);

                            $.post("/tpchat/index.php/Admin/Course/delCourse",
                                    {
                                        course_id:p_doc.attr('id')
                                    },
                                    function(data,status){
                                        console.log(data);
                                        if (data=='ok'){

                                            p_doc.remove();
                                        }
                                        else{
                                            $('body').html(data);
                                        }
                                    });
                        }
                    },
                    cancel:{
                        text: "取消",
                        btnClass: 'btn-danger',
                        keys: ['enter'],
                        action: function(){
                        }}
                }
            });

        });


    });
    function generateqr(obj) {
            if($(obj).attr('data-type')=='course'){
                console.log($(obj).attr('data-id'));
                $('#qrcode').qrcode("http://www.cunpianzi.com/tpchat/index.php/home/access/checkauth?course_id="+$(obj).attr('data-id')); //任意字符串
                layer.open({
                    type: 1,
                    title:'课程码课程编号：'+ $(obj).attr('data-id'),
                    closeBtn: 0,
                    area: '258px',
                    skin: '#ADADAD', //没有背景色
                    shadeClose: true,
                    content: $('#qrcode'),
                    end: function () {
                            $('#qrcode').remove();
                        $('body').prepend("<div id='qrcode'></div>");
                    }
                });
            }
            else{
                $('#qrcode').qrcode("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.cunpianzi.com/tpchat/index.php/home/access/checkauth?course_id="+$(obj).attr('data-id')+"&response_type=code&scope=snsapi_base&state=1#wechat_redirect"); //任意字符串
                layer.open({

                    type: 1,
                    title:'签到码课程编号：'+ $(obj).attr('data-id'),
                    closeBtn: 0,
                    area: '258px',
                    skin: '#ADADAD', //没有背景色
                    shadeClose: true,
                    content: $('#qrcode'),
                    end: function () {
                        $('#qrcode').remove();
                        $('body').prepend("<div id='qrcode'></div>");

                    }
                });
        }

    }


    function publish(obj) {
        layer.confirm('确认发布？', {
                    btn: ['确定','取消'] //按钮
                }, function(){
                    $.ajax({
                        type : 'post',
                        url :"/tpchat/index.php/Admin/Course/publish",
                        data : {
                            id:$(obj).attr('data-id')},
                        dataType : 'text',
                        success : function(data){
                            console.log(data);
                            if(data){
                                layer.msg('操作成功', {icon: 1});
                                history.go(0);
                            }
                        }
                    })
                }, function(index){
                    layer.close(index);
                    return false;// 取消
                }
        );
    }
</script>
<!-- Content Header (Page header) -->
<body>
<!-- Main content -->
<div id="qrcode" ></div>
<div class="row">

    <div class="col-md-1" style="margin-left: 30px">
        <h3>课程列表</h3>
        <h5>(共<?php echo ($count); ?>条记录)</h5>
    </div>
    <form class="navbar-form form-inline" style="margin-top: 50px" method="post" action="/index.php/Admin/order/export_order"  name="search-form2" id="search-form2">

        <div class="sDiv">
            <!--<div class="col-md-1">-->
                <!--<input type="text" size="30" id="add_time_begin" name="add_time_begin" value="" class="qsbox"  placeholder="起始时间">-->
            <!--</div>-->
            <!--<div class="col-md-2">-->
                <!--<input type="text" size="30" id="add_time_end" name="add_time_end" value="" class="qsbox"  placeholder="结束时间">-->
            <!--</div>-->


            <!--<div class="col-md-1">-->
                <!--<select name="shipping_status" class="select" style="width:100px;">-->
                    <!--<option value="0">正在</option>-->
                    <!--<option value="1">已参加</option>-->
                <!--</select>-->
            <!--</div>-->

            <!--<div class="col-md-1">-->
                <!--<select  name="keytype" class="select">-->
                    <!--<option value="consignee">课程发布者</option>-->
                    <!--<option value="order_sn">课程编号</option>-->
                    <!--</foreach>-->
                <!--</select>-->
            <!--</div>-->
            <!--<div class="col-md-2">-->
                <!--<input type="text" size="30" name="keywords" class="qsbox" placeholder="搜索相关数据...">-->
            <!--</div>-->



        </div>
    </form>
</div>




<table class="table table-hover table-condensed table-striped table-bordered">
    <div class="navbar-form form-inline" style="margin-top: 50px" method="post" action="/index.php/Admin/order/export_order"  name="search-form2" id="search-form2">
        <a href="addcourse"><button type="button" class="btn btn-primary">添加课程</button></a>
        <div class="col-md-1">
            <select  id="selector" name="keytype" class="select">
                <option value="title">课程名称</option>
                <option value="speaker">主讲老师</option>
            </select>
        </div>
        <div class="col-md-2">
            <input id="keyword"  type="text" size="30" name="keywords" class="qsbox" placeholder="输入相关数据">
        </div>
        <div class="col-md-1">
            <button class="btn btn-primary" onclick="search()">搜索</button>
        </div>
    </div>
    <thead>

    <tr>

        <th>课程号</th>
        <th>课程标题</th>
        <th>课程简介</th>
        <th>年龄区间</th>

        <th>地点</th>
        <th>单价</th>
        <th>图片</th>
        <th>开始时间</th>
        <th>联系电话</th>
        <th>主讲</th>
        <th>招收人数</th>
        <th>操作</th>
    </tr>
    </thead>
    <tbody>
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><tr id="<?php echo ($v["course_id"]); ?>">
            <td ><?php echo ($v["course_id"]); ?></td>
            <td ><?php echo ($v["title"]); ?></td>
            <td ><?php echo ($v["desc"]); ?></td>
            <th><?php echo ($v["age_limit"]); ?></th>

            <td ><?php echo ($v["address"]); ?></td>
            <td><?php echo ($v["price"]); ?></td>
            <td ><img src="<?php echo (SHOW_URL); echo ($v["image"]); ?>" height="60" width="60"/></td>
            <td ><?php echo ($v["starttime"]); ?></td>
            <td ><?php echo ($v["phone"]); ?></td>
            <td><?php echo ($v["speaker"]); ?></td>
            <td><?php echo ($v["people_limit"]); ?></td>
            <td ><div class="btn-group" role="group">
                <a href="update?i=<?php echo ($v["course_id"]); ?>"><button type="button" href="user" class="btn btn-success">修改</button></a>

                <a><button type="button" class="btn btn-danger">删除</button></a>
                <a><button data-id="<?php echo ($v["course_id"]); ?>" data-type="course" onclick="generateqr(this)" type="button" class="btn btn-primary">课程码</button>
                </a>
                <a> <button data-id="<?php echo ($v["course_id"]); ?>" onclick="generateqr(this)" type="button" class="btn btn-primary">签到码</button></a>
                <?php if($v["publish_state"] == 0 ): ?><a> <button data-id="<?php echo ($v["course_id"]); ?>" onclick="publish(this)" type="button" class="btn btn-success">发布</button></a>
                    <?php else: ?>
                    <a> <button data-id="<?php echo ($v["course_id"]); ?>" onclick="publish(this)" type="button" class="btn btn-info">取消发布</button></a><?php endif; ?>

            </div></td>

        </tr><?php endforeach; endif; else: echo "" ;endif; ?>
    </tbody>
</table>
</body>
<script>
    function search() {
                var keyword=$("#keyword").val();
                var act=$("#selector").val();
                window.location.href="/tpchat/index.php/Admin/Course/search?act="+act+"&keyword="+keyword;
    }
</script>
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