<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006-2014 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: liu21st <liu21st@gmail.com>
// +----------------------------------------------------------------------
header("Content-type:text/html;charset=utf-8");

// 应用入口文件

// 检测PHP环境
if(version_compare(PHP_VERSION,'5.3.0','<'))  die('require PHP > 5.3.0 !');

// 开启调试模式 建议开发阶段开启 部署阶段注释或者设为false
define('APP_DEBUG',True);

// 定义应用目录
define('APP_PATH','./Application/');
define('DEFAULT_MODULE' , 'Home');
define('MODULE_ALLOW_LIST' , array('Home','Admin'));
//给系统资源文件路径定义成常量
//前台
define("SITE_URL","http://182.92.97.97/");
define("CSS_URL",SITE_URL."tpchat/Public/css/");
define("IMG_URL",SITE_URL."tpchat/Public/img/");
define("JS_URL",SITE_URL."tpchat/Public/js/");
//后台
define("ADMIN_CSS_URL",SITE_URL."tpchat/Admin/Public/css/");
define("ADMIN_IMG_URL",SITE_URL."tpchat/Admin/Public/img/");
define("ADMIN_JS_URL",SITE_URL."tpchat/Admin/Public/js/");

// 引入ThinkPHP入口文件
require './ThinkPHP/ThinkPHP.php';

$_SERVER['PATH_INFO'] = $_SERVER['REQUEST_URI' ];
// 亲^_^ 后面不需要任何代码了 就是如此简单