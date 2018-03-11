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
//        $point=$weObj->getRevEventGeo();
//        if(!D('user')->where(array('openid'=>$user))->find()){
//            D('user')->add(array('openid'=>$user,'point_x'=>$point['x'],'point_y'=>$point['y']));
//        }
//        else{
//            D('user')->where(array('openid'=>$user))->save(array('point_x'=>$point['x'],'point_y'=>$point['y']));
//
//        }

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
                if ($event['key']=='aboutus'){
                    $data = array(0 => array(
                        'Title' => '关于我们',
                        'Description' => '远途文化是一家校园媒体运营服务和教育培训提供商。',
                        'PicUrl' => 'http://mmbiz.qpic.cn/mmbiz_jpg/Tl6ricVN7P8dzC7M6ic8HicFbJxnpzibxPiaNicRqWRfbDRq9NCp6wxhbQYLBq3Lib1gnl9icwnHyS8Rq8o9UvUB0M31NQ/0?wx_fmt=jpeg',
                        'Url' => 'http://mp.weixin.qq.com/s?__biz=MzU1MzE4MjYxNQ==&mid=100000009&idx=1&sn=bd5bdde1b15fef810db0b2caf9b357e2&chksm=7bf7f5f14c807ce7bc482db9510b4bdb56977ab537aa8fe534e510ce18c07951b96f3a83ec81#rd'));

                    $weObj->news($data)->reply();
                }

                else if($event['event']==\Wechat::EVENT_SUBSCRIBE)
                    $weObj->text("感谢您的关注！筑影天地与各知名电视台、传媒高校一起，为5-13岁的青少儿童，量身打造文化传媒领域的实践培训基地，帮助孩子们建立自信，提升综合素养，锻炼实践和创新能力。您可以进入<a href='https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/chat&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'>筑影学堂</a>挑选专业的实训课程，教孩子们沟通表达、组织活动、摄影摄像、制作视频和策划校园栏目等，这些课程由专业老师教授，形式新颖，内容实用。您可以进入<a  href='https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/Chat/article&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'>热点聚焦</a>，阅读丰富多彩的文章，学习有用的文化传媒知识，了解最新的传媒教育动态，欣赏精彩的视频影像。您也可以进入<a href='https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.jianpianzi.com/tpchat/index.php/Chat/product&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'>作品集锦</a>，这些都是学堂孩子们培训后的成果展现，他们拍成了视频提交上来，等着你观看、点赞和评论，别忘了这里还经常举行比赛活动哦，点赞最多的孩子会获得丰厚的奖品。看累了，您就进入<a href='http://www.ximalaya.com/zhubo/93586430/'>筑影FM</a>感受一下，用耳朵倾听老师们的现场教学录音，总之这里有很多让你感觉有趣的东西，快来体验吧!")->reply();
                else  if ($event['key']=='commerce')
                    $weObj->text("筑影学堂热忱期待与有志于提高中小学生实践能力，为下一代成长贡献力量的机构及个人合作！诚招课程代理、主持人老师、摄影/摄像老师、青少年活动策划专家、互联网运营和推广专家等。同时欢迎培训机构、场地负责人、投资机构及个人洽谈合作。联系人：张经理，联系电话：<a href='010-85388138'>010-8538 8138</a>、<a href='13011133933'>13011133933</a>，敬请垂询！")->reply();
                else  if ($event['key']=='chat'){
                    $this->saveUserInfo($user);
                    $weObj->text("嘿~终于等到你一起学习啦！在输入框内回复以下关键词就可以看到更多内容哦！\n【活动】\n【买】\n【作品】\n【订】\n【我】")->reply();
                }
                break;

            case \Wechat::MSGTYPE_IMAGE:
                break;

            default:
                $weObj->text("help")->reply();
                break;
        }
    }

    public function saveUserInfo($openid){
        $weObj = new \Wechat();
        $userinfo=$weObj->getUserInfo($openid);
        $data=array();
        $data['username']=$userinfo['nickname'];
        $data['chatname']=$userinfo['nickname'];
        $data['profile']=$userinfo['headimgurl'];
        $data['gender']=$userinfo['sex'];
        $data['province']=$userinfo['province'];
        $data['city']=$userinfo['city'];
        $user=D('user')->where(array('openid'=>$openid))->save($data);

    }
}