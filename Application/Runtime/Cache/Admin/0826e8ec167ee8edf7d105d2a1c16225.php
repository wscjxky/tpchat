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
    <meta charset="UTF-8">
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


    <!-- jQuery 2.1.4 -->

</head>

<body>



<div class="row">
    <div class="col-md-1" style="margin-left: 30px">
        <h3>活动推送</h3>
    </div>
</div>
<div class="box" style="margin-top: 100px">
    <div class="box-body">
        <div class="row">
            <div class="col-sm-12">
                <table id="list-table" class="table table-bordered table-striped dataTable">
                    <thead>
                    <tr role="row">
                        <th>活动编号</th>
                        <th>标题</th>
                        <th>内容</th>
                        <th>图片</th>
                        <th>操作</th>
                    </tr>
                    </thead>
                    <tbody>
                    <?php if(is_array($article)): $k = 0; $__LIST__ = $article;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$vo): $mod = ($k % 2 );++$k;?><tr role="row" >
                            <td><?php echo ($vo["article_id"]); ?></td>
                            <td><?php echo ($vo["title"]); ?></td>
                            <td><?php echo ($vo["content"]); ?></td>
                            <td><img style="width: 100px;height:100px;" src="<?php echo (SHOW_URL); echo ($vo["image"]); ?>"/></td>
                            <td>
                                <?php if($vo["publish_state"] == 0 ): ?><a> <button data-id="<?php echo ($vo["article_id"]); ?>" onclick="publish(this,1)" type="button" class="btn btn-success">发布</button></a>
                                    <?php else: ?>
                                    <a> <button data-id="<?php echo ($vo["article_id"]); ?>" onclick="publish(this,1)" type="button" class="btn btn-info">取消发布</button></a><?php endif; ?>
                                <a class="btn btn-primary"  href="article_info?id=<?php echo ($vo["article_id"]); ?>">编辑</a>

                            </td>
                        </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                    <?php if(is_array($course)): $i = 0; $__LIST__ = $course;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><tr id="<?php echo ($v["course_id"]); ?>">
                            <td ><?php echo ($v["course_id"]); ?></td>
                            <td ><?php echo ($v["title"]); ?></td>
                            <td ><?php echo ($v["desc"]); ?></td>
                            <td ><img src="<?php echo (SHOW_URL); echo ($v["image"]); ?>" height="60" width="60"/></td>

                            <td >
                                <?php if($v["publish_state"] == 0 ): ?><a> <button data-id="<?php echo ($v["course_id"]); ?>" onclick="publish(this,0)" type="button" class="btn btn-success">发布</button></a>
                                    <?php else: ?>
                                    <a> <button data-id="<?php echo ($v["course_id"]); ?>" onclick="publish(this,0)" type="button" class="btn btn-info">取消发布</button></a><?php endif; ?>

                                <a class="btn btn-primary" href="/tpchat/index.php/Admin/Course/update?i=<?php echo ($v["course_id"]); ?>">
                                    编辑
                                </a>
                                <div class="btn-group" role="group">



                            </div></td>

                        </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                    <?php if(is_array($video)): foreach($video as $k=>$vo): ?><tr role="row" >
                            <td><?php echo ($vo["activity_id"]); ?></td>
                            <td><?php echo ($vo["title"]); ?></td>
                            <td><?php echo ($vo["content"]); ?></td>
                            <td ><img src="<?php echo (SHOW_URL); echo ($vo["activity_image"]); ?>" height="60" width="60"/></td>
                            <td>
                                <?php if($vo["publish_state"] == 0 ): ?><a> <button data-id="<?php echo ($vo["activity_id"]); ?>" onclick="publish(this,2)" type="button" class="btn btn-success">发布</button></a>
                                    <?php else: ?>
                                    <a> <button data-id="<?php echo ($vo["activity_id"]); ?>" onclick="publish(this,2)" type="button" class="btn btn-info">取消发布</button></a><?php endif; ?>

                                    <a class="btn btn-primary" href="/tpchat/index.php/Admin/activity?title=<?php echo ($vo["title"]); ?>"
                                       class="btn btn-info">编辑</a>
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
<script>

    function publish(obj,type) {
        if (type ==0){
            layer.confirm('确认发布？', {
                    btn: ['确定','取消'] //按钮
                }, function(){
                    $.ajax({
                        type : 'post',
                        url :"/tpchat/index.php/Admin/course/publish",
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
        else if (type ==1){
            console.log($(obj).attr('data-id'));

            layer.confirm('确认发布？', {
                    btn: ['确定','取消'] //按钮
                }, function(){
                    $.ajax({
                        type : 'post',
                        url :"/tpchat/index.php/Admin/Module/articlePublish",
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
        else if (type ==2){
            layer.confirm('确认发布？', {
                    btn: ['确定','取消'] //按钮
                }, function(){
                    $.ajax({
                        type : 'post',
                        url :"/tpchat/index.php/Admin/activity/publish",
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