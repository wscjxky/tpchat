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


<script type="text/javascript" src="/public/static/js/jquery.js"></script>
<link rel="stylesheet" type="text/css" href="/tpchat/Public/bootstrap/css/bootstrap.css"></link>
<link href="/tpchat/Public/plugins/daterangepicker/daterangepicker-bs3.css" rel="stylesheet" type="text/css" />
<script src="/tpchat/Public/plugins/daterangepicker/moment.min.js" type="text/javascript"></script>
<script src="/tpchat/Public/plugins/daterangepicker/daterangepicker.js" type="text/javascript"></script>
<!-- Content Header (Page header) -->
<link rel="stylesheet" href="<?php echo (CSS_URL); ?>jquery-confirm.min.css">
<script  src="<?php echo (JS_URL); ?>jquery-confirm.min.js"></script>

<script >
    $(document).ready(function() {





        $(".btn.btn-danger").click(function () {
            var doc=$(this);
            console.log($(this));
            var p_doc= doc.parent().parent().parent();
            $.confirm({
                title: '确认删除?',
                content: "确认",
                type: 'green',
                buttons: {
                    ok: {
                        text: "确认",
                        btnClass: 'btn-primary',
                        keys: ['enter'],
                        action: function(){
                            $.post("/tpchat/index.php/Admin/Trade/delTrade",
                                {
                                    trade_id:p_doc.attr('id')
                                },
                                function(data,status){
                                    if (data=='ok'){
                                        p_doc.remove();
                                    }
                                    else{
                                        $('body').html(data);
                                    }
                                });
                        }
                    },
                    cancel:{
                        text: "取消",
                        btnClass: 'btn-danger',
                        keys: ['enter'],
                        action: function(){
                        }}
                }
            });

        });

    });
</script>
<!-- Main content -->
<div class="row">

    <div class="col-md-2" style="margin-left: 30px">
        <h3>订单列表</h3>
        <h5>共<?php echo ($count); ?>条记录，课程购买数：<?php echo ($total_people); ?></h5>
    </div>
    <div class="navbar-form form-inline" style="margin-top: 50px" method="post" action="/index.php/Admin/order/export_order"  name="search-form2" id="search-form2">

        <div class="col-md-1">
            <select  id='selector' name="keytype" class="select">
                <option value="chatname">用户名</option>
                <option value="course_title">课程标题</option>
                </foreach>
            </select>
        </div>
        <div class="col-md-2">
            <input id='keyword' type="text" size="30" name="keyword" class="qsbox" placeholder="输入相关数据">
        </div>

        <div class="col-md-1">
            <select  id='trade_state' name="keytype" class="select">
                <option value="---">---</option>

                <option value="未支付">未支付</option>
                <option value="已支付">已支付</option>
            </select>
        </div>
        <div class="col-md-2">
            <button onclick="search()" class="btn btn-primary" >搜索</button>
        </div>
    </div>
</div>



<table class="table table-hover table-condensed table-striped table-bordered">
    <thead>
    <tr>
        <th>订单编号</th>
        <th>学员名称</th>
        <th>下单时间</th>
        <th>课程标题</th>
        <th>凭证码</th>
        <th>金额</th>
        <th>订单状态</th>

    </tr>
    </thead>
    <tbody>
    <?php if(is_array($data)): $i = 0; $__LIST__ = $data;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$v): $mod = ($i % 2 );++$i;?><tr id="<?php echo ($v["trade_id"]); ?>">
            <td ><?php echo ($v["trade_id"]); ?></td>
            <td ><?php echo ($v["chatname"]); ?></td>
            <td ><?php echo ($v["createtime"]); ?></td>
            <td><?php echo ($v["course_title"]); ?></td>
            <td ><?php if($v["trade_state"] == 已支付 ): echo ($v["evidence"]); ?></p><?php endif; ?>
            </td>
            <td >¥<?php echo ($v["final_price"]); ?></td>
            <td ><?php echo ($v["trade_state"]); ?></td>

        </tr>
        <tr><?php endforeach; endif; else: echo "" ;endif; ?>
    </tbody>
</table>



<!--订单-->
<div style="float: right;margin-right: 20px" class="result page"><?php echo ($page); ?></div>

<!--<div class="row">-->
<!--<div class="col-sm-6 text-left"></div>-->
<!--<div class="col-sm-6 text-right">-->
<!--<div class="dataTables_paginate paging_simple_numbers">-->
<!--<ul class="pagination">-->
<!--<li class="paginate_button active"><a tabindex="0" data-dt-idx="1" aria-controls="example1" data-p="1" href="javascript:void(0)">1</a></li>-->
<!--<li class="paginate_button"> <a class="num" data-p="3" href="javascript:void(0)">2</a></li>-->
<!--<li class="paginate_button"> <a class="num" data-p="3" href="javascript:void(0)">3</a></li>-->
<!--<li class="paginate_button"> <a class="num" data-p="4" href="javascript:void(0)">4</a></li>-->
<!--<li class="paginate_button"> <a class="num" data-p="5" href="javascript:void(0)">5</a></li>-->
<!--<li class="paginate_button"> <a class="num" data-p="6" href="javascript:void(0)">6</a></li>-->
<!--<li class="paginate_button"><a class="num" data-p="7" href="javascript:void(0)">7</a></li>-->
<!--<li class="paginate_button"><a class="num" data-p="8" href="javascript:void(0)">8</a></li>-->
<!--<li class="paginate_button"><a class="num" data-p="9" href="javascript:void(0)">9</a></li>-->
<!--<li class="paginate_button"><a class="num" data-p="10" href="javascript:void(0)">10</a></li>-->
<!--<li class="paginate_button"><a class="num" data-p="11" href="javascript:void(0)">11</a></li>-->
<!--<li id="example1_next" class="paginate_button next"><a class="next" data-p="2" href="javascript:void(0)">下一页</a></li>-->
<!--<li id="example1_previous" class="paginate_button previous disabled">-->
<!--</ul>-->
<!--</div>-->
<!--</div>-->
<!--</div>-->
</body>
<script>
    function search() {
        var keyword=$("#keyword").val();
        var act=$("#selector").val();
        var trade_state=$("#trade_state").val();
        window.location.href="/tpchat/index.php/Admin/Trade/search?act="+act+"&keyword="+keyword+"&trade_state="+trade_state;
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