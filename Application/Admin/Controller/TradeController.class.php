<?php
/**
 * Created by PhpStorm.
 * User: hhh
 * Date: 2017/8/17
 * Time: 上午11:24
 */

namespace Admin\Controller;

class TradeController extends BaseController
{
    public function __construct() {
        parent::__construct();
        // 订单 支付 发货状态
        $this->trade=D('trade');
        $this->query='SELECT*
                            FROM  `trade`  a
                            INNER JOIN `user` b
                            WHERE  a.openid=b.openid AND';

    }

    /*
     *订单首页
     */
    public function index(){
// 进行分页数据查询 注意page方法的参数的前面部分是当前的页数使用 $_GET[p]获取
        $count      = $this->trade->count();// 查询满足要求的总记录数
        $Page       = new \Think\Page($count,20);// 实例化分页类 传入总记录数和每页显示的记录数(25)
        $show       = $Page->show();// 分页显示输出
// 进行分页数据查询 注意limit方法的参数要使用Page类的属性
        $list =       $data=$this->trade->query("SELECT*
                            FROM  `trade`  a

                            INNER JOIN `user` b

                            WHERE  a.openid=b.openid
                            ORDER BY `createtime` DESC
                             LIMIT $Page->firstRow,$Page->listRows");
        $this->assign('count', count($data));

        $alldata=D('trade')->select();
        $total_people=0;
        foreach ($alldata as $item){
            $total_people+=$item['people_count'];
        }
        $this->assign('total_people', $total_people);
        $this->assign('data',$list);// 赋值数据集
        $this->assign('page',$show);// 赋值分页输出
        $this->display(); // 输出模板

//        $this->assign('data',$data);
//
//        $this->assign('count',count($data));
//
//        $this->display();
    }


    public function log(){

    }

    public function delTrade(){
        if(!empty($_POST)){
            $stage=$this->trade->where("trade_id='$_POST[trade_id]'")->delete();
            if($stage)
                exit('ok');
            else
                exit();

        }
        else
            exit();
    }
    public function search(){
        if(I('get.')){
            $act=I('get.act/s');
            $trade_state=I('get.trade_state/s');
            $keyword=I('get.keyword/s');
            if($act=='course_title'){
                if($trade_state=='---'){
                    $data=M('trade')->query($this->query."
                course_title  like '%$keyword%'");
                    $this->assign('data',$data);
                    $this->assign('count',count($data));
                }
                else {
                    $data = M('trade')->query($this->query . "
                course_title  like '%$keyword%' AND trade_state = '$trade_state'");
                    $this->assign('data', $data);
                    $this->assign('count', count($data));
                }
            }
            else if($act=='chatname'){
                if($trade_state=='---'){
                    $data=M('trade')->query("SELECT*
                FROM  `trade`  a   
                INNER JOIN `user` b
                ON a.openid=b.openid    
                WHERE  chatname  like '%$keyword%'");
                    $this->assign('data',$data);
                    $this->assign('count',count($data));
                }
                else {
                    $data = M('trade')->query("SELECT*
                FROM  `trade`  a   
                INNER JOIN `user` b
                ON a.openid=b.openid    
                WHERE  chatname  like '%$keyword%' AND trade_state = '$trade_state'");
                    $this->assign('data', $data);
                    $this->assign('count', count($data));
                }
            }
        }
        $total_people=0;
        foreach ($data as $item){
            $total_people+=$item['people_count'];
        }
        $this->assign('total_people', $total_people);
        $this->display();
    }
}