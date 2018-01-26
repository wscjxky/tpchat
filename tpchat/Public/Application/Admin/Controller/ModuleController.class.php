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
            var_dump(I('post.'));
            if($_FILES['image']['error']!=4) {
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
                    var_dump($data);
                } else {// 上传成功 获取上传文件信息
                    $picpathname = UP_PATH . $info['savepath'] . $info['savename'];
                    $_POST['image'] = $picpathname;
                    $info = M('banner')->create();
                    $z = M('banner')->add($info);  //add()返回新纪录的主键id值
                    if ($z) {
                        var_dump($info);
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


    public function article(){
        $data= M('article')->select();
        $this->assign('data',$data);
        $this->assign('count',count($data));
        $this->display();
    }


    public function article_info(){
        $article_id = I('get.id/d');
        var_dump($article_id);
        if(!empty($article_id)){
            $info = D('article')->where(array("article_id"=> $article_id))->find();
            $this->assign('data',$info);
        }
        $act = empty($article_id) ? 'add' : 'update';
        $this->assign('act',$act);
        $this->display();
    }

    public function articleHandle(){
        $data=I('post.');
        $article_id = I('post.id/d');
        $act = I('post.act');
        if($act == 'update') {
            unset($data['act']);
            $r = D('article')->where(array('article_id'=>$article_id))->save($data);
            var_dump($data);
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
            var_dump($data);
            unset($data['article_id']);
            $r = D('article')->add($data);
        }
        if($r){
            $this->success("操作成功",U('Admin/Module/article'));
        }else{
            $this->error("操作失败",U('Admin/Module/article'));
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