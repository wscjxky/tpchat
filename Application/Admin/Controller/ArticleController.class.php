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
    public function publish(){
        if($id=I('post.id')){
            $course= $this->article->where(array('article_id'=>$id))->find();
            if( $course['publish_state']==0)
                $course['publish_state']=1;
            else{
                $course['publish_state']=0;
            }
            $this->article->save($course);
            exit('ok');
        }
        else
            exit();

    }
    public function index()
    {
        $data=$this->article->order('createtime desc')->select();
        $this->assign('data',$data);
        $this->display();
    }
}
