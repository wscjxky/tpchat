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


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="wrapper">
    <section class="content">
        <div class="container-fluid">
            <div class="pull-right">
                <a href="javascript:history.go(-1)"
                   class="btn btn-default" ><i class="fa fa-reply"></i></a>

            </div>
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title"><i class="fa fa-list"></i> 编辑角色</h3>
                </div>
                <div class="panel-body ">
                    <form action="<?php echo U('Admin/Admin/roleHandle');?>" id="roleform" method="post">
                        <input type="hidden" name="role_id" value="<?php echo ($data["role_id"]); ?>" />
                        <table class="table table-bordered table-striped">
                            <tr>
                                <th >角色名称:</th>
                                <td><div class="col-xs-6">
                                    <input type="text" class="form-control" name="role_name" id="role_name" value="<?php echo ($data["role_name"]); ?>"></div></td>
                                <th >角色描述:</th>
                                <td><textarea rows="2" cols="50" name="role_desc"><?php echo ($data["role_desc"]); ?></textarea></td>
                            </tr>
                        </table>
                        <h4><b>权限分配：</b>
                        </h4>
                        <br>
                        <?php if(is_array($role_list)): $i = 0; $__LIST__ = $role_list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><label class="checkbox-inline">
                                <input type="checkbox" name=<?php echo ($i); ?> value="<?php echo ($v); ?>">   <?php echo ($v); ?>
                            </label><?php endforeach; endif; else: echo "" ;endif; ?>
                        <br>
                        <br>
                        <br>
                        <br>
                        <br>
                        <br>


                        <table class="table table-bordered table-striped dataTable">

                            <tfoot>
                            <td><input type="hidden" name="act" value="<?php echo ($act); ?>">
                                <input type="hidden" name="id" value="<?php echo ($data["role_id"]); ?>">
                            </td>
                            <tr align="center">
                                <td><input class="btn btn-default" type="reset" value="重置">&nbsp;&nbsp;&nbsp;&nbsp;
                                    <input class="btn btn-info" type="button" onclick="roleSubmit()" value="提交">
                                </td>
                            </tr>
                            </tfoot>
                        </table>
                    </form>
                </div>
            </div>
        </div></section>
</div>
<script>
    function roleSubmit() {

        if ($('#role_name').val() == '' ) {
            layer.msg('输入不能为空！', {icon: 2, time: 1000});//alert('少年，密码不能为空！');
            return false;
        }

        $('#roleform').submit();

    }
</script>
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