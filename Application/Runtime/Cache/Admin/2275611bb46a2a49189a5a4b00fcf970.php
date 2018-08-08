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
<html>
  <head>
    <meta charset="UTF-8">
    <title>后台登陆</title>
    <!-- Tell the browser to be responsive to screen width -->
    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
    <!-- Bootstrap 3.3.4 -->
    <link href="/tpchat/Public/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <!-- Theme style -->
    <script src="/tpchat/Public/plugins/jQuery/jQuery-2.1.4.min.js" type="text/javascript"></script>
    <!-- Bootstrap 3.3.2 JS -->
    <script src="/tpchat/Public/bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
    <style type="text/css">
      .form-bg{
        background: #00b4ef;
      }
      .form-horizontal{
        background: #fff;
        padding-bottom: 40px;
        border-radius: 15px;
        text-align: center;
      }
      .form-horizontal .heading{
        display: block;
        font-size: 35px;
        font-weight: 700;
        padding: 35px 0;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 30px;
      }
      .form-horizontal .form-group{
        padding: 0 40px;
        margin: 0 0 25px 0;
        position: relative;
      }
      .form-horizontal .form-control{
        background: #f0f0f0;
        border: none;
        border-radius: 20px;
        box-shadow: none;
        padding: 0 20px 0 45px;
        height: 40px;
        transition: all 0.3s ease 0s;
      }
      .form-horizontal .form-control:focus{
        background: #e0e0e0;
        box-shadow: none;
        outline: 0 none;
      }
      .form-horizontal .form-group i{
        position: absolute;
        top: 12px;
        left: 60px;
        font-size: 17px;
        color: #c8c8c8;
        transition : all 0.5s ease 0s;
      }
      .form-horizontal .form-control:focus + i{
        color: #00b4ef;
      }
      .form-horizontal .fa-question-circle{
        display: inline-block;
        position: absolute;
        top: 12px;
        right: 60px;
        font-size: 20px;
        color: #808080;
        transition: all 0.5s ease 0s;
      }
      .form-horizontal .fa-question-circle:hover{
        color: #000;
      }
      .form-horizontal .main-checkbox{
        float: left;
        width: 20px;
        height: 20px;
        background: #11a3fc;
        border-radius: 50%;
        position: relative;
        margin: 5px 0 0 5px;
        border: 1px solid #11a3fc;
      }
      .form-horizontal .main-checkbox label{
        width: 20px;
        height: 20px;
        position: absolute;
        top: 0;
        left: 0;
        cursor: pointer;
      }
      .form-horizontal .main-checkbox label:after{
        content: "";
        width: 10px;
        height: 5px;
        position: absolute;
        top: 5px;
        left: 4px;
        border: 3px solid #fff;
        border-top: none;
        border-right: none;
        background: transparent;
        opacity: 0;
        -webkit-transform: rotate(-45deg);
        transform: rotate(-45deg);
      }
      .form-horizontal .main-checkbox input[type=checkbox]{
        visibility: hidden;
      }
      .form-horizontal .main-checkbox input[type=checkbox]:checked + label:after{
        opacity: 1;
      }
      .form-horizontal .text{
        float: left;
        margin-left: 7px;
        line-height: 20px;
        padding-top: 5px;
        text-transform: capitalize;
      }
      .form-horizontal .btn{
        float: right;
        font-size: 14px;
        color: #fff;
        background: #00b4ef;
        border-radius: 30px;
        padding: 10px 25px;
        border: none;
        text-transform: capitalize;
        transition: all 0.5s ease 0s;
      }
      @media only screen and (max-width: 479px){
        .form-horizontal .form-group{
          padding: 0 25px;
        }
        .form-horizontal .form-group i{
          left: 45px;
        }
        .form-horizontal .btn{
          padding: 10px 20px;
        }
      }
    </style>
  </head>
  <body class=" form-bg">

    <div style="padding: 200px 0;">
      <div class="container">
        <div class="row">
          <div class="col-md-offset-3 col-md-6">
            <form class="form-horizontal" method="post" action="">
              <span class="heading">用户登录</span>
              <div class="form-group">
                <input type="text" name="username" id="username" class="form-control" placeholder="账号" />
                <i class="fa fa-user"></i>
              </div>
              <div class="form-group help">
                <input type="password" name="password" class="form-control" id="password" placeholder="密码" />
                <i class="fa fa-lock"></i>
                <a href="#" class="fa fa-question-circle"></a>
              </div>

              <div class="form-group">
                <div class="main-checkbox">
                  <input type="checkbox" value="None" id="checkbox1" name="check"/>
                  <label for="checkbox1"></label>
                </div>
                <span class="text">记住我</span>
                <span></span>
                <button type="submit" class="btn btn-primary btn-block btn-flat" >立即登陆 </button>
              </div>
            </form>
          </div>
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