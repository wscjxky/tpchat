<?php
// 本类由系统自动生成，仅供测试用途
namespace Chat\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');
class IndexController extends BaseController {
    public function __construct()
    {
        parent::__construct();
        $this->user=D('user');
//        session('openid','oAdCq01YzcVjLWljmeEBFcDEswEY');

    }

    public function index()
    {

        $banner=D('banner')->select();
        $this->assign('banner',$banner);
        $this->display();
    }
    public function ajaxCourse(){
        $course = M('course');
        if($index=I('post.index')){
            $res =  $course->where(array("publish_state"=>1))->limit($index)->select();
            $str='';
            foreach ($res as $r){
                $str .=sprintf("  <a href=\"Chat/index/course?courseid=$r[course_id]\" class=\"weui-media-box weui-media-box_appmsg\">
                            <div class=\"weui-media-box__hd\">
                                <img class=\"weui-media-box__thumb\" src=\"
                    %s\">
                            </div>
                            <div class=\"weui-media-box__bd\">
                                <h4 class=\"weui-media-box__title\">
                    $r[title]</h4>
                                <p class=\"weui-media-box__desc\">
                    $r[desc]</p>
                                <p class=\"weui-media-box__desc\"  style=\"text-align: end\">
                    $r[starttime]</p>
                                <p class=\"weui-media-box__desc\"  style=\"text-align: end\">¥ 
                   $r[price] </p>

                                <p class=\"weui-media-box__desc\" style=\"text-align: end\" >
                    $r[address]</p>

                            </div>
                        </a>",SHOW_URL.$r['image']);
            }
            if(count($res)<$index){
                exit(json_encode(array('status'=>'finish','data'=>$str)));
            }
            exit( exit(json_encode(array('status'=>'ok','data'=>$str))));
        }

    }
    public function course($courseid)
    {
        $weObj = new \Wechat();
        $aid='';
        $openid=I('get.aid');
        //$openid="oAdCq08z0miP9AerKiRV0akkB4EI";

        //如果aid和当前的一样就不是aid;
        if ($openid !=session('openid')) {
            $this->assign('aid',$openid);
            $aid=$openid;
            session('aid',$openid);
            //在数据库中记录俩个建立关系openid
//            var_dump(session('openid'));
        }
        $this->assign('trade_url',$weObj->getOauthRedirect("http://www.jianpianzi.com/tpchat/index.php/Chat/index/trade?course_id=$courseid&aid=$aid"));
        $course=D('course');
        $data=$course->where("course_id='$courseid'")->find();
        $data['content']= htmlspecialchars_decode($data['content']);
        $this->assign('data',$data);

        http://www.jianpianzi.com/tpchat/index.php/Chat/trade?course_id=12&aid=&code=0011Fgud1gSwwv057xsd1a0xud11FguL&state=
        //重新获取没有注册的用户信息


        $signPackage =  $weObj->getJsSign();
        echo '<script src="http://res.wx.qq.com/open/js/jweixin-1.2.0.js"></script>
<script>
  wx.config({
    debug: false,
    appId: \''.$signPackage["appId"].'\',
    timestamp: \''.$signPackage["timestamp"].'\',
    nonceStr: \''.$signPackage["nonceStr"].'\',
    signature: \''.$signPackage["signature"]. '\',
    jsApiList: [
        \'onMenuShareTimeline\',
            \'onMenuShareAppMessage\']
  });
  wx.ready(function () {
  var url=\'http://www.jianpianzi.com/tpchat/index.php/Chat/index/course?courseid=12&aid='.session('openid').'\';
          wx.onMenuShareTimeline({
              title: "'.$data['title'].'",
              desc :"'.$data['subtitle'].'",
              link: url,
              imgUrl: \'http://www.jianpianzi.com/tpchat/Public/upload/image/logo.jpg\'
              
          });
          
          wx.onMenuShareAppMessage({

            title:"'.$data['title'].'",
              desc :"'.$data['subtitle'].'",
              link: url,
              imgUrl: \'http://www.jianpianzi.com/tpchat/Public/upload/image/logo.jpg\'
});
  });
</script>
</html>';

        $this->display();
    }



    public function trade()
    {
        $user = D('user');
        $course_id=I('get.course_id');
        session('course_id',$course_id);
        $weObj = new \Wechat();
        if ($_GET['code']) {
            $result = $weObj->getOauthAccessToken();
            $openId = $result['openid'];
            $access = $result['access_token'];
            if ($openId) {
                session('openid', $openId);
                session('access', $access);
            }
            //立用户信息
            if (!$user->getUser()) {
                $weObj = new \Wechat();
                $userInfo = $weObj->getOauthUserinfo(session('access'), session('openid'));
                if ($userInfo) {
                    $user->addUser($userInfo);
                }
            }
        }

        if(I('post.')){
            $trade=D('trade');
            $data=$trade->create();
            $data['openid']=session('openid');
            $data['cheap_price']=(int)I('post.total_price')-(int)I('post.final_price');
            $data['evidence']=$trade->getRandom(I('post.people_count/d'),session('course_id'));

            if(session('aid'))
                $data['agent_openid']=session('aid');
            exit($trade->add($data));
        }

        $course=D('course');
        $data=$course->where(array('course_id'=>$course_id))->find();
        $user_data=  $user->where(array('openid'=>session('openid')))->find();
        if($user_data)
            $data['bonus_current']=$user_data['bonus_current'];
        else
            $data['bonus_current']=0;

        $this->assign('data',$data);


        $this->display();
    }

}
