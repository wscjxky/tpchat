<?php
/**
 * Created by PhpStorm.
 * User: hhh
 * Date: 2017/8/17
 * Time: 上午9:47
 */

namespace  Admin\Controller;


use Think\Controller;
use Think\Verify;
use Think\Db;
use Think\Session;

class ActivityController extends BaseController
{

    public function __construct()
    {
        parent::__construct();
        $this->activity = D('video_activity');

    }

    public function index()
    {

        $data = $this->activity->order('createtime desc')->select();
        $this->assign('data', $data);
        $this->assign('count', count($data));
        $this->display();
    }

    public function publish(){
        if($id=I('post.id')){
            $course= $this->course->where(array('course_id'=>$id))->find();
            if( $course['publish_state']==0)
                $course['publish_state']=1;
            else{
                $course['publish_state']=0;
            }
            $this->course->save($course);
            exit('ok');
        }
        else
            exit();

    }
    public function activityHandle(){
        $data=I('post.');
        $activity_id = I('post.id');
        $act = I('post.act');

        if($act == 'update') {
            unset($data['act']);
            $r = $this->activity->where(array('activity_id'=>$activity_id))->save($data);
            $this->success("操作成功",U('Activity/index'));

        }
        else if($act == 'publish'){

            $activity= $this->activity->where(array('activity_id'=>$activity_id))->find();

            if( $activity['publish_state']==0)
                $activity['publish_state']=1;
            else{
                $activity['publish_state']=0;
            }
            $this->activity->save($activity);
            exit('ok');

        }
        else if($act == 'del'){
            $r = $this->activity->where(array('activity_id'=>$activity_id))->delete();
            if($r){
                exit(json_encode(1));
            }else{
                exit(json_encode("删除失败"));
            }
        }
        else if($act == 'add'){
            $this->uploadimg();
            $data=I('post.');
            unset($data['activity_id']);
            $r = $this->activity->add($data);
        }
        if($r){
            $this->success("操作成功",U('Activity/index'));
        }
    }
    public function uploadimg(){
        $upload = new \Think\Upload(); // 实例化上传类
        $upload->maxSize = 51200; // 设置附件上传大小
        $upload->exts = array('jpg', 'gif', 'png', 'jpeg'); // 设置附件上传类型
        // 设置附件上传根目录
        $upload->rootPath = UP_PATH;

        // 上传单个文件
        $info = $upload->uploadOne($_FILES['activity_image']);
        if (!$info) {// 上传错误提示错误信息
            $data['code'] = 0;
            $data['error'] = $upload->getError();
            exit($data['error']."请返回重试");
        }
        else{
            $picpathname = UP_PATH . $info['savepath'] . $info['savename'];
            $_POST['activity_image'] = $picpathname;
        }
    }

    public function activity_info()
    {
        $activity_id = I('get.id/d');

        if(!empty($activity_id)){
            $info = $this->activity->where(array("activity_id"=> $activity_id))->find();
            $this->assign('data',$info);
        }


        $act = empty($activity_id) ? 'add' : 'update';
        $this->assign('act',$act);

        $this->display();
    }

}
