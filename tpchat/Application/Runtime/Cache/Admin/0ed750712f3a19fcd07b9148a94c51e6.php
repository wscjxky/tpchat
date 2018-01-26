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


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<script>
    $(document).ready(function () {
        $("select").change(function() {
            var type = $("select").find("option:selected").val();

            switch (type){
                case 'user_name':
                    $('#keyword').attr('placeholder',"用户名...");
                    break;
                default:
                    $('#keyword').attr('placeholder',"课程名...");

                    break
            }
        });
    });

</script>
<div class="row" style="margin-top: 50px;padding:2px ;"  >

    <div class="col-md-8">
            <label>
                <select id="selector" name="act" class="form-control">
                    <option value="user_name">查询用户名</option>
                    <option value="course_title">查询课程的订购用户</option>
                    <option value="register_title">查询课程的签到用户</option>
                </select>
            </label>
            <input id="keyword" type="text" size="30"  name="value" class="qsbox" placeholder="用户名...">
        <input id="starttime" type="text" size="30"  name="starttime" class="qsbox" placeholder="开始时间（xxxx-xx-xx）...">
        <input id="endtime" type="text" size="30"  name="endtime" class="qsbox" placeholder="结束时间（xxxx-xx-xx）...">

        <input class="btn btn-info" type="button" onclick="Submit()" value="搜索">
    </div>
    <table id="table" class="table table-hover table-condensed table-striped table-bordered" style="margin-top: 70px ;margin-left: 30px">

    </table>


    <div class="col-md-2">
        <a href="sendTemple"><button type="button" href="user" class="btn btn-success">群发微信模版</button></a>
        <a href="sendLog"><button type="button" href="user" class="btn btn-info">群发网站消息</button></a>
    </div>

</div>
</body>
<script>
    function Submit() {
        $.ajax({
            type: 'post',
            url: "/tpchat/index.php/Admin/User/search",
            data: {
                keyword:$("#keyword").val(),
                act: $("#selector").val(),
                starttime:$("#starttime").val(),
                endtime: $("#endtime").val()
            },
            dataType: 'text',
            success: function (data) {
                console.log(data);
                if (data) {
                    $("#table").html('');
                    $("#table").append(data);
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