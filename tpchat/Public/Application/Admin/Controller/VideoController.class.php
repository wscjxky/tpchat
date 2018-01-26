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

class VideoController extends BaseController
{

    public function __construct()
    {
        parent::__construct();
        $this->video = D('video');

    }

    public function index()
    {

        $data = D('video')->select();
        $this->assign('data', $data);
        $this->assign('count', count($data));
        $this->display();
    }


    public function addVideo()
    {
        if (I('post.')) {
            $this->uploadimg();
            $data = $this->video->create();
            $this->video->add($data);  //add()返回新纪录的主键id值
            $this->success("添加成功", U('Video/index'));
        }
        $this->display();
    }

    public function video_info()
    {
        $video_id = I('get.id');
        $act = I('get.act');
        $this->assign('act', $act);
        $this->assign('video_id', $video_id);
        $video=$this->video->where(array('video_id'=>$video_id))->find();
        $this->assign('data', $video);

        if (I('post.')) {
            if ($act == 'refuse') {
                $data = $this->video->create();
                $data['check_status'] = "审核未通过";
                $this->video->where(array('video_id' => I('post.video_id')))->save($data);
                $this->success("审核成功", U('Video/index'));
            } else if ($act == 'pass') {
                $this->uploadimg();
                $data = $this->video->create();
                $data['video_id'] = I('post.video_id');
                $data['check_status'] = "审核通过";
                $this->video->where(array('video_id' => I('post.video_id')))->save($data);
                $this->success("审核成功", U('Video/index'));
            }
            else{
                $this->uploadimg();
                $data = $this->video->create();
                $this->video->where(array('video_id' => I('post.video_id')))->save($data);
                $this->success("修改成功", U('Video/index'));
            }
        }
        $this->display();
    }

    public function uploadimg()
    {
        $upload = new \Think\Upload(); // 实例化上传类
        $upload->maxSize = 3145728; // 设置附件上传大小
        $upload->exts = array('jpg', 'gif', 'png', 'jpeg'); // 设置附件上传类型
        // 设置附件上传根目录
        $upload->rootPath = UP_PATH;
        // 上传单个文件
        $info = $upload->uploadOne($_FILES['image']);
        if (!$info) {
            // 上传错误提示错误信息
            $data['code'] = 0;
            $data['content'] = $upload->getError();
            var_dump($data);
        } 
        else {
            // 上传成功 获取上传文件信息
            $picpathname = UP_PATH . $info['savepath'] . $info['savename'];
            $_POST['image'] = $picpathname;
        }
    }

















































}