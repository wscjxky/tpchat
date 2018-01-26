$('.carousel').carousel({
    interval: 7000,
    pause:"hover",
    keyboard:true,
    wrap:true
})

var s_channel = [];
for(var i=1;i<=$('#channel_count').val();i++){
    s_channel[i-1] = $('#s_channel_'+i).val();
}
$.ajax({
    type:"POST",
    url:"InitIndexChannel",
    dataType: "json",
    contentType: "application/json",
    data:JSON.stringify({
        init_channel:s_channel
    }),
    error:function(){
        alert("请检查网络");
    },
    success:function(data){
        $.each(data,function(index,val){
            $('#channel_'+index).html(val);
        });
    }
});
$('.s-channel').children('h5').unbind('click').click(function(){
    $(this).parent().find('.active').removeClass('active');
    $(this).addClass('active');
    var s_channel_2 = [];
    s_channel_2[0] = $(this).context.attributes['value'].value;
    $.ajax({
        type: "POST",
        url: "InitIndexChannel",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            init_channel: s_channel_2
        }),
        error: function () {
            alert("请检查网络");
        },
        success: function (data) {
            $.each(data,function(index,val){
                $('#channel_'+index).html(val);
            });
        }
    });
});
$('.col-right-content nav div').hover(function(){
    $(this).parent().find('div').removeClass('active');
    $(this).addClass('active');
    var text = $(this).attr('id');
    $("div[name = "+ text +"]").parent().find('div').hide();
    $("div[name = "+ text +"]").show();
});


