<?php
namespace Home\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');
date_default_timezone_set("Asia/Shanghai");
class AccessController extends Controller
{
    private $weObj;

    public function __construct()
    {
        parent::__construct();

        $this->weObj = new \Wechat();
    }

    public function getUrl($url)

    {
        echo($this->weObj->getOauthRedirect($url));
    }

    public function index()
    {
        var_dump($this->weObj->checkAuth());
    }

    public function checkAuth()
    {
        $url='https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.cunpianzi.com/tpchat/index.php/home/access/checkauth&response_type=code&scope=snsapi_base&state=1#wechat_redirect';
        if(IS_POST){
            $evidence=I('post.evidence');
            $result=M('evidence')->where(array('evidence'=>$evidence))->find();

            session('course_id',$result['course_id']);

            $success_url="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxfdf007a79f182aed&redirect_uri=http://www.cunpianzi.com/tpchat/index.php/Chat/User/registerinfo?evidence_id=$result[evidence_id]&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect";

            if($result) {
                //如果没openID
                if(!$result['openid']) {
                    $result['openid'] = session('openid');
                    $now = date('Y-m-d H:i:s');
                    $result['time']=$now;
                    $result['use_count']+=1;
                    M('evidence')->save($result);
                    $this->success('您好，登陆成功，请享受课程吧！',$success_url);
                }
                else{
                    $now = date('Y-m-d H:i:s');
                    //如果是相同的openid
                    if($result['openid']!=session('openid')){
                        $t = strtotime($result['time']);
                        $day = round((strtotime($now)-$t)/3600/24);
                        if($day>=1){
                            $result['time']=$now;
                            $result['openid']=session('openid');
                            $result['use_count']+=1;
                            M('evidence')->save($result);
                            $this->success('您好，登陆成功，请享受课程吧',$success_url);
                        }
                        else{
                            $this->error('您好，该凭证码已被使用，请更换',$url);
                        }
                    }
                    else{
                        $result['time']=$now;
                        $result['use_count']+=1;
                        M('evidence')->save($result);
                        $this->success('您好，登陆成功，请享受课程吧',$success_url);
                    }


                }
            }
            else{
                $this->error('您好，凭证码无效，请重新再试',$url);            }
        }
        $data=$this->weObj->getOauthAccessToken();
        $openid=$data['openid'];
        if(!$openid){
            $this->error('您好，请重新授权',$url);
        }

        $data=M('user')->where(array('openid'=>$openid))->find();
        $this->assign('chatname',$data['chatname']);
        session('openid',$openid);
        $this->display();

    }


    public function getRedId()
    {

        $signPackage =  $this->weObj->getJsSign();
        $openArr=$this->weObj->getOauthAccessToken();
        echo '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title></title></head><body><span class="desc">获取“分享到朋友圈”按钮点击状态及自定义分享内容接口</span>
<button class="btn btn_primary" id="onMenuShareTimeline" >onMenuShareTimeline</button></body> ';
        echo '<script src="http://res.wx.qq.com/open/js/jweixin-1.2.0.js"></script>
<script>
  wx.config({
    debug: true,
    appId: \''.$signPackage["appId"].'\',
    timestamp: \''.$signPackage["timestamp"].'\',
    nonceStr: \''.$signPackage["nonceStr"].'\',
    signature: \''.$signPackage["signature"]. '\',
    jsApiList: [
        \'onMenuShareTimeline\'    ]
  });
  wx.ready(function () {
      
          wx.onMenuShareTimeline({
              title: \'测试\',

              link: \'http://www.cunpianzi.com/tpchat/index.php/Chat/index/course/courseid/12/aid/'.$openArr["openid"]
           .'\',
              imgUrl: \'http://demo.open.weixin.qq.com/jssdk/images/p2166127561.jpg\',
              trigger: function (res) {
                  // 不要尝试在trigger中使用ajax异步请求修改本次分享的内容，因为客户端分享操作是一个同步操作，这时候使用ajax的回包会还没有返回
                  alert(\'用户点击分享到朋友圈\');
              },
              success: function (res) {
                  alert(\'已分享\');
              },
              cancel: function (res) {
                  alert(\'已取消\');
              },
              fail: function (res) {
                  alert(JSON.stringify(res));
              }
          });
          alert(location.href.split(\'#\')[0]);
   
  });
</script>
</html>';
    }



    public function saveUserInfo($openid){
        $userinfo=$this->weObj->getUserInfo($openid);
        $data=array();
        $data['username']=$userinfo['nickname'];
        $data['chatname']=$userinfo['nickname'];
        $data['profile']=$userinfo['headimgurl'];
        $data['gender']=$userinfo['sex'];
        $data['province']=$userinfo['province'];
        $data['city']=$userinfo['city'];

        $user=D('user')->where(array('openid'=>$openid))->save($data);

        var_dump($user);



    }





    public function getUserInfo(){
        var_dump($users=$this->weObj->getUserList());
        foreach ($users['data']['openid'] as $user){
            $this->saveUserInfo($user);
//            var_dump($this->weObj->getUserInfo($user));
        }
    }
}