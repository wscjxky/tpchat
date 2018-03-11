<?php
namespace Home\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');
date_default_timezone_set("Asia/Shanghai");
class MenuController extends Controller{

    private $weObj;
    public function __construct()
    {
        parent::__construct();
        $this->weObj = new \Wechat();
    }

    public function index(){
        var_dump( $this->weObj->getMenu());
    }
    public function create(){
        $data=array (
      	    'button' => array (
                0 => array (
                    'name' => '筑影学院',
                    'sub_button' => array (
                        0 => array (
                            'type' => 'view',
                            'name' => '我的校外课',
                            'url' => 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/Chat/article&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'

                        ),
                        1 => array (

                            'type' => 'view',
                            'name' => '在线教程',
                            'url' => 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/Chat/product&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'                       ),
                        2 => array (
                            'type' => 'view',
                            'name' => '小主持人FM',
                            'url' => 'http://www.ximalaya.com/zhubo/93586430/'
                        ),
                        3 => array (

                            'type' => 'view',
                            'name' => '直播课堂',

                        )
                    )
                ),
                1 => array (
                'name' => '媒体校园',
                'sub_button' => array (
                0 => array (

                    'type' => 'view',
                    'name' => '活动推送',
                ),
                1 => array (
                    'type' => 'view',
                    'name' => '热点报道',
                    'url' => 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/Chat/article&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'

                )
                ),


            2=> array (
                'name' => '联系我们',
                'sub_button' => array (
                    0 => array (
                        'type' => 'click',
                        'name' => '商务合作',
                        'key' => 'commerce'                    ),
                    1 => array (
                        'type' => 'click',
                        'name' => '在线问答',
                        'key' => 'chat'                    ),
                    2 => array (
                        'type' => 'click',
                        'name' => '关于我们',
                        'key' => 'aboutus'                    ),

                    )
                )
            )
     	)
        );
        var_dump($this->weObj->createMenu($data));
    }
}