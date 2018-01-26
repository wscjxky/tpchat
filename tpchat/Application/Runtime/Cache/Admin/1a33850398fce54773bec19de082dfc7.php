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
<head>
    <!-- Include CSS for icons. -->
    <link href="/tpchat/Public/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css" />


</head>
<style>
    input{
        width: 300px;
    }
</style>
<body style="background-color: #FFF; overflow: scroll;position:relative">

<div class="page" style="  margin-left:10%">
    <div class="fixed-bar">
        <div class="item-title">
            <div class="subject">
                <h1>热点编辑</h1>
            </div>

        </div>
    </div>
    <!-- 操作说明 -->

    <!--表单数据-->

    <form method="post" action="<?php echo U('Admin/Module/articleHandle');?>" enctype="multipart/form-data"  >
        <div class="ncap-form-default tab_div_1">

            <dl class="row">
                <dt class="tit">
                    <label >标题</label>
                </dt>
                <dd class="opt">
                    <input type="text" value="<?php echo ($data["title"]); ?>"   placeholder="不超过8字" name="title" />
                    <span class="err" id="err_goods_name" style="color:#F00; display:none;"></span>
                </dd>
            </dl>

            <dl class="row">
                <dt class="tit">
                    <label >简介</label>
                </dt>
                <dd class="opt">
                    <input   value="<?php echo ($data["content"]); ?>" placeholder="不超过128字" name="content" rows="5" cols="5"  style="width: 300px">
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >图文链接</label>
                </dt>
                <dd class="opt">
                    <input  value="<?php echo ($data["url"]); ?>"  placeholder="https://mp.weixin.qq.com/s/DoT9geCUjAZiYnoF6Sg1FA"  name="url" />
                    <span  class="err" style="color:#F00; display:none;"></span>
                </dd>
            </dl>

            <dl class="row">
                <dt class="tit">

                    <label >封面图片上传（jpg.png.jpeg.gif，不超过10K，尺寸：80px*60px）</label>
                </dt>
                <dd class="opt">
                    <input type="file" value="<?php echo ($data["image"]); ?>" name="image">
                    <span  class="err" style="color:#F00; display:none;"></span>
                    <img src="<?php echo (SHOW_URL); echo ($data["image"]); ?>"/>
                </dd>
            </dl>
            <input style="display: none" value="<?php echo ($data["article_id"]); ?>"   name="id" />
            <input style="display: none" value="<?php echo ($act); ?>" name="act">

        </div>
        <br><br>  <br><br>
        <input class="btn btn-default" type="reset" value="重置">&nbsp;&nbsp;&nbsp;&nbsp;

            <input class="btn btn-info" type="button" onclick="Submit()" value="提交">



    </form>
    <!--表单数据-->
</div>





</body>

<script>
    function Submit() {

        if ($('#role_name').val() == '' ) {
            layer.msg('输入不能为空', {icon: 2, time: 1000});//alert('少年，密码不能为空！');
            return false;
        }

        $('form').submit();

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