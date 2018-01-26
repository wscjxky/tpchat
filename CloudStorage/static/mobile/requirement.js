//$(".deadline").datepicker();
//
//var sh = [];
//var refer_obj = '';
//var refer_name = '';
//
//if($.cookie('refer_obj')){
//    refer_obj = $.cookie('refer_obj');
//    refer_name = $.cookie('refer_name');
//
//    $('#refer_video').text('参考视频: '+refer_name);
//    $('#refer_video').attr('href','/mobile/share/'+refer_obj);
//
//    $.cookie('refer_name', '', {expires: -1, path: '/'});
//    $.cookie('refer_obj', '', {expires: -1, path: '/'});
//}
//var params = {
//    RequirementId:$('#request_id').attr('value')
//};






$('#cancel-publish-btn').unbind('click').click(function (e) {
                var id = $('#request_id').attr('value');
                console.log(id);
                e.stopPropagation(); //阻止消息继续传播 by zhh on 2016-10-26
                   $.ajax({
                        type: "POST",
                        url: "/mobile/deleteRequirement",
                        dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({Id: id}),
                        success: function (data) {
                                window.location.href = '/mobile/project/mine'
                            alert("需求提交成功！");

                        },
                        error: function () {
                            window.location.href = '/mobile/project/mine'
                            alert("需求提交成功！");
                        }
                    });
            });

$('#edit-publish-btn').unbind('click').click(function (e) {
                var id = $('#request_id').attr('value');
                console.log(id);
                e.stopPropagation(); //阻止消息继续传播 by zhh on 2016-10-26
               window.location.href='/mobile/editRequirement/'+id
            });

$('#comfirm-publish-btn').unbind('click').click(function (e) {
                var id = $('#request_id').attr('value');
                console.log(id);
                e.stopPropagation(); //阻止消息继续传播 by zhh on 2016-10-26
               window.location.href='/mobile/editRequirement/'+id
            });


