$(".deadline").datepicker();
var sh = [];
if($.cookie('producerDomain')) {
    sh.push($.cookie('producerDomain'));
    $.cookie('producerDomain', '', {expires: -1, path: '/'});
}
if($.cookie('refer_name')){
    $('#refer_name').text('参考视频: '+$.cookie('refer_name'));
    $('#refer_name').attr('href',($.cookie('refer_url')));
}
//if($.cookie('category_1')){
//    $("#video_category_1 option[value="+$.cookie('category_1')+"]").attr("selected", "selected");
//    $('#video_category_2').html('');
//    var category_1 = $('#video_category_1').val();
//    if(category_1 != '')
//        $.ajax({
//            type: "POST",
//            url: '/getCategory',
//            dataType: "json",
//            contentType: "application/json",
//            data: JSON.stringify({
//                id:category_1
//            }),
//            success: function (data) {
//                for (var item in data) {
//                    $('#video_category_2').append(
//                        '<option value="' + data[item].Id + '">' + data[item].Name + '</option>'
//                    );
//                }
//                $("#video_category_2 option[value="+$.cookie('category_2')+"]").attr("selected", "selected");
//                $.cookie('category_2', '', {expires: -1, path: '/'});
//                $.cookie('category_1', '', {expires: -1, path: '/'});
//            },
//            error: function () {
//                alert("搜索失败,网络异常");
//            }
//        });
//}
if($.cookie('tags')){
    $("#requirement_detail").text('标签：'+$.cookie('tags'));
    $.cookie('tags', '', {expires: -1, path: '/'});
}
$("#selectProducer").unbind('clicked').click(function(){
    $("#chosen_server").fadeIn();
    search('');
    $("#requirement_content").hide();
    $(".requirement-edit-bottom").hide();
});
$('.deleteProducer').unbind('clicked').click(function(){
    var v = $(this).attr('value');
    $.each(sh, function(key,value){
        if(value==v)
            sh.splice(key,1);
    });
    $(this).parent().parent().fadeOut();
});
$('#video_category_1').change(function(){
    $('#video_category_2').html('');
    var category_1 = $('#video_category_1').val();
    if(category_1 != '')
        $.ajax({
            type: "POST",
            url: '/getCategory',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                id:category_1
            }),
            success: function (data) {
                for (var item in data) {
                    $('#video_category_2').append(
                        '<option value="' + data[item].Id + '">' + data[item].Name + '</option>'
                    );
                }
            },
            error: function () {
                alert("搜索失败,网络异常");
            }
        });
});
function search(key){
    $.ajax({
        type: "POST",
        url: '/search',
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            req:true,
            search: key,
            sh:sh
        }),
        success: function (data) {
            $("#chosen_server").html(data);
            $(".requirement-edit-bottom").hide();

            $("#searchaw_btn").unbind('clicked').click(function(){
                search($("#searchaw-input").val());
            });
            $("#close").unbind("clicked").click(function(){
                $("#chosen_server").hide();
                $("#requirement_content").fadeIn();
                $(".requirement-edit-bottom").show();
            });
            $(".producer_checkbox").unbind('clicked').click(function(e){
                var id = $(e.currentTarget).val();
                if ($(e.currentTarget)[0].checked==true) {
                    if (sh.indexOf(id) == -1)
                        sh.push(id);
                }else{
                    $.each(sh, function(key,value){
                        if(value==id)
                            sh.splice(key,1);
                    });
                }
            });
            $("#confirm_select").unbind("clicked").click(function(){
                $.ajax({
                    type: "POST",
                    url: '/initserver',
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        sh:sh
                    }),
                    success: function (data) {
                        var tem = template.get("template/requirement/requirement_specifyProducer.html");
                        $("#chosen-server").html(tem(data));
                        $('.deleteProducer').unbind('clicked').click(function(){
                            var v = $(this).attr('value');
                            $.each(sh, function(key,value){
                                if(value==v)
                                    sh.splice(key,1);
                            });
                            $(this).parent().parent().fadeOut();
                        });
                    },
                    error:function(){
                        alert("失败,网络异常");
                    }
                });
                $("#chosen_server").hide();
                $("#requirement_content").fadeIn();
                $(".requirement-edit-bottom").show();
            });
        },
        error: function () {
            alert("搜索失败,网络异常");
        }
    });
}
$("#requirement_add_publish").unbind("clicked").click(function(){
    submit(1);
});
$("#requirement_add_commit").unbind("clicked").click(function(){
    submit(0);
});
function submit(status){
    if(!$("#requirement_title").val()){
        alert('请填写需求标题');
        return;
    }
    //if(!$("#requirement_long").val()){
    //    alert('请填写视频长度');
    //    return;
    //}
    if(!$("#requirement_detail").val()){
        alert('请填写具体需求');
        return;
    }
    if(!$(".deadline").val()){
        alert('请填写截止日期');
        return;
    }else{
        var myDate = new Date();
        var m = $(".deadline").val()[0]+$(".deadline").val()[1];
        var d = $(".deadline").val()[3]+$(".deadline").val()[4];
        var y = $(".deadline").val()[6]+$(".deadline").val()[7]+$(".deadline").val()[8]+$(".deadline").val()[9];
        if(y<myDate.getYear()+1900){
            alert("截止日期必须在今天之后");
            $(".deadline").focus();
            return 0;
        }else if (y == myDate.getYear()+1900){
            if(m<myDate.getMonth()+1){
                alert("截止日期必须在今天之后");
                $(".deadline").focus();
                return 0;
            }else if (m == myDate.getMonth()+1){
                if(d<=myDate.getDate()){
                    alert("截止日期必须在今天之后");
                    $(".deadline").focus();
                    return 0;
                }
            }
        }
    }
    if(!$("#requirement_amount").val()){
        alert('请填写预算金额');
        return;
    }
    if($.cookie('refer_url'))
        var refer = $.cookie('refer_url');
    else
        var refer = '';
    if($.cookie('refer_name'))
        var referName = $.cookie('refer_name');
    else
        var referName = '';
    var params;
    params = {
        Title: $("#requirement_title").val(),
        Detail: $("#requirement_detail").val(),
        Long:$("#requirement_long").val(),
        Amount: $("#requirement_amount").val(),
        Deadline: $(".deadline").val(),
        category_1: $('#video_category_1').val(),
        category_2: $('#video_category_2').val(),
        refer:refer,
        referName:referName,
        Status: status,
        specifyProducers:sh
    };


    function CheckLoginEx(cb) {
        $.ajax({
            type: "POST",
            url: "/checkDBToken",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                dbtoken: $.cookie('DBToken')
            }),
            success: function (data) {
                (data.bSuccess) ? cb() : signin();
            },
            error: function () {
                alert("登录失败，网络异常");
            }
        });

        function signin() {
            $('#signin').modal('show')
            $('#btn-signin').unbind('click').click(function () {
                $.ajax({
                    type: "POST",
                    url: "/SignIn",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        UserName: $('#normal_userName').val(),
                        Password: $.md5($('#normal_userPwd').val()),
                        DomainName: $("#domain_name").val(),
                        DomainUserName: $("#domain_userName").val(),
                        DomainPassword: $.md5($("#domain_userPwd").val())
                    }),
                    success: function (data) {
                        if (!data.result) {
                            alert(data.info);
                            return;
                        }
                        $('#btn-directsubmit').hide();
                        $('#signin').modal('hide')
                        cb();
                    },
                    error: function () {
                        alert("登录失败，网络异常");
                    }
                });
            })

            $('#btn-directsubmit').show();
            $('#btn-directsubmit').unbind('click').click(function () {
                $('#signin').modal('hide');
                var panel = $("#leave_contact_panel");
                panel.draggable({
                    handle: ".modal-header"
                });
                panel.modal();

                $('#lcontact_send').unbind('click').click(function () {
                    if (!$("#lcontact_name").val()) {
                        alert('请填写名字');
                        return;
                    }
                    if (!$("#lcontact_phone").val()) {
                        alert('请填写联系方式');
                        return;
                    }

                   var mesge = 'title:'+ $("#requirement_title").val()
                       +';detail:'+$("#requirement_detail").val()
                       +';long'+$("#requirement_long").val()
                       +';amount'+$("#requirement_amount").val()
                       +';deadline'+$(".deadline").val();
                    $.ajax({
                        type: "POST",
                        url: '/platform/leaveMsg',
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({
                            msg: mesge,
                            name: $('#lcontact_name').val(),
                            phone: $('#lcontact_phone').val(),
                            email: ''
                        }),
                        success: function (data) {
                            $("#leave_contact_panel").modal('hide');
                            $('#btn-directsubmit').hide();
                            alert('留言成功，我们的客服会尽快和您联系！')
                        },
                        error: function () {
                            alertState("留言失败,网络异常", "failed");
                        }
                    });
                })
            })
        }
    }
    CheckLoginEx(function(){
        $.ajax({
            type: "POST",
            url: "/publishRequirement",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(params),
            success: function (data) {
                $.cookie('refer_name', '', {expires: -1, path: '/'});
                window.location.href = '/session#/requirementPage'
            },
            error: function () {
                alert("需求提交失败，网络异常");
            }
        });
    })
}