<?php
namespace Chat\Controller;
use Think\Controller;
class UserController extends BaseController {
    public function __construct()
    {
        parent::__construct();
        $this->user=D('user');

        define("OPEN_ID",session('openid'));
        $this->openid=OPEN_ID;
    }

    public function index(){

        $data=$this->user->getUser();
        $this->assign('data',$data);
        $this->display();

    }
    public function userinfo(){
        $data=$this->user->getUser();
        $data['user_level']=$this->user->getLevel();
        $this->assign('data',$data);
        $this->display();
    }
    public function trade(){
        $trade=$this->user->getTrade();
        $this->assign('data',array_reverse($trade));
        $this->display();
    }
    public function tradeInfo(){
        $trade_id=I('get.trade_id');
        $trade=D('trade')->where(array('trade_id'=>$trade_id))->find();
        $course=D('course')->where(array('course_id'=>$trade['course_id']))->find();
        $evidencelist=explode(',',$trade['evidence']);
        $this->assign('course',$course);

        $this->assign('data',$trade);
        $this->assign('evidencelist',$evidencelist);



        $this->display();
    }


    public function point(){
        $data=$this->user->getUser();
        if($data)
            $this->assign('data',$data);
        $this->display();
    }
    public function cash(){
        $data=$this->user->getUser();
        if($data)
            $this->assign('data',$data);
        if(I('post.')){
                $user=$this->user->getUser();
                $user['cash_submit']=I('post.cash_current');
                $user['cash_current']=0;
                D('user')->save($user);
                exit(I('post.cash_current'));
        }
        $this->display();
    }
    public function video(){
        $data=$this->user->getVideo();
        $this->assign('data',$data);
        $this->assign('open_id',session('openid'));
        $this->display();
    }
    public function addvideo(){
        $user=$this->user->getUser();
        $this->assign('chatname',$user['chatname']);
        $this->assign('open_id',session('openid'));
        $this->assign('profile',$user['profile']);

        if(I('post.')) {
            $video = M('video');
            if ($video->create()) {
                $video->add();
            }
        }
        $this->display();
    }

    public function advice(){
        $this->assign('open_id',session('openid'));

        $data=$this->user->getAdvice();
        if($data)
            $this->assign('data',$data);
        $this->display();
    }

    public function addadvice(){
        $this->assign('open_id',session('openid'));
        echo '$("#activity").select({
        title: "选择活动",
        items: ["    ","默活动"]
    });';
        if(I('post.')) {
            $video = M('advice');
            if ($video->create()) {

                $video->add();
            }
        }
        $this->display();
    }
    public function register(){
        $this->assign('open_id',session('openid'));
        $data=D('evidence')->query("SELECT*
                            FROM  `evidence`  a

                            INNER JOIN `course` b

                            ON  a.course_id=b.course_id
                            WHERE a.openid='$this->openid'");
        $this->assign('data',$data);
        $this->display();
    }
    public function registerinfo(){
        $data=D('evidence')->query("SELECT*
                            FROM  `evidence`  a

                            INNER JOIN `course` b

                            ON  a.course_id=b.course_id
                            WHERE a.evidence_id=".I('get.evidence_id'));
        $this->assign('course',$data);
        $this->display();
    }
}