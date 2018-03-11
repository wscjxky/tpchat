<?php
namespace Home\Controller;
use Think\Controller;

class RedirectController extends Controller {


    public function share()
    {
        $this->assign('openid',$_GET['openid']?$_GET['openid']:'error');
        $this->display();
    }
}