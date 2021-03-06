<?php
namespace Chat\Controller;
use Think\Controller;
class ProductController extends BaseController
{
    public function __construct()
    {
        parent::__construct();
        $this->video=D('video');

    }
    public function ajax(){
        $course=D('course')->order('createtime desc')->select();


        $article=D('article')->order('createtime desc')->select();



        $activity=D('video_activity')->order('starttime desc')->select();

        $re=array(
            0=>$course,
            1=>$article,
            2=>$activity
        );
        $this->ajaxReturn($re);

    }
    public function index()
    {

        $course=D('course')->order('createtime desc')->select();
//        foreach ($course as $key=>$item){
//            $course[$key]['createtime']=(date("Y-m-d",$item['createtime']));
//        }
        $this->assign('course',$course);

        $article=D('article')->order('createtime desc')->select();

        $this->assign('article',$article);




        $activity=D('video_activity')->order('starttime desc')->select();

        $this->assign('activity',$activity);


//        $data=$this->video->
//        query("SELECT*
//                            FROM  `video`
//                            WHERE   `publish_state`=1 and activity_title=''
//                            ORDER BY confirm_time DESC");
//
//
//        $this->assign('data',$data);


        $this->display();

    }

    public function activity($title)
    {

        $data=$this->video->

        query("SELECT*
                            FROM  `video`  a
                            INNER JOIN `video_activity` b
                            ON  a.activity_title=b.title
                            WHERE   a.activity_title='$title'
                            AND a.`publish_state`=1
                            ORDER BY confirm_time DESC");

        foreach ($data as $key=>$item){
            $praises=D('video_praise')->where(array('video_id'=>$item['video_id']))->select();
            $data[$key]['praise_count']=count($praises);
        }
        $this->assign('data',$data);



        $this->display();

    }

    public function video($video_id)
    {
        session('video_id',$video_id);
//        session('openid',"oAdCq01YzcVjLWljmeEBFcDEswEY");

        $data=$this->video->where(array('video_id'=>$video_id))->find();
        $data['view_count']+=1;
        $this->video->save($data);
        $this->assign('data',$data);
        $this->assign('ispraise',$this->video->isPraise());
        $this->assign('praise_count',count($this->video->getPraise()));
        $this->assign('comments',$this->video->getComments());

        $this->display();



    }

    public function praise(){
        $data['video_id']=session('video_id');
        $data['openid']=session('openid');
        $this->video->addPraise($data);
        exit('ok');

    }

    public function addcomment(){
        if(I('post.')){
            $data=D('video_comment')->create();
            $data['video_id']=session('video_id');
            $data['openid']=session('openid');
            $userinfo=D('user')->getUser();
            $data['chatname']=$userinfo['chatname'];
            $data['profile']=$userinfo['profile'];
            $this->video->addComment($data);
            $this->redirect('Chat/Product/video?video_id='.session('video_id'));
        }
        $this->display();

    }


}