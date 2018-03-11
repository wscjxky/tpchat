<?php
namespace Home\Controller;
use Think\Controller;
//vendor('Wechat.wechat', '' ,'.php');

class ResultController extends Controller {
    public function __construct()
    {
        parent::__construct();

    }


    public function index(){
        $trade=D('trade')->where(array('trade_id'=>I('get.trade_id')))->find();
        $trade['trade_state']='已支付';
        D('trade')->save($trade);
        $this->assign('url','http://www.jianpianzi.com/tpchat/index.php/Chat/user/tradeinfo?trade_id='.I('get.trade_id'));
        $BUYER_IS_AGENT=false;
        $SHARER_IS_AGENT=false;
        $PEOPLE_COUNT=0;
        $ADD_BONUS=0;
        $ADD_CASH=0;
        $FINAL_PRICE=0;
        $trade=D('trade')->where(array('trade_id'=>I('get.trade_id')))->find();
        $user=D('user')->where(array('openid'=>$trade['openid']))->find();


        //定义各个变量
        if($aid=$trade['agent_openid']) {
            $share_user = D('user')->where(array('openid' => $aid))->find();
            if ($share_user['agent']!=0){
                $SHARER_IS_AGENT=true;
            }
        }

        if($user['agent']!=0){
            $BUYER_IS_AGENT=true;
        }

        $PEOPLE_COUNT=$trade['people_count'];
        $FINAL_PRICE=$trade['final_price'];


        switch ($user['agent']){
            case 1:
                $ADD_CASH=(int)floor($FINAL_PRICE * 0.05);
                break;
            case 2:
                $ADD_CASH=(int)floor($FINAL_PRICE * 0.075);
                break;
            case 3:
                $ADD_CASH=(int)floor($FINAL_PRICE * 0.1);
                break;
        }




        $ADD_BONUS=(int)$PEOPLE_COUNT*2;


        if($BUYER_IS_AGENT){
            if(!$SHARER_IS_AGENT &&$share_user){
                $this->addBonus($share_user,$ADD_BONUS,true);
            }
            $this->addCash($user,$ADD_CASH);

        }
        else {
            if($SHARER_IS_AGENT &&$share_user){
                $this->addCash($share_user,$ADD_CASH);
            }
            else if(!$SHARER_IS_AGENT &&$share_user){
                $this->addBonus($share_user,$ADD_BONUS,true);
            }
            $this->addBonus($user,$ADD_BONUS);

        }
        $this->display();
    }
    public function  addBonus($user,$bonus,$is_share=false){
        if(!$is_share) {
            $user["bonus_cost"] += (int)$user["bonus_current"];
        }
        $user["bonus_current"]=$bonus;
        $user['bonus_total']=$user["bonus_current"]+$user["bonus_cost"] ;

        D('user')->save($user);
    }
    public function  addCash($user,$cash){
        $user['cash_current'] =  (int)$user['cash_current']+$cash;
        $user['cash_total'] = $user['cash_current']+ $user['cash_cost']+$user['cash_submit'];
        D('user')->save($user);
    }
}