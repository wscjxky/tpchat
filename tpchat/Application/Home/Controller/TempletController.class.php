<?php
namespace Home\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');

class TempletController extends Controller {
    public function __construct()
    {
        parent::__construct();
        $this->weObj=new \Wechat();
    }
    public function index(){
        $data=array (
            'touser' => "oAdCq016X8Hgd9iVKRk6Ob-r-sNU",
            'template_id' => "Uv50VGgxnVFYF-zxsKd5PSyowrVJ6-Pvc_fqIEGA934",
            'url' => "http://www.cunpianzi.com/tpchat/index.php/admin",
            'appid' => "wxfdf007a79f182aed",
            'pagepath' => "",
            'data' => array(
                "first"=>array("value"=>"后台账号为  admin", "color"=>"#173177"),
                "keyword1"=>array("value"=>"密码为 zyxt123", "color"=>"#142577"),
                "keyword2"=>array("value"=>"测试", "color"=>"#178577"),
                "keyword3"=>array("value"=>"测试", "color"=>"#173587")

            )
        );

        var_dump($this->weObj->sendTemplateMessage($data));
        $data=array (
            'touser' => "oAdCq08z0miP9AerKiRV0akkB4EI",
            'template_id' => "Uv50VGgxnVFYF-zxsKd5PSyowrVJ6-Pvc_fqIEGA934",
            'url' => "http://www.cunpianzi.com/tpchat/index.php/admin",
            'appid' => "wxfdf007a79f182aed",
            'pagepath' => "",
            'data' => array(
                "first"=>array("value"=>"后台账号为  admin", "color"=>"#173177"),
                "keyword1"=>array("value"=>"密码为 zyxt123", "color"=>"#142577"),
                "keyword2"=>array("value"=>"测试", "color"=>"#178577"),
                "keyword3"=>array("value"=>"测试", "color"=>"#173587")

            )
        );

        var_dump($this->weObj->sendTemplateMessage($data));

}
#173177

}