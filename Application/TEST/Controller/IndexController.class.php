<?php
namespace TEST\Controller;
use Think\Controller;
class IndexController extends Controller {
    public function index(){
        $this->display();
    }
    public function test(){
        $this->assign('test',123123);
        $this->display();
    }
    public function post(){
        $this->assign('test','表单提交功能');
        $this->display();
    }
    public function result(){
        if(I('post.')) {
            $value_name = I('post.name');
            $value_age = I('post.age');
        }
        $this->assign('name',$value_name);
        $this->assign('age',$value_age);
        $this->display();
    }
    public function get1(){
        if(I('get.')) {
            $value_name = I('get.name');
            $value_age = I('get.age');
        }
        $this->assign('name',$value_name);
        $this->assign('age',$value_age);
        $this->display();
    }

    public function getre(){
        $this->assign('test','表单提交功能get方法');
        $this->display();
    }
    public function action1(){
        $this->display();
    }
    public function foreach1(){
        $arr=['11','22','33','44'];
        $dic=['a'=>1,'b'=>2,'c'=>3,'b'=>4];
        $this->assign('arr',$arr);
        $this->assign('dic',$dic);
        $this->display();
    }

}