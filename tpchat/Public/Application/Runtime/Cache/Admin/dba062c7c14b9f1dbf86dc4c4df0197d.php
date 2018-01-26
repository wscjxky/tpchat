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
    <h1>发送模版消息<small>示范 <i class="fa fa-lightbulb-o"></i></small></h1>
    <ul>
        <li>详细内容<br>
            {{first.DATA}}<br>
            学习内容：{{keyword1.DATA}}<br>
            完成进度：{{keyword2.DATA}}<br>
            开始时间：{{keyword3.DATA}}<br>
            {{remark.DATA}}<br>
            在发送时，需要将内容中的参数（{{.DATA}}内为参数）赋值替换为需要的信息<br>
        <li>内容示例</li>
        您好，您的孩子正在进行课程学习<br>
        学习内容：《凯文在春天》<br>
        完成进度：小有成就<br>
        开始时间：2016年5月1日<br>
        点击“互动跟读”陪孩子一起学习吧！
    </ul>
</div>

<form method="post" action="/tpchat/index.php/Admin/User/sendTemple?i=all" enctype="multipart/form-data"  style="margin-left: 10%" >


    <!--通用信息-->
    <div class="ncap-form-default tab_div_1" >

        <dl class="row">
            <dt class="tit">
                <label >内容一</label>
            </dt>
            <dd class="opt">
                <input type="text" value="<?php echo ($data["title"]); ?>"  placeholder="firstdata" name="1" />
                <span class="err" id="err_goods_name" style="color:#F00; display:none;"></span>
            </dd>
        </dl>
        <dl class="row">
            <dt class="tit">
                <label >内容二</label>
            </dt>
            <dd class="opt">
                <input  value="<?php echo ($data["subtitle"]); ?>" placeholder="" name="2" />
                <span id="err_goods_remark" class="err" style="color:#F00; display:none;"></span>
            </dd>
        </dl>

        <dl class="row">
            <dt class="tit">
                <label >内容三</label>
            </dt>
            <dd class="opt">
                <input  value="<?php echo ($data["age_limit"]); ?>"  placeholder=""  name="3" ></input>
                <span  class="err" style="color:#F00; display:none;"></span>
            </dd>
        </dl>

        <dl class="row">
            <dt class="tit">
                <label >内容四</label>
            </dt>
            <dd class="opt">
                <input type="text" value="<?php echo ($data["price"]); ?>" placeholder=""name="4" class="input-txt"/>
                <span class="err" style="color:#F00; display:none;"></span>
            </dd>
        </dl>
        <dl class="row">
            <dt class="tit">
                <label >内容五</label>
            </dt>
            <dd class="opt">
                <input type="text" value="" name="5" placeholder="" class="input-txt"/>
                <span class="err"  style="color:#F00; display:none;"></span>
            </dd>
        </dl>
        <dl class="row">
            <dt class="tit">
                <label >链接地址</label>
            </dt>
            <dd class="opt">
                <input type="text" value="" name="link" placeholder="http://或者https://开头" class="input-txt"/>
                <span class="err"  style="color:#F00; display:none;"></span>
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