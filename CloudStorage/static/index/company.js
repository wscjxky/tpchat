$('.collect').unbind('click').click(function(e){
    CheckLogin(function(){
        $.ajax({
            type: "POST",
            url:"/collectProducer",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                DomainId:$(this).parent().find('input').val()
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
});
