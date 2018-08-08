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


<html>
<link rel="stylesheet" type="text/css" href="/tpchat/Public/bootstrap/css/bootstrap.css">

<link href="/tpchat/Public/plugins/daterangepicker/daterangepicker-bs3.css" rel="stylesheet" type="text/css" />
<script src="/tpchat/Public/plugins/daterangepicker/moment.min.js" type="text/javascript"></script>
<script src="/tpchat/Public/plugins/daterangepicker/daterangepicker.js" type="text/javascript"></script>


<script >
</script>
<!-- Content Header (Page header) -->
<body>
<!-- Main content -->
<div class="row">

    <div class="col-md-1" style="margin-left: 30px">
        <h3>用户列表</h3>
        <h5>(共<?php echo ($count); ?>条记录)</h5>
    </div>




        <div class="row" style="margin-top: 50px;padding:2px ;"  >

            <div class="col-md-8">
                <input type="text" size="30" name="keywords" class="qsbox" placeholder="搜索用户名...">
                <button type="button" href="" class="btn btn-info" >搜索</button>
            </div>

            <div class="col-md-2">
                <a href="sendTemple?i=all"><button type="button" href="user" class="btn btn-success">群发微信模版</button></a>
                <a href="sendLog?i=all"><button type="button" href="user" class="btn btn-info">群发网站消息</button></a>
            </div>

        </div>


<table class="table table-hover table-condensed table-striped table-bordered" style="margin-top: 70px ;margin-left: 30px">
    <thead>

    <tr>
        <th>用户id</th>
        <th>用户微信名</th>
        <th>用户手机号</th>
        <th>用户地址</th>
        <th>用户性别</th>
        <th>用户头像</th>
        <th>关注时间</th>
        <th>用户积分</th>
        <th>顾问级别</th>
        <th>操作</th>
    </tr>
    </thead>
    <tbody>
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><tr id="<?php echo ($v["openid"]); ?>">
            <td ><?php echo ($v["openid"]); ?></td>
            <td ><?php echo ($v["chatname"]); ?></td>
            <td ><?php echo ($v["phone"]); ?></td>
            <td ><?php echo ($v["province"]); ?> <?php echo ($v["city"]); ?></td>
            <td><?php echo ($v["gender"]); ?></td>
            <td ><img src="<?php echo ($v["profile"]); ?>" height="60" width="60"/></td>
            <td ><?php echo ($v["createtime"]); ?></td>

            <td ><?php echo ($v["bonus_current"]); ?></td>
            <td ><?php echo ($v["agent"]); ?></td>
            <td ><div class="btn-group" role="group">
                <a href="sendTemple?i=<?php echo ($v["openid"]); ?>"><button type="button" href="user" class="btn btn-success">平台模版</button></a>
                <a href="sendLog?i=<?php echo ($v["openid"]); ?>"><button type="button" href="user" class="btn btn-info">网站消息</button></a>
                <a ><button onclick="javascript:cash(this)"   data-id="<?php echo ($v["openid"]); ?> "type="button"  class="btn btn-danger">提现<?php echo ($v["cash_submit"]); ?></button></a>

            </div></td>

        </tr><?php endforeach; endif; else: echo "" ;endif; ?>
    </tbody>
</table>


<!--?添加菜单-->


<!--订单-->
</div>
</body>
<script>
    function cash(obj) {
        console.log($(obj).attr('data-id'));
        $.confirm({
            title: '确认已经提现?',
            content: "确认",
            type: 'green',
            buttons: {
                ok: {
                    text: "确认",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        $.ajax({
                            type: 'post',
                            url: "/tpchat/index.php/Admin/User/handlecash",
                            data: {
                                id:$(obj).attr('data-id')
                            },
                            dataType: 'text',
                            success: function (data) {
                                console.log(data);
                                if (data) {
                                    history.go(0)
                                }
                            }
                        });
                    }
                },
                cancel: {
                    text: "取消",
                    btnClass: 'btn-danger',
                    keys: ['enter'],
                    action: function () {
                    }
                }
            }
            });
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