/**
 * Created by Liqinshuo on 2014/12/23.
 */
define(['jquery', 'template', 'storage'], function ($, Template, Storage) {
    function wallPage(){
        var wall = [];
        $.ajax({
            type: "POST",
            url: "/share/getWall",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
            }),
            error: function () {
                alert("get失败");
            },
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("失败.问题描述: " + data.errorMsg, "info");
                    return;
                }
                var tem = Template.get("template/wall/wall.html");
                var r = tem({'wall':data});
                $('#updata-content').html(r);
                $('#addwall').unbind("click").click(function(e){
                    Storage.filePickerDialog.open($('#addwall').parent(), function (files) {
                        $.ajax({
                            type: "POST",
                            url: "/share/addWall",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                files:files
                            }),
                            error: function(){
                                alert("添加失败");
                                return;
                            },
                            success:function(){
                                wallPage();
                            }
                        });
                    });
                });
                $(".wall-a").mouseover(function (e) {
                    var id = e.currentTarget.id;
                    var a = $(e.currentTarget).find("#wall_cancel").css("font-size","25px");
                    $(e.currentTarget).find("#wall_cancel").unbind("click").click(function(e){
                        if(!confirm("确认移出展示墙？"))return;
                        $.ajax({
                            type: "POST",
                            url: "/share/dropWall",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({
                                id:id
                            }),
                            error: function(){
                                alert("失败");
                                return;
                            },
                            success:function(){
                                alert("移出成功");
                                wallPage();
                            }
                        });
                    });
                });
                $(".wall-a").mouseout(function (e) {
                    var a = $(e.currentTarget).find("#wall_cancel").css("font-size","0px");
                });
            }
        });
    };

    var wall_interface = {};
    wall_interface.pageRouter = {
        '/WallPage': wallPage
    };
    return wall_interface;
});

