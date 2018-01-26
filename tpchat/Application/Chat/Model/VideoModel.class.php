<?php
/**
 * Created by PhpStorm.
 * User: hhh
 * Date: 2017/8/21
 * Time: 下午4:39
 */
namespace Chat\Model;
use Think\Model;

class VideoModel extends Model
{
    public function __construct()
    {
        parent::__construct();

    }
    public  function getPraise(){
        return D('video_praise')->where(array('video_id'=>session('video_id')))->select();
    }
    public function isPraise(){
        return D('video_praise')->where(array('openid'=>session('openid'),'video_id'=>session('video_id')))->find();
    }
    public function addPraise($data){
        return D('video_praise')->add($data);

    }
    public  function getComments(){
        return D('video_comment')->where(array('video_id'=>session('video_id')))->select();

    }
    public  function addComment($data){
        return D('video_comment')->add($data);
    }

}
