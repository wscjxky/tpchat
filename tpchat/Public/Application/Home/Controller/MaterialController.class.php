<?php
namespace Home\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');

class MaterialController extends Controller {
    public function index()
    {
        $media_id=null;
        $weObj = new \Wechat();
        $data=$weObj->getForeverList('news',0,5);
        foreach ($data as $item) {
            foreach ($item as $i) {
            $media_id = $i['media_id'];
        }
        }
        if($media_id) {
            $res = $weObj->getForeverMedia($media_id);
            foreach ($res as $item) {
                foreach ($item as $i) {
                    var_dump($i['url']);
                }
            }
        }
    }


}