<?php
/**
 * Created by PhpStorm.
 * User: hhh
 * Date: 2017/8/17
 * Time: 下午1:48
 */

namespace Admin\Controller;

use stdClass;

class CourseController extends BaseController
{
    public function __construct() {
        parent::__construct();
        // 订单 支付 发货状态

        $this->course=D('course');

    }

    /*
     *订单首页
     */
    public function index(){
        $data= $this->course->select();
        $this->assign('data',$data);
        $this->assign('count',count($data));

        $this->display();
    }


    public function addCourse(){
//        var_dump($_SERVER['DOCUMENT_ROOT'].'/tpchat/Public/up');

//        两个逻辑：展示表单、收集表单
        if(!empty($_POST)){
            var_dump(I('post.'));
            //实现附件上传处理
//            if($_FILES['image']['error']!=4){
                var_dump($_FILES['image']);
                //A.实现图片上传
                $upload = new \Think\Upload(); // 实例化上传类
                $upload->maxSize = 3145728; // 设置附件上传大小
                $upload->exts = array('jpg', 'gif', 'png', 'jpeg'); // 设置附件上传类型
                // 设置附件上传根目录
                $upload->rootPath = UP_PATH;

                // 上传单个文件
                $info = $upload->uploadOne($_FILES['image']);
                if (!$info) {// 上传错误提示错误信息
                    $data['code'] = 0;
                    $data['content'] = $upload->getError();
                    var_dump( $data);
                } else {// 上传成功 获取上传文件信息
                    $picpathname = UP_PATH . $info['savepath'] . $info['savename'];
                    $_POST['image'] = $picpathname;
                    $info = $this->course->create();
                    $z= $this->course->add($info);  //add()返回新纪录的主键id值
                    if($z){
                        $this->redirect('index',array(),2,'添加课程成功！'.$z);
                    }

                }
            }

            //通过Model的create方法收集表单信息
            //(过滤非法字段、表单验证、自动完成)
        $this->display();
    }
    public function delCourse(){
            if(!empty($_POST)){
                $stage= $this->course->where("course_id='$_POST[course_id]'")->delete();
                if($stage)
                    exit('ok');
                else
                    exit();

            }
            else
                exit();

    }
    public function update($i=null){
        if(!empty($i)){
            var_dump(I('post.'));
            $data= $this->course->where("course_id='$i'")->find();

            $data['content']= htmlspecialchars_decode($data['content']);
            $this->assign('data',$data);
            //两个逻辑：展示表单、收集表单
            if(!empty($_POST)){
//                实现附件上传处理
                if($_FILES['image']['error']!=4){
                    //A.实现图片上传
                    $upload = new \Think\Upload(); // 实例化上传类
                    $upload->maxSize = 3145728; // 设置附件上传大小
                    $upload->exts = array('jpg', 'gif', 'png', 'jpeg'); // 设置附件上传类型
                    // 设置附件上传根目录
                    $upload->rootPath = UP_PATH;

                    // 上传单个文件
                    $info = $upload->uploadOne($_FILES['image']);
                    if (!$info) {// 上传错误提示错误信息
                        $data['code'] = 0;
                        $data['content'] = $upload->getError();
                        var_dump( $data);
                    } else {// 上传成功 获取上传文件信息
                        $picpathname=UP_PATH.$info['savepath'].$info['savename'];
                        $_POST['image']=$picpathname;
                        $info= $this->course->create();
                        $z= $this->course->where("course_id='$i'")->save($info); //save
                        if($z){
                            $this->redirect('index',array(),2,'修改课程成功！');
                        }
                        else
                            echo "error";
                    }
                }
                else{
                    $info= $this->course->create();
                    $z= $this->course->where("course_id='$i'")->save($info); //save
                    if($z){
                        $this->redirect('index',array(),2,'修改课程成功！');
                    }
                    else
                        echo "error";
                }
                }

            $this->display();
    }
        else
            echo "<script> alert('没有接收到good') </script>";
    }
}