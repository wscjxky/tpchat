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

</head>
<body>
<style>
    input{
        width:30%;
        height:4%;
    }
</style>
<div class="page-header" style="">
    <h1>banner消息<small> <i class="fa fa-lightbulb-o"></i></small></h1>
    <ul>
        <li>详细内容<br>

    </ul>
</div>

<form method="post" action="/tpchat/index.php/Admin/Module/addbanner" enctype="multipart/form-data"  style="margin-left: 10%" >


    <!--通用信息-->
    <div class="ncap-form-default tab_div_1" >

        <dl class="row">
            <dt class="tit">
                <label >链接地址</label>
            </dt>
            <dd class="opt">
                <input type="text" value="" name="url" placeholder="http://或者https://开头" class="input-txt"/>
                <span class="err"  style="color:#F00; display:none;"></span>
            </dd>
        </dl>

        <dl class="row">
            <dt class="tit">
                <label >课程封面图片上传（jpg.png.jpgg.gif最好不超过3145728字节（3M）尺寸最小414px*255px）</label>
            </dt>
            <dd class="opt">
                <input type="file" value="<?php echo ($data["image"]); ?>" name="image">
                <span  class="err" style="color:#F00; display:none;"></span>
                <img src="<?php echo (SHOW_URL); echo ($data["image"]); ?>"/>
            </dd>
        </dl>

    </div>

    <button type="button" class="btn btn-info"  >提   交</button>

</form>

</body>

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