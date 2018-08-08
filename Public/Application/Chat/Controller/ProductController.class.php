<?php
namespace Chat\Controller;
use Think\Controller;
class ProductController extends Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->video=D('video');

    }
    public function index()
    {


        $data=$this->video->query("SELECT*
              from `video`  
WHERE  check_status='审核通过'"
);
        $this->assign('data',$data);
        $this->display();



    }


}