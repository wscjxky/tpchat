var selfSpace = "selfSpace";
var domainSpace = "domainSpace";
var shareSpace = "shareSpace";
var myShareSpace = "myShareSpace";

define(['jquery', 'template', 'shareSetting','webuploader', 'JcropWarp', 'zclip', 'sortElement', 'context-menu'], function ($, Template, ShareSetting, webuploader, JcropWarp) {
    var shareSpaceId = -2;
    var myShareSpaceId = -3;
    var imageCache = {};
	var navigateMode = {"gridMode": 1, "listMode": 2};
	var curNavigateMode = navigateMode["gridMode"];
    var filterMode = {"video": "videoFilter", "pic": "picFilter", "doc": "docFilter", "none": "noneFilter"};
    var curFilterMode = filterMode["none"];
    var cache_ = {
        bInit: false,
        userId: -1,
        nickName: "",
        email: "",
        curSpace: 0,
        spaces: [],
        shares: {},
        user:{},
        getCurSpace: function () {
            return this.spaces[this.curSpace]
        },
        isSelf: function () {
            return this.spaces[this.curSpace].spaceType == selfSpace
        },
        isDomain: function () {
            return this.spaces[this.curSpace].spaceType == domainSpace
        },
        isShare: function () {
            return this.spaces[this.curSpace].spaceType == shareSpace
        }
    };

    function templateHelper_is_object_shared(objId) {
        if (cache_.shares[objId] != null)
            return "inline-block";
        return "none";
    }

    function templateHelper_suffix_image(fileName) {
        //^.*?[.](?P<ext>tar\.gz|tar\.bz2|\w+)$
        if (isVideo(fileName))
            return "image/video.png";
        else if (isImage(fileName))
            return "";
        else if (isText(fileName))
            return "image/text.png";
        else if (isShareUser(fileName))
            return "image/shareUser.png";
        return "image/unknown.png";
    }

    Template.helper("ParseTime", function (date) {
        var d = new Date(date);
        return d.toString('yyyy-MM-dd HH:mm');
    });

    Template.helper("ToMB", function (size) {
        var kbSize = size / 1024;
        var mbSize = kbSize / 1024;
        var gbSize = mbSize / 1024;
        if (gbSize > 1)
            return gbSize.toFixed(2) + 'GB';
        if (mbSize > 1)
            return mbSize.toFixed(2) + 'MB';
        else
            return kbSize.toFixed(2) + "KB";
    });

    Template.helper("IsVideo", function (suffix) {
        if (isVideo(suffix))
            return "block";
        return "none";
    });

    Template.helper("ImageHeight", function (image) {
        var img = new Image();
        img.src = "../fileFolders/" + image;
        var w, h;
        if (img.complete) {
            w = img.width;
            h = img.height;
            cal(w, h);
        }
        else {
            img.onload = function () {
                w = img.width;
                h = img.height;
                cal(w, h);
            };
        }
        function cal(width, height) {
            if (width > height)
                height = 80 * height / width;
            else
                height = 80;
            imageCache[image] = height;
            var el = $("#" + image);
            el.css("height", height + "px");
            if (height < 80)
                el.css("margin-top", (80 - height) / 2);
            el.css("display", "block");
        }
    });

    function isVideo(fileName) {
        var strVideoRegex = "(mp4|mpg|mpeg|rp|rmvb|vod|mov|rm|flv)$";
        var re = new RegExp(strVideoRegex);
        return re.test(fileName);
    }

    function isImage(fileName) {
        var strImageRegex = "(jpg|JPG|gif|png)$";
        var re = new RegExp(strImageRegex);
        return re.test(fileName);
    }

    function isText(fileName) {
        var strTextRegex = "(txt|xml|json)$";
        var re = new RegExp(strTextRegex);
        return re.test(fileName);
    }

    function isShareUser(fileName) {
        return fileName == "shareUser";
    }

    function isObjDir(objectId) {
        return (cache_.getCurSpace().objectMap[objectId].fileId == null);
    }

    function isNormalObject(objId, parentId) {
        if (objId >= 0)
//            if (objId >= 0 && (parentId == null || parentId > 0))
            return true;
        return false;
    }

    //解析DBList信息
    function parseDBListInfo(data) {
        var spaceNum = 0;
        cache_.nickName = data.User.NickName;
        cache_.IsService = data.User.Domain.IsService;
        cache_.email = data.User.Email;
        cache_.userId = data.User.Id;
        cache_.storageSize = data.User.Domain.DefaultStorageSize + data.User.Domain.ExtendStorageSize;
        cache_.usedSize = data.User.Domain.UsedSize;
        //个人空间
        if (data.User.RootObject != null) {
            cache_.spaces[spaceNum++] = {
                spaceType: selfSpace,
                spaceName: "媒体库", //data.User.NickName
                spaceId: -1,
                rootObjId: data.User.RootObject.Id,
                ownerId: data.User.RootObject.OwnerUserId,
                curParentId: -1,
                copyObjId: null,
                activeObj: null,
                reNameObj: null,
                objectMap: [],
                levelTree: []
            };
        }
        //域空间
        if (data.User.Domain.OwnerUserId != data.User.Id) {
            cache_.spaces[spaceNum++] = {
                spaceType: domainSpace,
                spaceName: "媒体库",
                spaceId: data.User.Domain.Id,
                rootObjId: data.User.Domain.RootObject.Id,
                ownerId: data.User.Domain.OwnerUserId,
                curParentId: -1,
                copyObjId: null,
                activeObj: null,
                reNameObj: null,
                objectMap: [],
                levelTree: []
            };
        }
        //他人共享
        cache_.spaces[spaceNum++] = {
            spaceType: shareSpace,
            spaceName: "他人共享",
            spaceId: shareSpaceId,
            rootObjId: shareSpaceId,
            ownerId: -1,
            curParentId: shareSpaceId,
            copyObjId: null,
            activeObj: null,
            reNameObj: null,
            objectMap: [],
            levelTree: []
        };
        //我的共享
        cache_.spaces[spaceNum] = {
            spaceType: myShareSpace,
            spaceName: "我的共享",
            spaceId: myShareSpaceId,
            rootObjId: myShareSpaceId,
            ownerId: -1,
            curParentId: myShareSpaceId,
            copyObjId: null,
            activeObj: null,
            reNameObj: null,
            objectMap: [],
            levelTree: []
        };
        cache_.shares = {};
        cache_.Category_1 = {};
        cache_.Category_2 = {};
        cache_.Tags = data.Tags;
        $(data.Shares).each(function (index, value) {
            cache_.shares[value.ObjectId] = value;
        });
        $(data.Category_1).each(function(index, value){
            cache_.Category_1[value.Id] = value;
        });
        $(data.Category_2).each(function(index, value){
            cache_.Category_2[value.Id] = value;
        });
    }
    // 初始化上传组件
    function initUploadComponent() {
       InitSwfuploadComponent(uploadFileSuccess,cache_,webuploader);
    }
    function initStoragePage() {
        var tem = Template.get('template/storage/storagePage.html');
        var test = tem(cache_);
        $('#pageContent').html($.trim(test));
        $("#createDirectory").unbind("click").click(function () {
            newObject();
        });
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            cache_.curSpace = e.target.id;
            var objId;
            if (cache_.getCurSpace().curParentId != -1)
                objId = cache_.getCurSpace().curParentId;
            else
                objId = cache_.getCurSpace().rootObjId;
            initUploadComponent();
            getChildObject(objId);
        });
        initUploadComponent();

        document.onkeydown = function(event){
            var space = cache_.getCurSpace();
            if (space.activeObj && event.keyCode == 46)
                delObject(space.activeObj.id);
            else if (space.activeObj && event.ctrlKey && event.keyCode == 67)
                cache_.copyObject = {SrcId: space.activeObj.id};
            else if (event.ctrlKey && event.keyCode == 86 && cache_.copyObject != undefined)
               copyObject(space.curParentId);
        };
    }

    function storagePage() {
        cache_.bInit = true;
        Template.helper('suffix_image', templateHelper_suffix_image);
        Template.helper('is_object_shared', templateHelper_is_object_shared);

        $.ajax({
            type: "POST",
            url: "/cloud/getDBList",
            dataType: "json",
            contentType: "application/json",

            data: JSON.stringify({}),
            beforeSend: function(){
                var tem = Template.get('template/service/loading.html');
                var test = tem(cache_);
                $('#functionalArea').html($.trim(test));
            },   //加载
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("取DBLIST失败.问题描述: " + data.errorMsg, "failed");
                    return;
                }
                //解析DBList信息
                parseDBListInfo(data);
                initStoragePage();
                getChildObject(cache_.getCurSpace().rootObjId);
            },
            error: function () {
                alertState("取DBLIST失败.网络异常", "failed");
            }
        });
    }

    //特殊对象，共享空间内的用户节点
    function getSpecialChildObject(id, search) {
        if (id == myShareSpaceId) {
            getMyShareObjects(search);
        }
        else if (id == shareSpaceId) {
            $.ajax({
                type: "POST",
                url: "/cloud/getShareUsers",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({}),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("获取共享内容失败.问题描述: " + data.errorMsg, "failed");
                        return;
                    }
                    if (!cache_.isShare())
                        return;

                    var param = {Items: []};
                    var specialId = -100;
                    $(data).each(function (index, value) {
                        param.Items[index] = {
                            CreateTime: null,
                            ModifyTime: null,
                            CreatorUserId: value.Id,
                            Id: specialId--,
                            Name: value.CompanyName,
                            OwnerUserId: value.Id,
                            ParentId: -2
                        };
                    });
                    initObjectTree(param);
                    alertState("获取共享内容完成", "success");
                },
                error: function () {
                    alertState("获取共享内容失败，网络异常", "failed");
                }
            });
        }
        else {
            $.ajax({
                type: "POST",
                url: "/cloud/getShares",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    ShareDomainId: cache_.getCurSpace().objectMap[id].creatorId
                }),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("获取共享对象失败.问题描述: " + data.errorMsg, "failed");
                        return;
                    }
                    if (!cache_.isShare())
                        return;

                    var param = {Items: []};
                    $(data).each(function (index, value) {
                        param.Items[index] = {
                            CreateTime: value.Object.CreateTime,
                            CreatorUserId: value.Object.CreatorUserId,
                            ModifyTime: value.Object.ModifyTime,
                            Id: value.Object.Id,
                            Name: value.Object.Name,
                            OwnerUserId: value.Object.OwnerUserId,
                            ParentId: id,
                            FileId: value.Object.FileId,
                            Size: value.Object.Size,
                            Description: value.Object.Description,
                            Tag: value.Object.Tag,
                            File: value.Object.File,
                            Type: value.Object.Type,
                            bWrite: value.WritePermission,
                            bDownload: value.DownloadPermission
                        };
                    });
                    initObjectTree(param);
                    alertState("获取共享对象完成", "success");
                },
                error: function () {
                    alertState("获取共享对象失败，网络异常", "failed");
                }
            });
        }
    }
    function getChildObject(parentObjId, search) {
        var space = cache_.getCurSpace();
        space.curParentId = parentObjId;
        //特殊对象，共享空间内的用户节点
        if (parentObjId < 0) {
            $('#createDirectory').hide();
            $('#smFloating_list').hide();
            $('#uploader').hide();
            getSpecialChildObject(parentObjId, search);
            return;
        }
        else{
            $('#createDirectory').show();
            $('#smFloating_list').show();
            $('#uploader').show();
        }
        var param = {
            Id: space.curParentId,
            Page: 1,
            PageStep: 200,
            IsDeep: false
        };
        if (search)
            param.SearchKeyword = search;
        $.ajax({
            type: "POST",
            url: "/cloud/childObjects",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("获取目录内容失败.问题描述: " + data.errorMsg, "failed");
                    return;
                }
                if (search)
                    data.search = search;
                initObjectTree(data);
                initUploadComponent();
                alertState("获取共享用户节点目录内容完成", "success");
            },
            error: function () {
                alertState("获取目录内容失败，网络异常", "failed");
            }
        });
    }
    function getMyShareObjects(search) {
        var param = {};
        if (search)
            param.SearchKeyword = search;
        $.ajax({
            type: "POST",
            url: "/cloud/getMyShares",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("获取目录内容失败.问题描述: " + data.errorMsg, "failed");
                    return;
                }
                if (search)
                    data.search = search;
                initObjectTree(data);
                alertState("获取分享目录内容完成", "success");
            },
            error: function () {
                alertState("获取目录内容失败，网络异常", "failed");
            }
        });
    }
    function initSortTable(){
        $('.fileHeader, .typeHeader, .createTimeHeader').each(function(){
            var th = $(this),
            thIndex = th.index(),
            inverse = false;

            th.click(function(){
                $(".objectTable").find('td').filter(function(){
                    return $(this).index() === thIndex + 1;
                }).sortElements(function(a, b){
                    return $.text([a]) > $.text([b]) ? inverse ? -1 : 1 : inverse ? 1 : -1;
                }, function(){
                    return this.parentNode;
                });
                inverse = !inverse;
                if (inverse){
                    th.find(".glyphicon").removeClass("glyphicon-chevron-down");
                    th.find(".glyphicon").addClass("glyphicon-chevron-up");
                }
                else{
                    th.find(".glyphicon").removeClass("glyphicon-chevron-up");
                    th.find(".glyphicon").addClass("glyphicon-chevron-down");
                }
            });
        });
    }
    function initObjectTree(data) {
        var tem = Template.get('template/storage/objectTree.html');
		data.navigateMode = curNavigateMode;
        data.filterMode = curFilterMode;
        var test = tem(data);
        $('#objectTree_for_click').show();
        $('#objectTreeViewer').html($.trim(test));

        //初始化排序功能
        initSortTable();

        $.each(imageCache, function (n, value) {
            var el = $("#" + n);
            el.css("height", value + "px");
            if (value < 80)
                el.css("margin-top", (80 - value) / 2);
            el.css("display", "block");
        });
        var levelTree = configureLevelTree(cache_.getCurSpace().curParentId);
        tem = Template.get('template/storage/levelTree.html');
        test = tem(levelTree);
        $('#levelTreeNavigate').html($.trim(test));
        $(".levelTreeItem").unbind("click").click(function (e) {
            click_levelTreeItem(e);
        });
        $("#search_storage").unbind("click").click(function () {
            getChildObject(cache_.getCurSpace().curParentId, $("#search_content").val());
        });
        $("#search_content").bind('keyup', function (event) {
            if (event.keyCode == 13)
                getChildObject(cache_.getCurSpace().curParentId, $("#search_content").val());
        });
        $("#backstorage").unbind("click").click(function () {
            getChildObject(cache_.getCurSpace().curParentId);
        });
		$("#gridMode").unbind("click").click(function (){
            curNavigateMode = navigateMode["gridMode"];
            getChildObject(cache_.getCurSpace().curParentId);
		});
        $("#listMode").unbind("click").click(function (){
            curNavigateMode = navigateMode["listMode"];
            getChildObject(cache_.getCurSpace().curParentId);
		});
		if (curNavigateMode == navigateMode["gridMode"])
			$("#gridMode").addClass("active");
		else
			$("#listMode").addClass("active");
        $("#videoFilter").unbind("click").click(function (){
            curFilterMode = filterMode["video"];
            getChildObject(cache_.getCurSpace().curParentId);
		});
        $("#picFilter").unbind("click").click(function (){
            curFilterMode = filterMode["pic"];
            getChildObject(cache_.getCurSpace().curParentId);
		});
        $("#docFilter").unbind("click").click(function (){
            curFilterMode = filterMode["doc"];
            getChildObject(cache_.getCurSpace().curParentId);
		});
        $("#noneFilter").unbind("click").click(function (){
            curFilterMode = filterMode["none"];
            getChildObject(cache_.getCurSpace().curParentId);
		});
        $("#" + curFilterMode).addClass("active");

        //空白处点击处理
        $("#objectTree_for_click").mousedown(function () {
            var el_text = $('.cloud_object_text').find('p');
            el_text.removeClass("label-success");
//            el_text.addClass("label-primary");
            cache_.getCurSpace().activeObj = null;
            showObjectDescription(false);
        });
        $("#rClickObjectMenu").contextmenu({
            target: '#object-menu',
            onItem: rClickObjectMenu,
            before: before_rClickObjectMenu
        });
        $.each(data.Items, function (n, value) {
            var selector = "#" + value.Id;
            initObject(selector, value);
        });
        //默认激活第一项
        cache_.getCurSpace().activeObj = $("#objectTreeViewer").find(".cloud_object").first();
        cache_.getCurSpace().activeObj.addClass("active");
    }
    function initObject(selector, data) {

        $(selector).draggable({helper: "clone"});
        //只有普遍对象，并且对象的父对象也为普通对象才能有菜单等功能
        //排除在外的包括共享的用户节点，每个用户共享的内容根节点
        if (isNormalObject(data.Id, data.ParentId)) {
            //拖拽属性设置
            $(selector).droppable({drop: function (event, ui) {
                dropObject(event, ui, $(this))
            }});
            $(selector).contextmenu({
                target: '#object-menu',
                onItem: rClickObjectMenu,
                before: before_rClickObjectMenu
            });
            //对象编辑框失去焦点时完成重命名
			var el_input;
			if (curNavigateMode == navigateMode["gridMode"])
				el_input = $(selector).find(".cloud_object_edit");
			else 
				el_input = $(selector).find(".list_object_input > input");
            el_input.blur(function () {
                reNameObject(false, true);
            });
            //回车键按下，完成重命名
            el_input.bind('keyup', function (event) {
                if (event.keyCode == 13)
                    reNameObject(false, true);
                else if (event.keyCode == 27)
                    reNameObject(false, false);
            });
        }
        //对象鼠标按键设置
        $(selector).mousedown(function (e) {
            onMouseDown_object(e);
            return false;
        });
        ////////////////修改/////////////////
       //class ObjectType(IntEnum):
       //Video, Image, Document, Other = range(0, 4)
        if (data.FileId && data.Type==0) {
        var FileCode=data.File.FileCode;
           //设置播放文件
//            console.log(data);
            $(selector).dblclick(viewVideo);
            $(selector).data("VideoFile",data.File.VideoFile);
            $(selector).data("Name",data.Name);
            $(selector).data("Type",0);
            $(selector).data("FileCode",data.File.FileCode);
            $(selector).data("ObjId",data.Id);
            $(selector).data("ImagePath",data.File.Path);
        }
        else if (data.FileId && data.Type==1)
        {
            $(selector).data("ImagePath",data.File.Path);
            $(selector).data("Name",data.Name);
            $(selector).data("Type",1);
            $(selector).data("FileCode",data.File.FileCode);
            $(selector).dblclick(viewImage);
        }
         else if (data.FileId && data.Type==2)
        {
            $(selector).data("ImagePath",data.File.Path);
            $(selector).data("filePath",data.File.VideoFile);
            $(selector).data("Name",data.Name);
            $(selector).data("Type",2);
            $(selector).data("FileCode",data.File.FileCode);
            $(selector).dblclick(viewDocument);
        }
        else
           //其他类型的文件
            $(selector).dblclick(enterObject);
        ////////////////////////////////////////////
        cache_.getCurSpace().objectMap[data.Id] = {
            createTime: data.CreateTime,
            creatorId: data.CreatorUserId,
            modifyTime: data.ModifyTime,
            name: data.Name,
            ownerId: data.OwnerUserId,
            parentId: data.ParentId,
            id: data.Id,
            fileId: data.FileId,
            description: data.Description,
            camera: data.Camera,
            script: data.Script,
            size: data.Size,
            tag: data.Tag,
            category_1: data.Category_1,
            category_2: data.Category_2,
            BShare: data.BShare,
            ReferPrice: data.ReferPrice,
            BasePrice: data.BasePrice,
            SchemePrice: data.SchemePrice,
            ShotPrice: data.ShotPrice,
            ActorPrice: data.ActorPrice,
            MusicPrice: data.MusicPrice,
            AEPrice: data.AEPrice,
            Price: data.Price,
            shareObjectId: data.ShareObjectId,
            type: data.Type
        };
        if (data.hasOwnProperty('bWrite'))
            cache_.getCurSpace().objectMap[data.Id]['bWrite'] = data.bWrite;
        if (data.hasOwnProperty('bDownload'))
            cache_.getCurSpace().objectMap[data.Id]['bDownload'] = data.bDownload;
    }

    function dropObject(event, ui, dest) {
        var srcObjId = ui.draggable.attr("id");
        var destObjId = dest.attr("id");
        var space = cache_.getCurSpace();
        var param = {
            SrcId: srcObjId,
            DestId: destObjId,
            SrcShareId: space.ownerId,
            DesShareId: space.ownerId
        };
        if (space.objectMap[destObjId].fileId != null)
            return;

        $.ajax({
            type: "POST",
            url: "/cloud/moveObject",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("移动文件操作失败.问题描述: " + data.errorMsg, "failed");
                    return;
                }
                UpdateObjectState(srcObjId);
                $("#" + srcObjId).remove();
                alertState("移动文件操作完成", "success");
            },
            error: function () {
                alertState("移动文件操作失败，网络异常", "failed");
            }
        });
    }

    function enterObject() {
        var space = cache_.getCurSpace();
        if (isObjDir(space.activeObj.id))
            getChildObject(space.activeObj.id);
    }
    ///观看视频
    function viewVideo() {
//        window.open("/share/" + $(this).data("ObjId"));
        $.extend($().voSetup, $().voDefaultSetup({
            name: $(this).data("Name"),
            path: $(this).data("VideoFile"),
            type: $(this).data("Type"),
            el_hide: $("#objectTree_for_click"),
            el_show: $('#objectViewer')
        }));
        $().ViewObject();
    }
    //观看图片
    function viewImage() {
        $.extend($().voSetup, $().voDefaultSetup({
            name: $(this).data("Name"),
            path: $(this).data("ImagePath"),
            type: $(this).data("Type"),
            el_hide: $("#objectTree_for_click"),
            el_show: $('#objectViewer')
        }));
        $().ViewObject();
    }
    //预览文档
    function viewDocument(){
        $.extend($().voSetup, $().voDefaultSetup({
            name: $(this).data("Name"),
            path: $(this).data("filePath"),
            type: $(this).data("Type"),
            el_hide: $("#objectTree_for_click"),
            el_show: $('#objectViewer')
        }));
        $().ViewObject();
    }
    //新建目录
    function newObject() {
        var id = "新建文件夹";
        var space = cache_.getCurSpace();
        var param = {Name: id, DestId: space.curParentId};
        $.ajax({
            type: "POST",
            url: "/cloud/createDir",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("新建目录操作失败. 问题描述: " + data.errorMsg, "failed");
                    return;
                }
                getChildObject(cache_.getCurSpace().curParentId);
                alertState("新建目录操作完成", "success");
            },
            error: function () {
                alertState("新建目录操作失败，网络异常", "failed");
            }
        });
    }

    function reNameObject(bStart, bRename) {
        var el_text;
        var el_input;
		var el_inputContainer;
        var text;
		var space = cache_.getCurSpace();
        if (bStart) {
            space.reNameObj = space.activeObj;
			if (curNavigateMode == navigateMode["gridMode"]){		
				el_text = $(space.reNameObj).find(".cloud_object_text");
				el_input = $(space.reNameObj).find(".cloud_object_edit");
				el_inputContainer = el_input;
				text = el_text.find("p").text();
			}
			else{
				el_text = $(space.reNameObj).find(".list_object_text");
				el_input = $(space.reNameObj).find(".list_object_input > input");
				el_inputContainer = $(space.reNameObj).find(".list_object_input");
				text = el_text.find(".text").text();
			}
            el_input.addClass("form-control");
            el_input.val(text);
            el_text.hide();
            el_inputContainer.show();
            el_input.focus();
            el_input.select();
        }
        else {
			if (curNavigateMode == navigateMode["gridMode"]){		
				el_text = $(space.reNameObj).find(".cloud_object_text");
				el_input = $(space.reNameObj).find(".cloud_object_edit");
				el_inputContainer = el_input;
				text = el_text.find("p").text();
			}
			else{
				el_text = $(space.reNameObj).find(".list_object_text");
				el_input = $(space.reNameObj).find(".list_object_input > input");
				el_inputContainer = $(space.reNameObj).find(".list_object_input");
				text = el_text.find(".text").text();
			}
            if (bRename && text != el_input.val()) {
                var param = {
                    Name: el_input.val(),
                    Id: space.reNameObj.id
                };
                $.ajax({
                    type: "POST",
                    url: "/cloud/renameObject",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify(param),
                    success: function (data) {
                        if (!isResponseDataAvailable(data)) {
                            alertState("文件重命名操作失败.问题描述: " + data.errorMsg, "failed");
                            return;
                        }
                        space.objectMap[data.Id].name = data.Name;
                        reNameObject_ui(data.Id, data.Name);
                        alertState("文件重命名操作完成", "success");
                    },
                    error: function () {
                        alertState("文件重命名操作失败，网络异常", "failed");
                    }
                });
            }
            el_text.show();
            el_inputContainer.hide();
            space.reNameObj = null;
        }
    }

    function reNameObject_ui(objId, name) {
        var el_text;
		if (curNavigateMode == navigateMode["gridMode"]){
			el_text = $("#" + objId).find(".cloud_object_text");
			el_text.find("p").text(name);
			el_text.find("p").attr("title", name);
		}
		else{
			el_text = $("#" + objId).find(".list_object_text");
			el_text.find(".text").text(name);
        }
	}

    function delObject(objId) {
        if (confirm("确定删除？") != true)
            return;

        var space = cache_.getCurSpace();
        var param = {Id: objId};
        $.ajax({
            type: "POST",
            url: "/cloud/delObject",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("删除文件操作失败.问题描述: " + data.errorMsg, "failed");
                    return;
                }
                if (data.hasOwnProperty('failedContent')){
                    alert(data.failedContent);
                    return;
                }

                UpdateObjectState(objId);
                $("#" + objId).remove();
                alertState("删除文件操作完成", "success");
            },
            error: function () {
                alertState("删除文件操作失败，网络异常", "failed");
            }
        });
    }

    function copyObject(destObjId) {
        var param = {DestId: destObjId};
        param = $.extend(param, cache_.copyObject);
        $.ajax({
            type: "POST",
            url: "/cloud/copyObject",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(param),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("拷贝文件操作失败.问题描述: " + data.errorMsg, "failed");
                    return;
                }
                getChildObject(cache_.getCurSpace().curParentId);
                alertState("拷贝文件操作完成", "success");
            },
            error: function () {
                alertState("拷贝文件操作失败，网络异常", "failed");
            }
        });
    }

    function shareObject(objId) {
        var space = cache_.getCurSpace();
        var data = {
            objectId: objId,
            objectName: space.objectMap[objId].name,
            spaceId: space.spaceId,
            spaceName: space.spaceName,
            spaceType: space.spaceType,
            cb_shareObjectDone: function (bSuccess) {
                if (bSuccess)
                    storagePage();
            }
        };
        ShareSetting.initSetting(data);
    }

    function cancelShareObject(objId) {
        $.ajax({
            type: "POST",
            url: "/cloud/delStorageShareObject",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ObjectId: objId}),
            success: function (data) {
                if (!isResponseDataAvailable(data)) {
                    alertState("查找用户失败.问题描述: " + data.errorMsg, "failed");
                    return;
                }
                storagePage();
            },
            error: function () {
                alertState("查找用户失败，网络异常", "failed");
            }
        });
    }

    function rClickObjectMenu(context, e) {
        var space = cache_.getCurSpace();
        if ($(e.target).text() == "重命名")
            reNameObject(true, true);
        else if ($(e.target).text() == "删除") {
            delObject(space.activeObj.id);
        }
        else if ($(e.target).text() == "复制") {
            cache_.copyObject = {SrcId: space.activeObj.id};
        }
        else if ($(e.target).text() == "粘贴") {
            if (cache_.copyObject != undefined) //copyObjId
                copyObject(space.curParentId);
        }
        else if ($(e.target).text() == "共享") {
            shareObject(space.activeObj.id);
        }
        else if ($(e.target).text() == "取消共享") {
            cancelShareObject(space.activeObj.id);
        }
        else if ($(e.target).text() == "复制视频链接") {

        }
        else if ($(e.target).text() == "下载") {
            var FileCode=$(space.activeObj).data("FileCode");
            var Type=$(space.activeObj).data("Type");
            var DownloadUrl=$.getDownloadURL(FileCode,Type);
            $().downloadPermission(space.activeObj.id, 'storage', function(bSuccess){
                if (bSuccess)
                    window.open(DownloadUrl);
            });
        }
    }

    function before_rClickObjectMenu(e) {
        var space = cache_.getCurSpace();
        var tem, data;
        if (space.activeObj){
            tem = Template.get('template/storage/objectMenu.html');
            var tet =space.objectMap[space.activeObj.id];
            data = {
                bIsFile: (space.objectMap[space.activeObj.id].fileId != null),
                bPublic: (space.objectMap[space.activeObj.id].type == 0 && space.objectMap[space.activeObj.id].BShare),
                bShare: (cache_.shares[space.activeObj.id] != null),
                bShareSpace: (space.spaceType == shareSpace),
                bCanDownload: true,
                bCanDelete: true,
                bCanWrite: true,
                bCanShare: true
            };
            if (cache_.isShare()){
                if (!space.objectMap[space.activeObj.id].bWrite){
                    data['bCanDelete'] = false;
                    data['bCanWrite'] = false;
                    data['bCanShare'] = false;
                }
                if (!space.objectMap[space.activeObj.id].bDownload){
                    data['bCanDownload'] = false;
                }
            }

            if (!$().userHasRight("Sto_Download"))
                data["bCanDownload"] = false;
            if (!$().userHasRight("Sto_Share"))
                data["bCanShare"] = false;
            if (!$().userHasRight("Sto_Delete"))
                data["bCanDelete"] = false;
            if (!$().userHasRight("Sto_Write"))
                data["bCanWrite"] = false;
        }
        else{
            tem = Template.get('template/storage/commonMenu.html');
            data = {bHasCopyObject: (cache_.copyObject != undefined)};
            if (!data.bHasCopyObject)
                return;
        }
        var test = tem(data);
        $('#object-menu').html($.trim(test));
        $('#object-menu').mousedown(function(){
            return false;
        });
        $('#copyPathMenu').zclip({
            path: '//cdn.bootcss.com/zclip/1.1.2/ZeroClipboard.swf',
            copy: function(){
                return window.location.host + '/player/' + space.activeObj.id;
            },
            afterCopy: function(){
                return false;
            }
        });
        return true;
    }

    function onMouseDown_object(e) {
        var space = cache_.getCurSpace();
        var el_text;
        if (space.activeObj && space.activeObj != e.currentTarget) {
            $(space.activeObj).removeClass("active");
            el_text = $(space.activeObj).find(".cloud_object_text > p");
            el_text.removeClass("label-success");
//            el_text.addClass("label-primary");
        }
        $(e.currentTarget).addClass("active");
        space.activeObj = e.currentTarget;
        el_text = $(space.activeObj).find(".cloud_object_text > p");
//        el_text.removeClass("label-primary");
        el_text.addClass("label-success");
        showObjectDescription(true);
    }

    function showObjectDescription(bShow) {
        var e = $('#objectDescription');
        if (bShow){
            var space = cache_.getCurSpace();
            if (!space.activeObj)
                return;
            if (space.curParentId == shareSpaceId)
                return;

            var obj = space.objectMap[space.activeObj.id];
            var tem = Template.get('template/storage/object_property.html');
            var selector = "#" + obj.id;
            var Type=$(selector).data("Type");
            var Path=$(selector).data("ImagePath");
            var test = tem({IsService:cache_.IsService, obj:obj, flag:true, type: Type, category_1: cache_.Category_1, category_2: cache_.Category_2, tags: cache_.Tags});
            e.html($.trim(test));
            var objImage = Path;
            var left = 0, right = 0, top = 0, bottom = 0;
            if (Type == 0){
                initPortrait();
            }
            $("#editDescription").unbind("click").click(function(){
                $(".description_list").hide();
                $(".description_input,.des_edit").css("display", "block");
                expandCollapse($('#collapseOne'), true);
                return false;
            });
            $("#saveDescription").unbind("click").click(function(){
                saveDescription(obj);
                return false;
            });
            $("#cancelDescription").unbind("click").click(function(){
                cancelDescription();
                return false;
            });
            changeTag();
            changeCategory();
            $("#editShare").unbind("click").click(function(e){
                $(".share_list").hide();
                $(".share_input,.share_edit").css("display", "block");
                expandCollapse($('#collapseTwo'), true);
                return false;
            });
            $("#saveEditShare").unbind("click").click(function(){
                saveShare(obj);
                return false;
            });
            $("#cancelEditShare").unbind("click").click(function(){
                cancelShare();
                return false;
            });
            $("#editPrice").unbind("click").click(function(){
                $(".price_list").hide();
                $(".price_input,.price_edit").css("display", "block");
                expandCollapse($('#collapseThree'), true);
                return false;
            });
            $("#saveEditPrice").unbind("click").click(function(){
                savePrice(obj);
                return false;
            });
            $("#cancelEditPrice").unbind("click").click(function(){
                cancelPrice();
                return false;
            });
            $("#editVideo").unbind("click").click(function(){
                $(".video_list").hide();
                $(".video_input,.video_edit").css("display", "block");
                $('#tag_normal').css("display", "inline-block");
                expandCollapse($('#collapseFour'), true);
                return false;
            });
            $("#saveEditVideo").unbind("click").click(function(){
                saveVideo(obj, objImage ,left, right, top, bottom);
                return false;
            });
            $("#cancelEditVideo").unbind("click").click(function(){
                cancelVideo();
                return false;
            });
            $('.panel-heading').unbind('click').click(function(e){
                var collapse = $(e.currentTarget).parent().find('.panel-collapse');
                var expand = $(e.currentTarget).parent().find('#expand-span');
                if (collapse.hasClass('in')) {
                    collapse.collapse('hide');
                    expand.attr('class', 'glyphicon glyphicon-triangle-bottom');
                }
                else {
                    collapse.collapse('show');
                    expand.attr('class', 'glyphicon glyphicon-triangle-top');
                }
            });
        }
        function expandCollapse(collapse, bForce){
            var expand = collapse.parent().find('#expand-span');
            if (collapse.hasClass('in')) {
                if (!bForce){
                    collapse.collapse('hide');
                    expand.attr('class', 'glyphicon glyphicon-triangle-bottom');
                }
            }
            else {
                collapse.collapse('show');
                expand.attr('class', 'glyphicon glyphicon-triangle-top');
            }
        }
        function cancelShare(){
            $(".share_list").show();
            $(".share_input,.share_edit").css("display", "none");
        }
        function saveShare(obj){
            var objId = obj.id;
            var bshare = $(".share_check")[0].checked == true;
            $.ajax({
                type: "POST",
                url: "/cloud/modifyShareProperty",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    ObjectId: objId,
                    BShare: bshare,
                    Price: $('.price_edit').val()
                }),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("添加分享失败.问题描述: " + data.errorMsg, "info");
                        return;
                    }
                    alertState("添加分享操作完成", "success");
                    var obj = space.objectMap[data.Id];
                    obj.BShare = data.BShare;
                    obj.Price = data.Price;
                    var tem = Template.get('template/storage/o_p_share.html');
                    var property = $('.property_' + data.Id);
                    var selector = property.find("#collapseTwo");
                    var test = tem({obj:obj});
                    selector.html($.trim(test));
                },
                error: function () {
                    alertState("添加备注失败，网络异常", "failed");
                }
            });
            cancelShare();
        }
        function changeTag(){
            $('#tag_normal').change(function(){
                var tag = $('#tag_normal').val();
                var curTag = $('.category_edit').val();
                $('.category_edit').val(curTag + ' ' + tag);
            });
        }
        function changeCategory(){
            $('#category_1').change(function(){
                $('#category_2').html('');
                var category_1 = $('#category_1').val();
                if(category_1 != '')
                    $.each(cache_.Category_2, function(key, value){
                        if (value.ParentId == category_1){
                            $('#category_2').append(
                                '<option value="' + value.Id + '">' + value.Name + '</option>'
                            );
                        }
                    });
            });
        }
        function initPortrait(){
            var jnext = JcropWarp();
            jnext.title = '修改视频图标';
            jnext.useAge = 'objectVideo';
            jnext.ratio = 1;
            jnext.uploadBtn = 'objectVideo-btn';
            jnext.init(Path, $('#objectVideo_portrait'), function(p, l, t, r, b){
                objImage = p;
                left = l;
                right = r;
                top = t;
                bottom = b;
            });
            jnext.startSelect();
        }
        function cancelPrice(){
            $(".price_list").show();
            $(".price_input,.price_edit").css("display", "none");
        }
        function savePrice(obj){
            var objId = obj.id;
            $.ajax({
                type: "POST",
                url: "/cloud/modifyPriceProperty",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    ObjectId: objId,
                    bp: $('.basePrice_edit').val(),
                    scp: $('.schemePrice_edit').val(),
                    shp: $('.shotPrice_edit').val(),
                    acp: $('.actorPrice_edit').val(),
                    mp: $('.musicPrice_edit').val(),
                    aep: $('.aePrice_edit').val()
                }),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("修改报价失败.问题描述: " + data.errorMsg, "info");
                        return;
                    }
                    alertState("修改报价操作完成", "success");
                    var obj = space.objectMap[data.Id];
                    obj.BasePrice = data.BasePrice;
                    obj.ReferPrice = data.ReferPrice;
                    obj.SchemePrice = data.SchemePrice;
                    obj.ShotPrice = data.ShotPrice;
                    obj.ActorPrice = data.ActorPrice;
                    obj.MusicPrice = data.MusicPrice;
                    obj.AEPrice = data.AEPrice;
                    var tem = Template.get('template/storage/o_p_price.html');
                    var property = $('.property_' + data.Id);
                    var selector = property.find("#collapseThree");
                    var test = tem({obj:obj});
                    selector.html($.trim(test));
                },
                error: function () {
                    alertState("修改报价失败，网络异常", "failed");
                }
            });
            cancelPrice();
        }
        function cancelVideo(){
            $(".video_list").show();
            $(".video_input,.video_edit").css("display", "none");
        }
        function saveVideo(obj, objImage ,left, right, top, bottom){
            var camera = $('.camera_edit').val();
            var script = $('.script_edit').val();
            var tag = $('.category_edit').val();
            var category_1 = parseInt($('#category_1').val());
            var category_2 = parseInt($('#category_2').val());
            var objId = obj.id;
            $.ajax({
                type: "POST",
                url: "/cloud/modifyDescription",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    ObjectId: objId,
                    Camera: camera,
                    Script: script,
                    Tag: tag,
                    ObjImage: objImage,
                    Left: left,
                    Right: right,
                    Top: top,
                    Bottom: bottom,
                    Category_1: category_1,
                    Category_2: category_2
                }),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("添加备注失败.问题描述: " + data.errorMsg, "info");
                        return;
                    }
                    alertState("添加备注操作完成", "success");
                    var obj = space.objectMap[data.Id];
                    obj.camera = data.Camera;
                    obj.script = data.Script;
                    obj.tag = data.Tag;
                    obj.category_1 = data.Category_1;
                    obj.category_2 = data.Category_2;
                    $('#' + obj.id).find('.cloud_object_image').css('background-image', "url("+data.File.Path+')');
                    $('#' + obj.id).data("ImagePath",data.File.Path);
                    var tem = Template.get('template/storage/o_p_video.html');
                    var property = $('.property_' + data.Id);
                    var selector = property.find("#collapseFour");
                    var test = tem({obj:obj, type: 0, category_1: cache_.Category_1, category_2: cache_.Category_2, tags: cache_.Tags});
                    selector.html($.trim(test));
                    changeTag();
                    changeCategory();
                    initPortrait();
                },
                error: function () {
                    alertState("添加备注失败，网络异常", "failed");
                }
            });
            cancelVideo();
        }
        function cancelDescription(){
            $(".description_list").show();
            $(".description_input,.des_edit").css("display", "none");
        }
        function saveDescription(obj){
            var description = $('.description_edit').val();
            var objId = obj.id;
            $.ajax({
                type: "POST",
                url: "/cloud/modifyBase",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    ObjectId: objId,
                    Description: description
                }),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("添加备注失败.问题描述: " + data.errorMsg, "info");
                        return;
                    }
                    alertState("添加备注操作完成", "success");
                    var obj = space.objectMap[data.Id];
                    obj.description = data.Description;
                    var tem = Template.get('template/storage/o_p_base.html');
                    var property = $('.property_' + data.Id);
                    var selector = property.find("#collapseOne");
                    var test = tem({obj:obj, type: 0, category_1: cache_.Category_1, category_2: cache_.Category_2});
                    selector.html($.trim(test));
                },
                error: function () {
                    alertState("添加备注失败，网络异常", "failed");
                }
            });
            cancelDescription();
        }
    }

    ///上传成功初始化 界面
    function uploadFileSuccess(file, data) {
        if (!isResponseDataAvailable(data)) {
            alertState("上传文件操作失败", "failed");
            return;
        }
        $(data).each(function (index) {
            var objData = {
                Items: [
                {ParentId: cache_.getCurSpace().curParentId, Id: this.Id, Name: this.Name, FileId: this.FileId, File: this.File, Type: this.Type}
            ]};
            objData.navigateMode = curNavigateMode;
            objData.filterMode = curFilterMode;
            var tem = Template.get('template/storage/objectTree.html');
            var test = tem(objData);
            $('#objectTreeViewer').append($.trim(test));
            var selector = "#" + this.Id;
            //filecode
            $(selector).data("FileCode",this.File.FileCode);
            initObject(selector, this);
        });
        alertState("上传文件操作完成", "success");
    }

    function downloadFile(objId) {
        if (cache_.getCurSpace().objectMap[objId].fileId == null)
            return;
        var download = "/cloud/downloadFile?Id=" + objId + '&Context=Storage';
        if (cache_.isDomain())
            download = download + "&DomainId=" + cache_.getCurSpace().spaceId;
        if (cache_.isShare())
            download = download + "&ShareId=" + cache_.getCurSpace().objectMap[objId].shareObjectId;

        $("#iFrameDownload").attr("src", download);
    }

    //移动、删除操作会导致的obj变更
    function UpdateObjectState(modifyObjId) {
        var space = cache_.getCurSpace();
        if (space.copyObjId == modifyObjId)
            space.copyObjId = null;
        if (space.activeObj && space.activeObj.id == modifyObjId)
            space.activeObj = null;
    }

    function configureLevelTree(curObjId) {
        var space = cache_.getCurSpace();
        var objectInfo = space.objectMap[curObjId];
        space.levelTree = [];
        var i = 0;
        while (objectInfo && objectInfo.parentId != null) {
            space.levelTree[i] = {name: objectInfo.name, id: objectInfo.id};
            objectInfo = space.objectMap[objectInfo.parentId];
            i++;
        }
        space.levelTree[i] = {name: space.spaceName, id: space.rootObjId};

        var result = {data: [], active: -1, url: ""};
        result.url = "/mainPanelpage/";
        i = 0;
        for (var j = space.levelTree.length - 1; j >= 0; j--, i++) {
            result.data[i] = space.levelTree[j];
            result.url = result.url + "%" + result.data[i].id;
        }
        result.active = result.data[result.data.length - 1].id;
        result.dataSize = space.levelTree.length;
        return result;
    }

    function click_levelTreeItem(e) {
        $('#objectViewer').hide();
        getChildObject(e.currentTarget.id);
    }

    var storagePage_interface = {};
    storagePage_interface.filePickerDialog = {
        open: function (parent, success_callback, bDir) {
            $.ajax({
                type: "POST",
                url: "/cloud/getDBList",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({}),
                success: function (data) {
                    if (!isResponseDataAvailable(data)) {
                        alertState("取DBLIST失败.问题描述: " + data.errorMsg, "failed");
                        return;
                    }
                    //解析DBList信息
                    parseDBListInfo(data);
                    if ($.isFunction(success_callback)) {
                        var t = Template.get('template/storage/filepickerdialog.html');
                        parent.html(t({'curSpace': cache_.curSpace, 'spaces': cache_.spaces, bDir: bDir}));
                        var selected_file = null;

                        function initFileTree() {
                            $('#filepickerDialog_filetree').replaceWith('<div id="filepickerDialog_filetree"></div>');
                            $('#filepickerDialog_filetree').jstree({
                                "core": {
                                    "animation": 0,
                                    "check_callback": true,
                                    "themes": { "stripes": true },
                                    'data': function (obj, callback) {
                                        if (cache_.curSpace == undefined) {
                                            cache_.curSpace = 0;
                                        }
                                        var space = cache_.getCurSpace();
                                        var parentId = null;
                                        if (obj.id == '#') {
                                            parentId = space.rootObjId;
                                        } else {
                                            parentId = obj.id;
                                        }
                                        var param = {
                                            Id: parentId,
                                            Page: 1,
                                            PageStep: 200,
                                            IsDeep: false
                                        };
                                        $.ajax({
                                            type: "POST",
                                            url: "/cloud/childObjects",
                                            dataType: "json",
                                            contentType: "application/json",
                                            data: JSON.stringify(param),
                                            success: function (d) {
                                                var dirItems = [];
                                                $.each(d.Items, function (i, item) {
                                                    item.data = item;
                                                    item.text = item.Name;
                                                    item.id = item.Id;
                                                    item.type = item.FileId == null ? "default" : "file";
                                                    cache_.getCurSpace().objectMap[item.Id] = item;
                                                    if (item.type != "file") {
                                                        item.children = true;
                                                    }
                                                    if (bDir && item.type != "file")
                                                        dirItems.push(item);
                                                });
                                                if (!bDir)
                                                    callback.call(this, d.Items);
                                                else
                                                    callback.call(this, dirItems);
                                            },
                                            error: function () {
                                                alertState("获取目录内容失败，网络异常", "failed");
                                            }
                                        });
                                    }
                                },
                                "types": {
                                    "#": {
                                        "valid_children": ["default"]
                                    },
                                    "default": {
                                        "valid_children": ["default", "file"]
                                    },
                                    "file": {
                                        "icon": "glyphicon glyphicon-file",
                                        "valid_children": []
                                    }
                                },
                                "plugins": [
                                    "contextmenu", "dnd", "search",
                                    "state", "types", "wholerow"
                                ]
                            }).on('changed.jstree', function (e, data) {
                                if (data && data.selected && data.selected.length) {
                                    selected_file = data.selected;
                                }
                            });
                        }

                        $('#filePicker_SpaceSelector').find('button').click(function (e) {
                            var space = $(e.currentTarget).val();
                            cache_.curSpace = +space;
                            initFileTree();
                        });
                        initFileTree();
                        $('#filepickerDialog_confirm').unbind('click').click(function (e) {
                            var files = [];
                            if (selected_file){
                                $.each(selected_file, function(n, value){
                                    var obj = cache_.getCurSpace().objectMap[value];
                                    if (bDir && !obj.FileId){
                                        files.push({
                                            Name: obj.Name,
                                            Id: value,
                                            Type: obj.Type,
                                            CreateTime: obj.CreateTime,
                                            Description: "",
                                            IsDir: true
                                        });
                                    }
                                    else if (!bDir && obj.FileId){
                                        files.push({
                                            Name: obj.Name,
                                            Id: value,
                                            Type: obj.Type,
                                            CreateTime: obj.CreateTime,
                                            Description: "",
                                            Path: obj.File.Path,
                                            IsDir: false
                                        });
                                    }
                                });
                            }
                            success_callback(files);
                        });
                        $('#filepickerDialog_cancel').unbind('click').click(function (e) {
                            success_callback([]);
                        });
                    }
                },
                error: function () {
                    alertState("取DBLIST失败.网络异常", "failed");
                }
            });
        }
    };
    storagePage_interface.pageRouter = {
        '/storagePage': storagePage
    };
    storagePage_interface.pageCache = cache_;
    return storagePage_interface;
});
