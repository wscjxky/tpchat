<?php
namespace Home\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');

class MaterialController extends Controller {
    public function index()
    {
        $weObj = new \Wechat();
        var_dump($weObj->getForeverList('news',0,5));
    }


}