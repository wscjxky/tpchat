<?php
// 本类由系统自动生成，仅供测试用途
namespace Chat\Controller;
use Think\Controller;
class ArticleController extends Controller {
    public function __construct()
    {
        parent::__construct();
        $this->article=D('article');
    }

    public function index()
    {
        $data=$this->article->select();
        $this->assign('data',$data);
        $this->display();


        }





}
