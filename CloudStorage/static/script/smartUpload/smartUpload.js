/*
 * smartUpload v1.0
 * Copyright (c) 2014 huiTen All rights reserved.
 * Released under the MIT license.
 * Date: 2014.12.1
 */
(function ($) {
    $.fn.smartUpload = function (options) {
        var pluginIdentity = "smartUpload";
        var fui = $('#smFloating_list');
        var instance = null;
        if (fui.length != 0)
            instance = fui.data(pluginIdentity);
        if (!instance)
            return fui.data(pluginIdentity, smartUpload_plugin.createInstance(this, options));
        else
            instance.init(this, options);
        return this;
    };

    var smartUpload_plugin = {
        createInstance: function (element, options) {
            var TaskState = {init: 0, uploading: 1, pause: 2, finish: 3, closing: 4};
            var su = {};
            su.default = {
                blockSize: 1024 * 1024,
                uploadSuccess: function (task) {
                },
                uploadFailed: function (task) {
                },
                getFileInfoUrl: "",
                uploadFileUrl: "",
                userData: "",
                template: 0
            };
            su.options = $.extend(true, {}, su.default, options);
            su.tasks = [];
            su.elDetail = null;
            su.init = function(el, userData){
                su.options = $.extend(true, {}, su.default, userData);
                su.ui(el);
            };

            su.ui = function (el) {
                su.el = $(el);
                this.el.html('<div class="btn-group">' +
                    '<input type="file" multiple="multiple" id="smFile">' +
                    '<button type="button" id="smBtn" class="btn btn-success" style="border-radius:4px 0 0 4px;">智能上传</button>' +
                    '<button type="button" id="smdBtn" class="btn btn-success"><span id="smBadge" class="badge">0</span></button>' +
                    '</div>');
                su.elf = $('#smFile');
                su.elbtn = $('#smBtn');
                su.eldBtn = $('#smdBtn');
                su.elBadge = $('#smBadge');
                su.elf.css('width', su.elbtn.css('width'));
                su.elf.css('height', su.elbtn.css('height'));
                su.elf.css("opacity", 0);
                su.elf.css("position", 'absolute');
                su.elf.css("cursor", 'pointer');
                su.elBadge.text(su.tasks.length);
                su.elbtn.unbind('click').click(function () {
                    su.elf.trigger('click');
                });
                su.eldBtn.unbind('click').click(function () {
                    su.showDetail(true);
                });
                su.elf.unbind('change').change(function (event) {
                    add_file_(event);
                });
            };

            su.floating_ui = function(){
                var fui = $('#smFloating_list');
                if (fui.length == 0)
                    $('body').append('<div id="smFloating_list" title="上传任务列表"></div>');
                $('#smFloating_list').unbind('click').click(function(){
                    su.showDetail(true);
                });
            };

            su.options.template.helper("ToKB", function (size){
                var mbSize = size / 1024;
                return mbSize.toFixed(2) + "KB";
            });

            su.showDetail = function (bShow) {
                if (!su.elDetail)
                    $('body').append('<div class="modal fade bs-example-modal-sm" id="smDetail"></div>');
                su.elDetail = $('#smDetail');
                var tem = su.options.template.get('script/smartUpload/uploadDetail.html');
                var alltask = [];
                $.each(su.tasks, function (index, value) {
                    alltask.push(su.tasks[value]);
                });
                var html = tem(alltask);
                su.elDetail.html($.trim(html));

                $('.smPause').unbind('click').click(function (e) {
                    var taskId = $(e.currentTarget).parent().find('input').val();
                    var task = su.tasks[taskId];
                    if (su.isPause(task) || su.isInit(task)) {
                        getFileInfo_(task);
                    }
                    else if (su.isUploading(task)) {
                        su.toPause(task);
                    }
                });
                $('.smClose').unbind('click').click(function (e) {
                    var taskId = $(e.currentTarget).parent().find('input').val();
                    var task = su.tasks[taskId];
                    su.toClosing(task);
                });
                $('#smStopAll').unbind('click').click(function (e) {
                    $.each(su.tasks, function (index, value) {
                        su.toPause(su.tasks[value]);
                    });
                });
                $('#smCancelAll').unbind('click').click(function (e) {
                    var alltask = [];
                    $.each(su.tasks, function (index, value) {
                        alltask.push(su.tasks[value]);
                    });
                    $.each(alltask, function (index, value) {
                        su.toClosing(alltask[index]);
                    });
                });
                if (bShow)
                    su.elDetail.modal('show');
            };

            su.toInit = function (task) {
                if (task.state == TaskState.init)
                    return;
                task.state = TaskState.init;
                task.startPos = 0;
                task.endPos = task.size;
                task.percent = 0;
                su.showDetail(false);
            };
            su.toPause = function (task) {
                if (task.state == TaskState.pause)
                    return;
                task.state = TaskState.pause;
                su.showDetail(false);
            };
            su.toUpload = function (task) {
                if (task.state == TaskState.uploading)
                    return;
                task.state = TaskState.uploading;
                su.showDetail(false);
            };
            su.toFinish = function (task, response) {
                if (task.state == TaskState.finish)
                    return;
                task.state = TaskState.finish;
                task.percent = 100;
                task.endPos = task.size;
                su.showDetail(false);
                su.options.uploadSuccess(task, response.data);
            };
            su.toClosing = function (task) {
                if (task.state == TaskState.closing)
                    return;
                if (!su.isUploading(task))
                    removeTask(task.id);
                else
                    task.state = TaskState.closing;
            };
            su.isPause = function (task) {
                return task.state == TaskState.pause;
            };
            su.isUploading = function (task) {
                return task.state == TaskState.uploading;
            };
            su.isInit = function (task) {
                return task.state == TaskState.init;
            };
            su.isFinish = function (task) {
                return task.state == TaskState.finish;
            };
            su.isClosing = function (task) {
                return task.state == TaskState.closing;
            };
            //添加任务
            function add_file_(e) {
                var files = e.target.files;
                for (var index = 0; index < files.length; index++) {
                    var task = files[index];
                    var id = task.id = (task.lastModifiedDate + "").replace(/\W/g, '') + task.size + task.type.replace(/\W/g, '');
                    su.toInit(task);
                    if (su.tasks.indexOf(id) == -1) {
                        su.tasks.push(id);
                        task.arrayIndex = su.tasks.length - 1;
                        su.tasks[id] = task;
                        su.elBadge.text(su.tasks.length);
                        getFileInfo_(task);
                    }
                }
            }

            //取文件信息
            function getFileInfo_(task) {
                $.ajax({
                    type: "POST",
                    url: su.options.getFileInfoUrl,
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify($.extend(true, {}, {IdentityName: task.id, FileSize: task.size, FileName: task.name}, su.options.userData)),
                    success: function (response) {
                        cb_getFileInfo(task, true, response);
                    },
                    error: function (response) {
                        cb_getFileInfo(task, false, response);
                    }
                });
                function cb_getFileInfo(task, bSuccess, response) {
                    if (!bSuccess)
                        return;
                    if (!isResponseDataAvailable(response)) {
                        alertState("文件信息获取失败.描述:" + response.errorMsg, "failed");
                        return;
                    }
                    if (response.Size == undefined || response.Id == undefined)
                        return;
//                    if (task.size <= response.Size) {
//                        su.toFinish(task);
//                        return;
//                    }
                    task.startPos = response.Size;
                    task.fileId = response.Id;
                    upload(task);
                }
            }

            //上传接口
            function upload(task) {
                su.toUpload(task);
                task.endPos = task.startPos + su.options.blockSize;
                if (task.endPos > task.size)
                    task.endPos = task.size;
                var data = new FormData();
                data.append("fileName", task.name);
                data.append("identityName", task.fileId);
                data.append("file", task.slice(task.startPos, task.endPos));
                data.append("start", task.startPos);
                data.append("size", task.endPos - task.startPos);
                $.each(su.options.userData, function (key, value) {
                    data.append(key, value);
                });
                $.ajax({
                    type: "POST",
                    url: su.options.uploadFileUrl,
                    contentType: false,
                    data: data,
                    processData: false,
                    xhrFields: {
                        onprogress: function (e) {
                            uploadProgress(task, e.loaded / e.total);
                        }
                    },
                    success: function (response) {
                        cb_upload(task, true, response);
                    },
                    error: function (response) {
                        cb_upload(task, false, response);
                    }
                });
                function cb_upload(task, bSuccess, response) {
                    if (!bSuccess) {
                        su.toInit(task);
                        return;
                    }
                    if (!isResponseDataAvailable(response) || response.Size == undefined) {
                        alertState("传输出现问题.描述:" + response.errorMsg, "failed");
                        su.toInit(task);
                        return;
                    }
                    task.startPos = response.Size;
                    if (task.startPos >= task.size) {
                        su.toFinish(task, response);
                        return;
                    }
                    if (su.isUploading(task))
                        upload(task);
                    if (su.isClosing(task))
                        removeTask(task.id);
                }

                function uploadProgress(task, percent) {
                    if (task.size > 0)
                        task.percent = ((task.endPos - task.startPos) * percent + task.startPos) / task.size * 100;
                    else
                        task.percent = 0;
                    var progress = "#" + task.fileId + "_smProgress";
                    $(progress).find('.progress-bar').attr('aria-valuenow', task.percent);
                    $(progress).find('.progress-bar').css('width', task.percent + '%');
                }
            }

            function removeTask(id) {
                var task = su.tasks[id];
                su.tasks.splice(task.arrayIndex, 1);
                delete su.tasks[id];
                $.each(su.tasks, function (index, value) {
                    su.tasks[value].arrayIndex = index;
                });
                su.elBadge.text(su.tasks.length);
                su.showDetail(false);
            }

            su.ui(element);
            su.floating_ui();
            return su;
        }
    };
})(jQuery);