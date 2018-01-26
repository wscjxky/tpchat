<?php
namespace Home\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');

class IndexController extends Controller {

    public function index(){

        $weObj = new \Wechat();

        $weObj->valid();//明文或兼容模式可以在接口验证通过后注释此句，但加密模式一定不能注释，否则会验证失败

        $type = $weObj->getRev()->getRevType();

        $event=$weObj->getRev()->getRevEvent();
        $user=$weObj->getRevFrom();
        $content=$weObj->getRevContent();
        switch($type) {
            case \Wechat::MSGTYPE_TEXT:
                switch ($content){
                    case "活动":
                        $weObj->text("<a href='http://www.jianpianzi.com/tpchat/index.php/Chat/article'>活动详情</a>")->reply();
                        break;
                    case "买":
                        $weObj->text('点击底部菜单栏中间的筑影课程，就可以直接进入购买页啦！')->reply();
                        break;
                    case "作品":
                        $weObj->text('<a href="http://www.jianpianzi.com/tpchat/index.php/Chat/product">作品集锦</a>')->reply();
                        break;
                    case "订":
                        $weObj->text('<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/chat/user/trade&response_type=code&scope=snsapi_userinfo&state=1&connect_redirect=1#wechat_redirect">我的订单</a>')->reply();
                        break;
                    case "我":
                        $weObj->text('<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/chat/user&response_type=code&scope=snsapi_userinfo&state=1&connect_redirect=1#wechat_redirect">我的信息</a>')->reply();
                        break;
                    default:
                        $weObj->text($content)->reply();
                        break;
                }
                break;
            case \Wechat::MSGTYPE_EVENT:
                if ($event['key']=='aboutus')
                    $weObj->text("筑影学堂隶属于北京远途文化公司，专为5-16岁语言形成关键时期的青少儿量身打造专业课程。我们的联系方式：<a href='tel:010-85388138'>010-85388138</a>")->reply();
                else if($event['event']==\Wechat::EVENT_SUBSCRIBE)
                    $weObj->text("感谢您的关注！筑影学堂与各大知名高校联手，共同专为5-16岁的青少儿量身打造传媒领域专业课程，让孩子们从小建立自信，提升综合素质，拥有更大舞台。")->reply();
                else  if ($event['key']=='commerce')
                    $weObj->text("您好，如果有各种问题、建议、咨询或是合作，可联系<a href='tel:13011133933'>13011133933</a>。投稿可发邮箱：59741843@qq.com")->reply();
                else  if ($event['key']=='chat')
                    $weObj->text("嘿~终于等到你一起学习啦！在输入框内回复以下关键词就可以看到更多内容哦！\n【活动】\n【买】\n【作品】\n【订】\n【我】")->reply();
                    break;
            case \Wechat::MSGTYPE_IMAGE:
                break;

            default:
                $weObj->text("help")->reply();
                break;
        }
    }
}