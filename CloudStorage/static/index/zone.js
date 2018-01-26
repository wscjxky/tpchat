$('#focus').unbind('click').click(function(e){
    $.ajax({
        type: "POST",
        url:"/collectProducer",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            DomainId:$(this).val()
        }),
        success: function (data) {
            if(!data.bSuccess)
                self.location='/login#/loginPage';
            else
                $(e)[0].currentTarget.innerText = '已关注';
        },
        error:function(){
            alert('请检查网络。');
        }
    });
});
$('#require').unbind('click').click(function(){
    $.cookie('newReq',true,{path:'/'});
    $.cookie('producerDomain',$(this).val(),{path:'/'});
    self.location='/submit';
});
$('#viewCases').unbind('click').click(function() {
    $('#viewCases-modal').modal();
});