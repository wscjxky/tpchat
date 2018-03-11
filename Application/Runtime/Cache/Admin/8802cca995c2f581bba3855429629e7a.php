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
            console.log($(obj).attr('data-id'));

            layer.confirm('确认删除？', {
                    btn: ['确定','取消'] //按钮
                }, function(){

                    $.ajax({
                        type : 'post',
                        url : $(obj).attr('data-url'),
                        data : {act:$(obj).attr('data-act'),id:$(obj).attr('data-id')},
                        dataType : 'json',
                        success : function(data){
                            console.log(data);
                            layer.closeAll();
                            if(data==1){
                                layer.msg('操作成功', {icon: 1});
                                $(obj).parent().parent().remove();
                            }else{
                                layer.msg(data, {icon: 2,time: 2000});
                            }
                            layer.closeAll();
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
    
</head>
<body>

<div class="row">
    <div class="col-md-8" style="margin-left: 30px">
        <h3>权限资源列表</h3>
        <h5>网站权限</h5>

    </div>

</div>
<a href="" style="position:absolute;float: left;margin-top: 60px" class="btn btn-primary pull-right"><i class="fa fa-plus"></i>添加权限资源</a>

<div class="box"  style="margin-top: 100px">

    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table id="list-table" class="table table-bordered table-striped dataTable">
                    <thead>
                    <tr role="row">
                        <th>权限ID</th>
                        <th>权限分组</th>
                        <th>权限名称</th>
                        <th>操作</th>
                    </tr>
                    </thead>
                    <tbody>
                    <?php if(is_array($data)): foreach($data as $k=>$vo): ?><tr role="row" >
                            <td><?php echo ($vo["right_id"]); ?></td>
                            <td><?php echo ($vo["right_category"]); ?></td>
                            <td><?php echo ($vo["right_name"]); ?></td>
                            <td>
                                <a class="btn btn-primary" href=""><i class="fa fa-pencil"></i></a>
                                <a class="btn btn-danger" href="javascript:void(0)"><i class="fa fa-trash-o"></i></a>

                            </td>
                        </tr><?php endforeach; endif; ?>
                    </tbody>
                    <tfoot>
                    </tfoot>
                </table>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-6 text-left"></div>
            <div class="col-sm-6 text-right"><?php echo ($page); ?></div>
        </div>
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