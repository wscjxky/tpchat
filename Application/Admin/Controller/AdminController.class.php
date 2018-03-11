<?php
/**
 * Created by PhpStorm.
 * User: hhh
 * Date: 2017/8/17
 * Time: 上午9:47
 */

namespace  Admin\Controller;


use app\admin\controller\Base;
use Think\Controller;
use Think\Verify;
use Think\Db;
use Think\Session;

class AdminController extends Controller {

    public function __construct()
    {
        parent::__construct();
        $this->right_list=array(
            '创建课程伙伴',
            '创建筑影运营',
            '创建筑影商务',
            '发布课程','
            发布软文',
            '审核课程发布','
        审核软文发布',
            '查看/管理本单位数据（课程、订单、软文）','
        查看/管理所有数据（课程、订单、软文）
        ','
        处理提现',
            '设置顾问级别'
        ,'设置会员状态');

    }

    public function index(){


        $data=D('admin')->select();
        $this->assign('data',$data);

        $this->assign('count',count($data));

        $this->display();
    }

    /*
    * 管理员登陆
    */
    public function login(){

        if(session('?account')){
            $this->error("您已登录",U('Admin/Index/index'));
        }

        if(IS_POST){
//            $verify = new Verify();
//            if (!$verify->check(I('post.vertify'), "admin_login")) {
//                exit(json_encode(array('status'=>0,'msg'=>'验证码错误')));
//            }
            $condition['account'] = I('post.username/s');
            $condition['password'] = I('post.password/s');
            if(!empty($condition['account']) && !empty($condition['password'])){
                $admin_info =D('admin')->where(array("account"=>$condition['account'],"password"=>$condition['password']))->find();
                if(is_array($admin_info)){
                    session('role',$admin_info['role']);
                    session('account',$admin_info['account']);
                    session('admin_id',$admin_info['admin_id']);
                    session('admin_username',$admin_info['username']);
                    $this->redirect('Index/index');

                }else{
                    exit(var_dump(array('status'=>0,'msg'=>'账号密码不正确')));
                }
            }else{
                exit(var_dump(array('status'=>0,'msg'=>'请填写账号密码')));
            }
        }

        $this->display();
    }




    public function role(){


        $data=D('admin_role')->select();
        $this->assign('data',$data);
        $this->assign('count',count($data));

        $this->display();
    }

    public function role_info(){
        $role_id = I('get.id/d');

        if(!empty($role_id)){
            $info = D('admin_role')->where(array("role_id"=> $role_id))->find();
            $this->assign('data',$info);
        }
        $act = empty($role_id) ? 'add' : 'update';
        $this->assign('act',$act);


        $this->assign('role_list',$this->right_list);

        return $this->display();
    }

    public function roleHandle(){
        $data=I('post.');
        $role_id = I('post.id/d');
        $act = I('post.act');
        if($act == 'update') {
            unset($data['act']);
            $r = D('admin_role')->where(array('role_id'=>$role_id))->save($data);
            var_dump($data);
        }
        else if($act == 'del'){

//            $admin = D('admin')->where(array('role_id'=>$role_id))->find();
//            if($admin){
//                exit(json_encode(2));

//            }else{
                $r = M('admin_role')->where(array('role_id'=>$role_id))->delete();
                if($r){
                    exit(json_encode(1));
                }else{
                    exit(json_encode("删除失败"));
                }
//            }
        }
        else if($act == 'add'){
            var_dump($data);
            if(D('admin_role')->where(array("role_name"=>$data['role_name']))->find()){
                $this->error("此名已被注册，请更换",U('Admin/Admin/role'));
            }else{
                unset($data['role_id']);
                $data['role_list'] ='';
                foreach ($data as $key=>$value) {
                    if(is_numeric($key)){
                        $data['role_list'] .= $value.',';
                    }
                }            var_dump($data);

                $r = D('admin_role')->add($data);

            }
        }
        if($r){
            $this->success("操作成功",U('Admin/Admin/role'));
        }else{
//            $this->error("操作失败",U('Admin/Admin/role'));
        }




    }






    public function admin_info(){
        $admin_id = I('get.id/d');
        var_dump($admin_id);

        if(!empty($admin_id)){
            $info = D('admin')->where(array("admin_id"=> $admin_id))->find();
            $this->assign('data',$info);
        }
        $act = empty($admin_id) ? 'add' : 'update';
        $this->assign('act',$act);
        $role_list=D('admin_role')->select();
        $this->assign('role_list',$role_list);
        return $this->display();
    }

    public function adminHandle(){
        $data=I('post.');
        $admin_id = I('post.id/d');
        $act = I('post.act');
        if($act == 'update') {
            unset($data['act']);
            $r = D('admin')->where(array('admin_id'=>$admin_id))->save($data);
        }
        else if($act == 'del'){
            $r = M('admin')->where(array('admin_id'=>$admin_id))->delete();
            if($r){
                exit(json_encode(1));
            }else{
                exit(json_encode("删除失败"));
            }
        }
        else if($act == 'add'){
            if(D('admin')->where(array("account"=>$data['account']))->find()){
                $this->error("此名已被注册，请更换",U('Admin/Admin/index'));
            }else{
                unset($data['admin_id']);
                $r = D('admin')->add($data);

            }
        }
        if($r){
            $this->success("操作成功",U('Admin/Admin/index'));
        }else{
            $this->error("操作失败",U('Admin/Admin/index'));
        }




    }


    public function log(){
        $data=D('admin_log')->select();
        $this->assign('data',$data);

        $this->display();
    }
































    /**
     * 修改管理员密码
     * @return \think\mixed
     */













    public function modify_pwd(){
        $admin_id = I('admin_id/d',0);
        $oldPwd = I('old_pw/s');
        $newPwd = I('new_pw/s');
        $new2Pwd = I('new_pw2/s');

        if($admin_id){
            $info = D('admin')->where("admin_id", $admin_id)->find();
            $info['password'] =  "";
            $this->assign('info',$info);
        }

        if(IS_POST){
            //修改密码
            $enOldPwd = encrypt($oldPwd);
            $enNewPwd = encrypt($newPwd);
            $admin = M('admin')->where('admin_id' , $admin_id)->find();
            if(!$admin || $admin['password'] != $enOldPwd){
                exit(json_encode(array('status'=>-1,'msg'=>'旧密码不正确')));
            }else if($newPwd != $new2Pwd){
                exit(json_encode(array('status'=>-1,'msg'=>'两次密码不一致')));
            }else{
                $row = M('admin')->where('admin_id' , $admin_id)->save(array('password' => $enNewPwd));
                if($row){
                    exit(json_encode(array('status'=>1,'msg'=>'修改成功')));
                }else{
                    exit(json_encode(array('status'=>-1,'msg'=>'修改失败')));
                }
            }
        }
        return $this->fetch();
    }
    

    /**
     * 退出登陆
     */
    public function logout(){
        session_unset();
        session_destroy();
        session::clear();
        $this->success("退出成功",U('Admin/Admin/login'));
    }

    /**
     * 验证码获取
     */
    public function vertify()
    {
        $config = array(
            'fontSize' => 30,
            'length' => 4,
            'useCurve' => true,
            'useNoise' => false,
            'reset' => false
        );
        $Verify = new Verify($config);
        $Verify->entry("admin_login");
        exit();
    }



}