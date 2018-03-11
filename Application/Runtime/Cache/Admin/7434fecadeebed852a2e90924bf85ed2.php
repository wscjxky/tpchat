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
    <title>Title</title>
</head>
<body>
<div class="page-header" style="">
    <h1>回复用户消息<small>提示 <i class="fa fa-lightbulb-o"></i></small></h1>
</div>
<form method="post" action="/tpchat/index.php/Admin/User/reply?advice_id=3" enctype="multipart/form-data"  style="margin-left: 10%" >

    <!--通用信息-->
    <div class="ncap-form-default tab_div_1" >

        <dl class="row">
            <dt class="tit">
                <label >内容</label>
            </dt>
            <dd class="opt">
                <textarea type="text" value=""  placeholder="content" name="content"  rows="20" style="width: 400px"></textarea>
            </dd>
        </dl>

    </div>

    <input type="submit" class="btn btn-info"   value="提交">

</form>
<script>
    $(document).ready(function () {
        $('button').click(function () {
            $.confirm({
                title: '确认提交?',
                content: "确认",
                type: 'green',
                buttons: {
                    ok: {
                        text: "确认",
                        btnClass: 'btn-primary',
                        keys: ['enter'],
                        action: function () {
                            $('form').submit();
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
        })
    })

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