<?php
namespace Admin\Model;
use Think\Model;

//用户model模型类
class UserModel extends Model{

    public function __construct()
    {
        parent::__construct();
    }

    public function getTradeArr($openid){
        return $this->query("
        SELECT*
        FROM `user` a
        INNER JOIN `trade` b
        ON a.openid=b.openid
        WHERE a.openid='$openid' AND b.trade_state='已支付'");
    }
    public function getAgent($agent){
            switch ($agent){
                case 0:
                    return '非顾问';
                    break;
                case 1:
                    return '顾问';
                    break;

                case 2:
                    return '高级顾问';
                    break;

                case 3:
                    return '资深顾问';
                    break;

                default:
                    break;
            }
    }
}