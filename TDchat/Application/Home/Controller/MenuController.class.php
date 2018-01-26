<?php
namespace Home\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');

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
                    'name' => '筑影天地',
                    'sub_button' => array (
                        0 => array (
                            'type' => 'view',
                            'name' => '热点聚焦',
                            'url' => 'http://www.jianpianzi.com/tpchat/index.php/Chat/article'
                        ),
                        1 => array (
                            'type' => 'view',
                            'name' => '作品集锦',
                            'url' => 'http://www.jianpianzi.com/tpchat/index.php/Chat/product'                       ),
                        2 => array (
                            'type' => 'view',
                            'name' => '筑影FM',
                            'url' => 'http://www.ximalaya.com/zhubo/93586430/'
                                                  )
                    )
                ),
                  1 => array (
                      'type' => 'view',
                      'name' => '筑影学堂',
                      'url' =>  'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/chat&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'
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
     	);
        var_dump($this->weObj->createMenu($data));
    }
}