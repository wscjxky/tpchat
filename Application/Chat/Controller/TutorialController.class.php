<?php
// 本类由系统自动生成，仅供测试用途
namespace Chat\Controller;
use Think\Controller;
class tutorialController extends Controller {
    public function __construct()
    {
        parent::__construct();
        $this->tutorial=D('tutorial');
    }

    public function index()
    {
        $data=$this->tutorial->order('createtime desc')->select();
        $this->assign('data',$data);
        $this->display();
    }
}
