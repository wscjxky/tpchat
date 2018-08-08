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
<head>
    <!--以上是在线编辑器 代码  end-->
    <!-- Include CSS for icons. -->
    <link href="/tpchat/Public/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css" />

    <link href="/tpchat/Public/froala_editor/css/froala_editor.pkgd.min.css" rel="stylesheet" type="text/css" />
    <link href="/tpchat/Public/froala_editor/css/froala_style.min.css" rel="stylesheet" type="text/css" />
</head>
<body style="background-color: #FFF; overflow: scroll;position:relative;">
<style>
    .ke-container.ke-container-default{
        width: 400px;
    }
</style>
<div class="page" style=" margin-left:10%">
    <div class="fixed-bar">
        <div class="item-title">
            <div class="subject">
                <h1>课程设置</h1>
            </div>

        </div>
    </div>
    <!-- 操作说明 -->

    <!--表单数据-->
    <form method="post" action="/tpchat/index.php/Admin/Course/update?i=14" enctype="multipart/form-data"  >


        <!--通用信息-->
        <div class="ncap-form-default tab_div_1">

            <dl class="row">
                <dt class="tit">
                    <label >课程标题</label>
                </dt>
                <dd class="opt">
                    <input type="text" value="<?php echo ($data["title"]); ?>"   placeholder="不超过8字" name="title" />
                    <span class="err" id="err_goods_name" style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >课程子标题</label>
                </dt>
                <dd class="opt">
                    <input  value="<?php echo ($data["subtitle"]); ?>" placeholder="不超过25字" name="subtitle" />
                    <span id="err_goods_remark" class="err" style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >课程简介</label>
                </dt>
                <dd class="opt">
                    <textarea   placeholder="不超过128字" name="desc" rows="5" cols="5"  style="width: 300px"><?php echo ($data["desc"]); ?></textarea>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >课程年龄区间</label>
                </dt>
                <dd class="opt">
                    <input  value="<?php echo ($data["age_limit"]); ?>"  placeholder="6-13"  name="age_limit" />
                    <span  class="err" style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >主讲</label>
                </dt>
                <dd class="opt">
                    <input  value="<?php echo ($data["speaker"]); ?>"  placeholder="名字"  name="speaker" />
                    <span  class="err" style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >招收人数</label>
                </dt>
                <dd class="opt">
                    <input  value="<?php echo ($data["people_limit"]); ?>"  placeholder="数字"  name="people_limit" />
                    <span  class="err" style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >课程封面图片上传（jpg.png.jpgg.gif最好不超过3145728字节（3M）尺寸：长与宽同，最小60px*60px）</label>
                </dt>
                <dd class="opt">
                    <input type="file" value="<?php echo ($data["image"]); ?>" name="image">
                    <span  class="err" style="color:#F00; display:none;"></span>
                    <img src="<?php echo (SHOW_URL); echo ($data["image"]); ?>"/>
                </dd>
            </dl>



            <dl class="row">
                <dt class="tit">
                    <label >课程价格</label>
                </dt>
                <dd class="opt">
                    <input type="text" value="<?php echo ($data["price"]); ?>" placeholder="元为单位，四舍五入.100.50=101"name="price" class="input-txt"/>
                    <span class="err" style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >课程开始时间</label>
                </dt>
                <dd class="opt">
                    <input type="text" value="<?php echo ($data["starttime"]); ?>" name="starttime" placeholder="2016-06-06 上午09:00" class="input-txt"/>
                    <span class="err"  style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <!--<dl class="row">-->
            <!--<dt class="tit">-->
            <!--<label >课程城市</label>-->
            <!--</dt>-->
            <!--<dd class="opt">-->
            <!--<input type="text" value="<?php echo ($data["address_big"]); ?>" name="address_big" placeholder="精确到县市（浙江省杭州市桐庐县）" class="input-txt"/>-->
            <!--<span class="err"  style="color:#F00; display:none;"></span>-->
            <!--</dd>-->
            <!--</dl>-->
            <dl class="row">
                <dt class="tit">
                    <label >课程地址</label>
                </dt>
                <dd class="opt">
                    <input type="text" value="<?php echo ($data["address"]); ?>" name="address" placeholder="精确到街区门号(北京市海淀区上园村3号)" class="input-txt"/>
                    <span class="err"  style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label >联系电话</label>
                </dt>
                <dd class="opt">
                    <input  value="<?php echo ($data["phone"]); ?>"  placeholder="名字"  name="phone" />
                    <span  class="err" style="color:#F00; display:none;"></span>
                </dd>
            </dl>
            <dl class="row">
                <dt class="tit">
                    <label for="">课程内容</label>
                </dt>
                <textarea id="editor" name="content"><?php echo ($data["content"]); ?></textarea>

            </dl>
        </div>

        <input type="submit" class="btn btn-info" value="提交">



    </form>

    <!--表单数据-->
</div>


</body>
<link rel="stylesheet" href="/tpchat/Public/kindeditor/themes/default/default.css" />
<script charset="utf-8" src="/tpchat/Public/js/jquery.js"></script>

<script charset="utf-8" src="/tpchat/Public/kindeditor/kindeditor-all.js"></script>
<script charset="utf-8" src="/tpchat/Public/kindeditor/lang/zh-CN.js"></script>
<script charset="utf-8" src="/tpchat/Public/kindeditor/plugins/image/image.js"></script>
<script charset="utf-8" src="/tpchat/Public/kindeditor/plugins/code/prettify.js"></script>

<script>
    KindEditor.ready(function(K) {
        var editor = K.create('#editor',{
            width:'400px' ,
            height:'700px',

                afterUpload: function(){this.sync();}, //图片上传后，将上传内容同步到textarea中
                afterBlur: function(){this.sync();}   ////失去焦点时，将上传内容同步到textarea中

            }

        );

    });
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