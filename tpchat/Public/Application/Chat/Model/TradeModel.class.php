<?php
/**
 * Created by PhpStorm.
 * User: hhh
 * Date: 2017/8/21
 * Time: 下午4:39
 */
namespace Chat\Model;
use Think\Model;

class TradeModel extends Model
{
    public function __construct()
    {
        parent::__construct();

    }
    public  function getCourse(){
        $openid=session('openid');
        $data=array();
        $result=$this->where("openid='".$openid."'")->select();
        if($result) {
            foreach ($result as $value) {
                $course_id = $value['course_id'];
                $course = D('course')->where("course_id='$course_id'")->find();
                array_push($data, $course);
            }
            return $data;
        }
        else{
            return false;
        }
    }
    public function getRandom($count,$course_id){
        $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        $data='';
        for ($j=0;$j<$count;$j++) {
            $password = '';
            for ($i = 0; $i < 16; $i++) {
                $password .= $chars[mt_rand(0, strlen($chars) - 1)];
            }
            M('evidence')->add(array('evidence'=>$password,'course_id'=>$course_id));
            $data.=$password.',';
        }
            return substr($data,0,strlen($data)-1);

    }
    public  function insertEvidence($elist){

    }
}
