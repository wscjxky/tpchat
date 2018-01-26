define(['jquery', 'template'], function ($, Template) {
    function ManagementMain(){
        $.ajax({
            type: "POST",
            url: "/share/getUserSize",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({}),
            error: function () {
                alert("网络连接失败，请检查网络");
            },
            success: function (data){
                var tem = Template.get('template/management/management-basic.html');
                var params = {
                    'IsService':$().retrieveSession().IsService,
                    user:data
                };
                $().retrieveSession().IsManagement = true;
                var test = tem(params);
                $('#pageContent').html($.trim(test));
                $().GoToUrl('/requirementPage');
            }
        });
    };

    var management_interface = {};
    management_interface.pageRouter = {
        '/managementPage': ManagementMain
    };
    return management_interface;
});
