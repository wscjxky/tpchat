<?php
namespace Admin\Controller;
use Think\Controller;
class ModuleController extends Controller {
    public function index(){
        $data= M('banner')->select();
        $this->assign('data',$data);
        $this->assign('count',count($data));
        $this->display();
    }
    public function addbanner(){
        if(!empty($_POST)){
            if($_FILES['image']['error']!=4) {
                //A.实现图片上传
                $upload = new \Think\Upload(); // 实例化上传类
                $upload->maxSize = 10240; // 设置附件上传大小
                $upload->exts = array('jpg', 'gif', 'png', 'jpeg'); // 设置附件上传类型
                // 设置附件上传根目录
                $upload->rootPath = UP_PATH;

                // 上传单个文件
                $info = $upload->uploadOne($_FILES['image']);
                if (!$info) {// 上传错误提示错误信息
                    $data['code'] = 0;
                    $data['content'] = $upload->getError();
                } else {// 上传成功 获取上传文件信息
                    $picpathname = UP_PATH . $info['savepath'] . $info['savename'];
                    $image = new \Think\Image();
                    $image->open($picpathname);
                    $image->thumb(480, 240 )->save($picpathname);
                    $_POST['image'] = $picpathname;
                    $info = M('banner')->create();
                    $z = M('banner')->add($info);  //add()返回新纪录的主键id值
                    if ($z) {

                        $this->success("操作成功",U('Module/index'));
                    }

                }
            }
        }

        $this->display();
    }
    public function bannerHandle(){
            $banner_id = I('post.id/d');
            $act = I('post.act');
            if($act == 'del'){
                $r = M('banner')->where(array('banner_id'=>$banner_id))->delete();
                if($r){
                    exit(json_encode(1));
                }else{
                    exit(json_encode("删除失败"));
                }
            }

        }
    public function message(){

        $data=M('user')->select();
        $this->assign('data',$data);
        $this->display();
    }
    public function article(){
        $data= M('article')->order('createtime desc')->select();
        $this->assign('data',$data);
        $this->assign('count',count($data));
        $this->display();
    }
    public function article_info(){
        $article_id = I('get.id/d');
        if(!empty($article_id)){
            $info = D('article')->where(array("article_id"=> $article_id))->find();
            $this->assign('data',$info);
        }
        $act = empty($article_id) ? 'add' : 'update';
        $this->assign('act',$act);
        $this->display();
    }
    public function articleHandle(){

        $article_id = I('post.id/d');
        $act = I('post.act');

        if($act == 'update') {
            $this->uploadimg();
            $data=I('post.');
            unset($data['act']);
            $r = D('article')->where(array('article_id'=>$article_id))->save($data);
        }
        else if($act == 'del'){
            $r = M('article')->where(array('article_id'=>$article_id))->delete();
            if($r){
                exit(json_encode(1));
            }else{
                exit(json_encode("删除失败"));
            }
        }
        else if($act == 'add'){
            $this->uploadimg();
            $data=I('post.');
            unset($data['article_id']);
            $r = D('article')->add($data);
        }
        if($r){
            $this->success("操作成功",U('Admin/Module/article'));
        }else{
            $this->success("操作成功",U('Admin/Module/article'));

//            $this->error("操作成功",U('Admin/Module/article'));
        }




    }
    public function articlePublish(){
        if($id=I('post.id')){
            $course= D('article')->where(array('article_id'=>$id))->find();
            if( $course['publish_state']==0)
                $course['publish_state']=1;
            else{
                $course['publish_state']=0;
            }
            D('article')->save($course);
            exit('ok');
        }
        else
            exit();
    }

    public function tutorial(){
        $data= M('tutorial')->order('createtime desc')->select();
        $this->assign('data',$data);
        $this->assign('count',count($data));
        $this->display();
    }
    public function tutorial_info(){
        $tutorial_id = I('get.id/d');
        if(!empty($tutorial_id)){
            $info = D('tutorial')->where(array("tutorial_id"=> $tutorial_id))->find();
            $this->assign('data',$info);
        }
        $act = empty($tutorial_id) ? 'add' : 'update';
        $this->assign('act',$act);
        $this->display();
    }
    public function tutorialHandle(){

        $tutorial_id = I('post.id/d');
        $act = I('post.act');

        if($act == 'update') {
            $this->uploadimg();
            $data=I('post.');
            unset($data['act']);
            $r = D('tutorial')->where(array('tutorial_id'=>$tutorial_id))->save($data);
        }
        else if($act == 'del'){
            $r = M('tutorial')->where(array('tutorial_id'=>$tutorial_id))->delete();
            if($r){
                exit(json_encode(1));
            }else{
                exit(json_encode("删除失败"));
            }
        }
        else if($act == 'add'){
            $this->uploadimg();
            $data=I('post.');
            unset($data['tutorial_id']);
            $r = D('tutorial')->add($data);
        }
        if($r){
            $this->success("操作成功",U('Admin/Module/tutorial'));
        }else{
            $this->success("操作成功",U('Admin/Module/tutorial'));

//            $this->error("操作成功",U('Admin/Module/tutorial'));
        }




    }

    public function activity(){
        $video= D('video_activity')->order('createtime desc')->select();
        $course= D('course')->where(array('is_activity'=>1))->order('createtime desc')->select();
        $article= D('article')->where(array('is_activity'=>1))->order('createtime desc')->select();

        $this->assign('video',$video);
        $this->assign('course',$course);
        $this->assign('article',$article);
        $this->display();
    }

    public function uploadimg(){
        $upload = new \Think\Upload(); // 实例化上传类
        $upload->maxSize = 51200; // 设置附件上传大小
        $upload->exts = array('jpg', 'gif', 'png', 'jpeg'); // 设置附件上传类型
        // 设置附件上传根目录
        $upload->rootPath = UP_PATH;

        // 上传单个文件
        $info = $upload->uploadOne($_FILES['image']);
        if (!$info) {// 上传错误提示错误信息
            $data['code'] = 0;
            $data['error'] = $upload->getError();
            exit($data['error']."请返回重试");
        }
        else{
            $picpathname = UP_PATH . $info['savepath'] . $info['savename'];
            $_POST['image'] = $picpathname;
        }
    }
    public function advice(){

        $data=M('advice')->query("SELECT*
                            FROM  `advice`  a
                            
                            INNER JOIN `user` b
                       
                            WHERE  a.openid=b.openid");
        $this->assign('data',$data);
        $this->assign('count',count($data));

        $this->display();



    }
}