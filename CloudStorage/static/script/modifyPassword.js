define(['jquery','template'],function($,Template){
    function modifyPasswordInit(){
        var tem = Template.get('template/service/ModifyPassword.html');
        var test = tem();
        $('#pageContent').html($.trim(test));

    }

    var modifyPassword_interface = {};
    modifyPassword_interface.pageRouter = {
        '/ModifyPasswordPage': modifyPasswordInit
    };
    return modifyPassword_interface;
});