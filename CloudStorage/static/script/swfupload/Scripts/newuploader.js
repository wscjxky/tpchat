var swfu;
var index = 0;
var count= 0;
//upload 参数
var g_upload_data=
{
    "uploadurl":"http://123.57.157.64:8080/upload.aspx",
    "download":"http://123.57.157.64:8080/download.aspx",
    "flashurl":"script/swfupload/Scripts/Uploader.swf",
	"transcodedurl":"http://123.57.157.64:8080/",
	"addfileurl":"/cloud/addFile",
	index:1000   //前端占位用  ~~
};
var Uploader = {
	CB:null,
	UploadCB:null,
	cache_:null,
	  //计算 filesize
    getFileSize: function (num) {
        if (isNaN(num)) {
            return false;
        }
        num = parseInt(num);
        var units = [" B", " KB", " MB", " GB"];
        for (var i = 0; i < units.length; i += 1) {
            if (num < 1024) {
                num = num + "";
                if (num.indexOf(".") != -1 && num.indexOf(".") != 3) {
                    num = num.substring(0, 4);
                } else {
                    num = num.substring(0, 3);
                }
                break;
            } else {
                num = num / 1024;
            }
        }
        return num + units[i];
    },
    Handler: {
		//上传成功回调
        uploadSuccess: function (serverData) {
         //   var obj=eval("("+serverData+")") ;
         //alert(JSON.stringify(serverData));
         var obj=serverData;
		   //转码返回结果
          var outfile=g_upload_data.transcodedurl+obj.filedir+"/"+obj.outfilename;   //转码后的 地址 .mp4  通过player直接播放就ok了
		   var outfileThumb=g_upload_data.transcodedurl+obj.filedir+"/img/"+obj.filcode+"_1.jpg";  //转码后的缩略图用于图标展示
		   var fileCode=obj.filcode; //非MD5   通过查询接口定时查询 文件转码状态 
		   var originName=obj.oldname ;//原始名字
		   var fileSize= obj.filesize;  //后续完善个人空间暂留obj.filesize;//file size
		   var filename=obj.filename;//临时文件
//		   var tempfile=g_upload_data.transcodedurl+"tmpfiles/"+filename

		   var status=2;//
		 //  var ext=serverData.ext.toLowerCase() ; //转换小写
         ///暂时禁用
         console.log("转码后地址:"+outfile);
         console.log("转码后缩略图:"+outfileThumb);
         console.log("FileCode:"+fileCode);
        /*********************测试****************************************/
          //class ObjectType(IntEnum):
         //  Video, Image, Document, Other = range(0, 4)
        var testObj={
	    Camera: null,
	    Category: null,
	    CreateTime: "2015-05-20T13:58:51+00:00",
	    CreatorUserId: Uploader.cache_.userId,
	    Description: null,
	    Download: null,
	    Extend: null,
	    File: {
		Ext: "png",
		Path:"image/transcoding.png",
		ThunbFile:"",
		VideoFile:outfile,
		FileCode:fileCode
	    },
	    FileId: 5,
	    Good: null,
	    Id: g_upload_data.index++,
	    KeyWord: null,
	    ModifyTime: "2015-05-20T13:58:51+00:00",
	    Name: originName,
	    OwnerUserId: 2,
	    ParentId: 1,
    	Remark: null,
	    Script: null,
	    Size: 1532,
	    Status: null,
	    Type: 0,
	    Watch: null,
    	_Left_: 30,
    	_Right_: 31,
	    _sa_instance_state: null
        };
         //秒传直接出结果
         if(obj.status=="2"){
            testObj.File.Path=outfileThumb ;
            delete g_upload_data[obj.md5]
             alertState("文件秒传成功!", "success");
             status=1;
         }else{
              alertState("文件上传成功!", "success");
          }
        ///如果是图片
        if($.checkImg(originName)){
              testObj.Type=1;
              testObj.File.Path=g_upload_data.transcodedurl+"tmpfiles/"+filename;
              testObj.File.VideoFile="";
              outfile="";
              testObj.File.path=filename;
              outfileThumb=testObj.File.Path;
        }
        ///针对其他格式进行处理视频图片外
        //上传格式允许添加一个白名单就行了
       if($.checkDocType(originName)){
              testObj.Type=2;
            //  testObj.File.Path=g_upload_data.transcodedurl+"tmpfiles/"+filename;
              testObj.File.VideoFile="";
              outfile="";
              testObj.File.Path="image/text.png";
              outfileThumb="image/text.png";
       }
      ////针对其他格式的处理
     $.ajax({
       type: "POST",
        url: g_upload_data.addfileurl,
        /////md5
        data: "md5="+obj.md5+"&FileTranscodedUrl="+outfile
               +"&UserId="+Uploader.cache_.userId+"&FileThumbUrl="
               +outfileThumb+"&FileSize="+fileSize+"&FileName="+originName+"&Id="
               +Uploader.cache_.getCurSpace().curParentId+"&DBToken="
               +$().retrieveSession().DBToken+"&Filecode="+fileCode+"&status="+status+"&FilePath="+g_upload_data.transcodedurl+"tmpfiles/"+filename,
              success: function(msg){
             //文件入库  获取id
                   Uploader.UploadCB(null,msg);
                   alertState("同步后台数据成功", "success");
          }
      });
       }
    }
};
//初始化新的上传组件
///AMD
var curTime = 0;
var cb_timeListener = null;
//flashvars里的b参数如果为1，该回调就会失效
function timeListener(t){
    curTime = parseInt(t);
    if (cb_timeListener)
        cb_timeListener(curTime);
}
function loadedHandler(){
    if (CKobject.getObjectById('ckplayer_a1').getType && CKobject.getObjectById('ckplayer_a1').getType())
        CKobject.getObjectById('ckplayer_a1').addListener('time', timeListener);
    else
        CKobject.getObjectById('ckplayer_a1').addListener('time', 'timeListener');
}
function InitSwfuploadComponent(ucb,cache_,WebUploader)
{
///////////////////////////////////////////////begin////////////////////////////////////
    $.extend({
        getDownloadURL:function(filecode,type){
           return  g_upload_data.download+"?filecode="+filecode+"&type="+type.toString();
        },
        getCurTime: function(){
            return curTime;
        },
        videoSeek: function(t){
            CKobject.getObjectById('ckplayer_a1').videoSeek(t);
        },
        videoPause: function(){
            CKobject.getObjectById('ckplayer_a1').videoPause();
        },
        viewVideo:function(videoUrl, caption, w, h, markPos, marks, timeListener){
            var flashvars = null;
            cb_timeListener = timeListener;
            var params = {bgcolor:'#FFF',allowFullScreen:true,allowScriptAccess:'always',wmode:'transparent'};
            var video = [videoUrl+'->video/mp4'];
            if($.checkBroweser()==0){
                flashvars={
                    f:videoUrl,
                    c:0,
                    p:1,
                    h:3
                };
                CKobject.embed('script/player/ckplayer/ckplayer.swf','videoPlayer','ckplayer_a1',w,h,true,flashvars,video,params);
                //alert("phone");
            }else{
                flashvars={
                    f:videoUrl,
                    c:0,
                    b:0,
                    k:markPos,      //'10|30|60',
                    n:marks,        //'打点2|打点3|打点1',
                    q:'start',
                    p:1,
                    h:4,
                    loaded:'loadedHandler'
                };
                CKobject.embedSWF('script/player/ckplayer/ckplayer.swf','videoPlayer','ckplayer_a1',w,h,flashvars,params);
            }
       },
       checkImg:function(filename){
           var re=/(jpg|png|jpeg|bmp|gif|ico)/i ;
           return re.test(filename);
       },
       checkVideo:function(filename){
           var re=/(avi|mp4|avi|wmv|asf|3gp)/i ;
           return re.test(filename);
       },
       //检测是否是其他类型文件
        checkDocType:function(filename){
           var re=/(doc|docx|xls|pdf|txt|xlsx|chm|ppt|pptx)/i ;
           return re.test(filename);
       },
       //0 1  phone  pc
       checkBroweser:function(){
            var sUserAgent = navigator.userAgent.toLowerCase();
            var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
            var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
            var bIsMidp = sUserAgent.match(/midp/i) == "midp";
            var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
            var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
            var bIsAndroid = sUserAgent.match(/android/i) == "android";
            var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
            var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
            if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
                return 0;
            } else {
               return 1;
            }
       }
    });
/////////////////////////////JQEXT///////////////////////////
	 // 实例化
        uploader = WebUploader.create({
            pick: {
                id: '#file_upload',
                label: '上传文件'
            },
            formData: {
                "action": "save",
                  "from":"",//请求的应用
                  "filetype": "",//文件属性
                  "md5":"12345" //文件的md5 秒传去除重复实际环境中我们要获取真实md5
            },
             accept: {
                  title: 'Files',
                  extensions: 'gif,jpg,jpeg,bmp,png,gif,ico,txt,pdf,ppt,pptx,doc,docx,xls,xlsx,rar,zip,chm,mp4,wmv,avi,3gp,mp3,flv,rmvb,rm,mkv,mov,mpg,mp3,f4v'
           },
            swf:g_upload_data.flashurl,
            chunked: false,
            chunkSize: 512 * 1024,
            server:g_upload_data.uploadurl+ '?action=save&md5=111',
            runtimeOrder: 'flash,html5',
            auto:'true',
            disableGlobalDnd: true,
            duplicate:false,
            fileNumLimit: 300,
            fileSizeLimit: 1000 * 1024 * 1024,    // 200 M
            fileSingleSizeLimit: 1000* 1024 * 1024   , // 50 M
        });
        ///上传进度
        uploader.on('uploadProgress',function(file,progress){
           var  percent=100*progress ;
           $("#file_" + file.id + " div.progress-bar").attr("aria-valuenow",percent.toString() ).css("width",percent+"%");
        });
        uploader.on('fileQueued',function(file){
        //文件入队列
           //添加
            var row='<div id="file_'+file.id+'" class="container-fluid"><div class="col-sm-10"><span class="fileTitle">文件: </span><span>'+ file.name+'</span><span class="fileTitle"> / </span>'
			 +'<span>'+Uploader.getFileSize(file.size)+'</span><br><div class="col-xs-1" style="padding: 0"><span class="fileTitle">状态: </span></div><div class="col-xs-8" style="padding: 0"><div class="progress smProgress" id="2_smProgress">'
			 +'<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div></div></div><div class="col-xs-3"><span id="status_tip_'+file.id+'">等待上传</span></div></div>'
			 +'<div class="col-sm-2"><red><span id="task_del_'+file.id+'" class="cancel-upload glyphicon glyphicon-remove-sign" style="font-size: 40px"></span></red></div>';
			 $("#file_upload_task_list").append(row);
			 var rowID="file_"+file.id ;
			 $("#"+"task_del_"+file.id).click(function(){
			    //从 html dom中删除  row item
			    $("#"+rowID).remove() ; //删除元素
				////从队列中移除文件
				///后续完善
                 uploader.removeFile(file.id, true);
			 });
        });
        //文件上传成功
        uploader.on('uploadSuccess',function(file,response){
                //response obj
                  $("#file_"+file.id).remove() ; //删除元素
                   Uploader.Handler.uploadSuccess(response);
                   if(0==uploader.getStats().progressNum){
                       uploader.reset();
                    }
            });
            ///文件上传出错
       uploader.on('uploadError',function(file,reason){
            alertState("文件上传失败:"+reason,"failed");
       });
       //////hook before-send-file
       WebUploader.Uploader.unRegister('preupload');
       WebUploader.Uploader.register(
           {
               name: 'preupload',
               'before-send-file': 'preupload'
           },
           {preupload: function( file ) {
               var me = this, owner = this.owner, deferred = WebUploader.Deferred();
               // 查看用户空间是否足够
               $.ajax({
                    type: "POST",
                    url: "/cloud/checkUserSize",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({fileSize: file.size}),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("检查用户空间容量失败.问题描述: " + data.errorMsg, "failed");
                            return;
                        }
                        if (data.full) {
                            alertState('您的媒体库空间不足，无法上传文件，请前往管理中心购买更多的存储空间',"failed");
                            alert('您的媒体库空间不足，无法上传文件，请前往管理中心购买更多的存储空间');
                            uploader.reset();
                        }
                        else{
                           // md5值计算完成
                           console.debug('----begin md5 cal----');
                           console.debug(file.source.name);
                           owner.md5File( file.source ).then(function( md5 ) {
                               console.debug('----finish md5 cal----');
                           ///结束继续往下走
                           //设置md5参数
                                me.options.server=g_upload_data.uploadurl+ '?action=save&md5='+md5;
                                console.log(me.options.server);
                                ///未定义
                                if(typeof(g_upload_data[md5])=="undefined")
                                {
                                    g_upload_data[md5]=true;
                                    $.ajax({
                                        type: "get",
                                        url: me.options.server,
                                        async:true,
                                        success:function(msg){
                                            //response obj
                                            if (msg){
                                                var obj=eval('('+msg+')');
                                                //文件重复
                                                if(obj.status=="2"&&document.getElementById(file.id)==null)
                                                {
                                                    console.log("MD5:"+md5);
                                                    owner.skipFile( file );
                                                    //  owner.removeFile( file );
                                                    $("#file_"+file.id).remove(); //删除元素
                                                    Uploader.Handler.uploadSuccess(obj);
                                                    if(0==uploader.getStats().progressNum)
                                                        uploader.reset();
                                                }
                                            }
                                        }
                                    });
                                }
                                //等待事件完成
                                deferred.resolve();
                           });
                        }
                    },
                    error: function () {
                        alertState("检查用户空间容量失败.网络异常", "failed");
                    }
               });
               return deferred.promise();
           }
    });
	//设置callback
	Uploader.UploadCB=ucb;
	Uploader.cache_=cache_;
	//创建任务列表按钮 通过jquery ui 打开~~ dialog
	 $("#placeholder").html('<div id="smFloating_list" title="上传任务列表"></div>');
     $("#smFloating_list").unbind("click").click(function(){
         $("#ftask").draggable({
            handle: ".modal-header"
         });
         $("#ftask").modal();
	});
	//全部删除
    $("#smStopAll").unbind("click").click(function(){
          //  $('#file_upload').uploadify('cancel','*');
          //alert( $('#file_upload').get(0));
        //直接计算md5
//         alert(document.getElementById("file_upload").files[0]);
       $(uploader.getFiles()).each(function(i, v){
           uploader.removeFile(v.id);
       });
        $('#file_upload_task_list').html('');
   });
/////////////////////////////////////////////begin////////////////////////////////////
}




