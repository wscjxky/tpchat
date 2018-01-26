define(['jquery','template', 'jcrop'], function ($, Template) {
    var getJcropClass = function JcropWarpClass(){
        var j = {};
        var Portrait = '';
        var HtmlParent = '';
        var left = 0, right = 0, top = 0, bottom = 0;
        j = {title: '修改头像', useAge: 'userPortrait', ratio: 1, uploadBtn: 'portrait-btn', needCrop: true};
        j.init = function(portrait, htmlParent, cb){
            Portrait = portrait;
            HtmlParent = htmlParent;
            var tem = Template.get('script/JcropWarp/JcropWarp.html');
            var content = tem({portrait: portrait, uploadBtn: j.uploadBtn});
            HtmlParent.html(content);
            HtmlParent.find('#' + j.uploadBtn).uploadify({
                'buttonText': j.title,
                'hideButton': true,
                'wmode': 'transparent',
                'swf': "/script/uploadify/uploadify.swf",
                'height': 34,
                'uploader': '/cloud/uploadFile/easy?useAge=' + j.useAge,
                'fileTypeExts': '*.jpg;*.png;*.jpeg;*.bmp',
                'onUploadStart': function(e){
                    if (e.size / 1024 / 1024 > 2){
                        alert('请上传不大于2M的图片文件');
                        this.cancelUpload(e.id);
                        return false;
                    }
                },
                'onUploadSuccess': function (file, data, response) {
                    var obj = JSON.parse(data);
                    if (obj.errorMsg == undefined) {
                        Portrait = obj.fileName;
                        var portraitImage = HtmlParent.find('#portrait-img');
                        portraitImage.attr('src', obj.filePath);
                        if (j.needCrop){
                            portraitImage.Jcrop({
                                onSelect: cb_select,
                                bgColor: 'black',
                                bgOpacity: .4,
                                setSelect: [ 0, 0, 1000, 1000 ],
                                aspectRatio: j.ratio
                            });
                        }
                        cb(Portrait, left, top, right, bottom);
                    } else {
                        alertState("上传文件失败，错误信息：" + obj.errorMsg, "failed");
                    }
                    function cb_select(data){
                        var jcorpHolder = HtmlParent.find('.jcrop-holder');
                        var width = parseInt(jcorpHolder.css('width'));
                        var height = parseInt(jcorpHolder.css('height'));
                        left = data.x / width;
                        top = data.y / height;
                        right = data.x2 / width;
                        bottom = data.y2 / height;
                        cb(Portrait, left, top, right, bottom);
                    }
                },
                onUploadError: function (file, errorCode, errorMsg) {
                    alertState("上传文件失败，错误信息：" + errorMsg, "failed");
                }
            });
        };
        j.startSelect = function(){
            HtmlParent.find('#portrait-btn-warp').show();
        };
        j.endSelect = function(){
            HtmlParent.find('#portrait-btn-warp').hide();
        };
        return j;
    };
    return getJcropClass;
});