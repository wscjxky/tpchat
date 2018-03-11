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
			   <h3>活动列表</h3>
			   <h5>(共<?php echo ($count); ?>条记录)</h5>
		   </div>
	   </div>
			<div class="box" style="margin-top: 2%">
				<a href="activity_info"><button type="button" class="btn btn-primary">添加活动</button></a>

				<div class="box-body">
					<div class="row">
						<div class="col-sm-12">
							<table id="list-table" class="table table-bordered table-striped dataTable">
								<thead>
								<tr role="row">
									<th>编号</th>
									<th>活动标题</th>
									<th>活动内容</th>

									<th>活动封面</th>
									<th>开始时间</th>
									<th>结束时间</th>
									<th>创建时间</th>
									<th>操作</th>
								</tr>
								</thead>
								<tbody>
								<?php if(is_array($data)): foreach($data as $k=>$vo): ?><tr role="row" >
										<td><?php echo ($vo["activity_id"]); ?></td>
										<td><?php echo ($vo["title"]); ?></td>
										<td><?php echo ($vo["content"]); ?></td>

										<td ><img src="<?php echo (SHOW_URL); echo ($vo["activity_image"]); ?>" height="60" width="60"/></td>
										<td><?php echo ($vo["createtime"]); ?></td>
										<td><?php echo ($vo["starttime"]); ?></td>

										<td><?php echo ($vo["endtime"]); ?></td>

										<td>
											<a class="btn btn-primary"  href="activity_info?id=<?php echo ($vo["activity_id"]); ?>"><i class="fa fa-pencil"></i></a>

											<a type="button" data-id="<?php echo ($vo["activity_id"]); ?>" data-act="del"  data-url="<?php echo U('Activity/activityHandle');?>" class="btn btn-danger" onclick="javascript:delfunc(this);"><i class="fa fa-trash-o"></i></a>
											<?php if($vo["publish_state"] == 0 ): ?><a> <button data-id="<?php echo ($vo["activity_id"]); ?>" onclick="publish(this)" type="button" class="btn btn-success">发布</button></a>
												<?php else: ?>
												<a> <button data-id="<?php echo ($vo["activity_id"]); ?>" onclick="publish(this)" type="button" class="btn btn-info">取消发布</button></a><?php endif; ?>
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
<script>
    function publish(obj) {
        layer.confirm('确认发布？', {
                btn: ['确定','取消'] //按钮
            }, function(){
                $.ajax({
                    type : 'post',
                    url :"/tpchat/index.php/Admin/Activity/activityHandle",
                    data : {
                        act:'publish',
                        id:$(obj).attr('data-id')
					},
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
    }//	layer.open({
//		type: 1,
//		skin: 'layui-layer-lan',
//		title:"确认",
//		btn:['确认','取消'],
//		content:
//		'<label>平台打分</label>' +
//		'<input  style="margin:20px" type="text" id="score" placeholder="5-10" value=""/>'+
//		'<label>平台评价</label>' +
//		'<input  style="margin:20px" type="text" id="admin_comment" placeholder="5-10" value=""/>'+
//		'<label>显示链接</label>' +
//		'<input  style="margin:20px" type="text" id="confirm_url" placeholder="5-10" value=""/>'+
//		'<label>平台描述</label>' +
//		'<input  style="margin:20px" type="text" id="admin_desc" placeholder="5-10" value=""/>'
//		,
//		yes: function(index,layero){
//			$.ajax({
//				type : 'post',
//				url : $(obj).attr('data-url'),
//				data : {act:$(obj).attr('data-act'),
//					id:$(obj).attr('data-id')},
//				dataType : 'text',
//				success : function(data){
//					if(data==1){
//						layer.closeAll();
//						layer.msg('操作成功', {icon: 1});
//						history.go(0);
//					}
//					else{
//						layer.msg(data, {icon: 2,time: 2000});
//					}
//				}
//			})
//		},
//		btn2: function(index,layero){
//		}
//	});

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