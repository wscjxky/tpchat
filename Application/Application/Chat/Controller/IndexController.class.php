<?php
// 本类由系统自动生成，仅供测试用途
namespace Chat\Controller;
use Think\Controller;
vendor('Wechat.wechat', '' ,'.php');
class IndexController extends BaseController
{
    public function __construct()
    {
        parent::__construct();
        $this->user = D('user');
//        session('openid','oAdCq016X8Hgd9iVKRk6Ob-r-sNU');
//        order('starttime desc')
    }

    public function index()
    {
        $banner = D('banner')->select();
        $this->assign('banner', $banner);
        $category = D('category')->select();
        $this->assign('small_category', $category);
        $this->display();
    }

    public function ajaxCourse()
    {
        $course = M('course');
        $big_category=I('post.big_category');
        if ($index = I('post.index')) {
            $res = $course->where(array("publish_state" => 1,'big_category'=>$big_category))->order('starttime desc')->limit($index)->select();
            $str = '';
            foreach ($res as $r) {
                $price=$r['price']==0?'免费报名':($r['price'].'元');
                $lasttime=$r['lasttime']?"，".$r['lasttime']:"";
                if($big_category=='专题活动')//时间配置
                    $r['starttime']=$this->time_zhuanti($r['starttime']);
                else{
                    $r['starttime']=$this->time_day($r['starttime']);
                }
                $str .= sprintf("  <div  class=\"weui-media-box weui-media-box_appmsg\"style='padding: 5px'>
                                <img onclick=\"javascript:window.location.href='Chat/index/course?courseid=$r[course_id]'\" style='width: 90px;height: 62px;vertical-align: top;margin-bottom: 15px'  src=\"
                    %s\">
                            <div class=\"weui-media-box__bd\">
                                <a  href='Chat/index/course?courseid=$r[course_id]' class='course_title'>
                    $r[title]
                                
                                <p class='weui-media-box__desc' >
                    $r[address]</p>
                    </a>
                                <p class='weui-media-box__desc'  >
                    $r[starttime] $lasttime </p>
                    
                     
                    
                                <p style='text-align: end'><i class='weui-media-box__desc_time'> $price </i> 
                  </p>

                               

                            </div>
                        </div>", SHOW_URL . $r['image']);
            }
            if (count($res) < $index) {
                exit(json_encode(array('status' => 'finish', 'data' => $str)));
            }
            exit(exit(json_encode(array('status' => 'ok', 'data' => $str))));
        }

    }

    public function arr_sort($array, $key, $order = "asc")
    { //asc是升序 desc是降序
        $arr_nums = $arr = array();
        foreach ($array as $k => $v) {
            $arr_nums[$k] = $v[$key];
        }
        if ($order == 'asc') {
            asort($arr_nums);
        } else {
            arsort($arr_nums);
        }
        foreach ($arr_nums as $k => $v) {
            $arr[$k] = $array[$k];
        }
        return $arr;
    }

    public function sortcourse()
    {
        $type=I('post.type');
        $category=I('post.category_name');
        $big_category=I('post.big_category');

        if($type=='address'){
            $user_x=I('post.x');
            $user_y=I('post.y');
            $course = M('course');
            if($category)
                $data =  $course->where(array("publish_state"=>1,"small_category"=>$category,'big_category'=>$big_category))->select();
            else
                $data =  $course->where(array("publish_state"=>1,'big_category'=>$big_category))->select();

            $sortdata=array();
            foreach ($data as $item) {
                $item['distance'] = $this->getDistance($user_y, $user_x, $item['point_y'], $item['point_x']);
                array_push($sortdata,$item);

            }

            //根据距离排序
            $sortdata=$this->arr_sort($sortdata,'distance');

            $str='';
            foreach ($sortdata as $r){
                $price=$r['price']==0?'免费报名':($r['price'].'元');
                if($big_category=='专题活动')//时间配置
                    $r['starttime']=$this->time_zhuanti($r['starttime']);
                else{
                    $r['starttime']=$this->time_day($r['starttime']);
                }
                $str .=sprintf("  <div  class=\"weui-media-box weui-media-box_appmsg\"style='padding: 5px'>
                                <img onclick=\"javascript:window . location . href = 'Chat/index/course?courseid=$r[course_id]'\" style='width: 90px;height: 62px;vertical-align: top;margin-bottom: 15px'  src=\"
                    %s\">
                            <div class=\"weui-media-box__bd\">
                                <a  href='Chat/index/course?courseid=$r[course_id]' class='course_title'>
                    $r[title]
                                
                     <p class='weui-media-box__desc' >
                    $r[address]</p>
                    </a>
                     <p class='weui-media-box__desc'  >
                    $r[starttime]</p>
                    
                             <p style='text-align: end'><i class='weui-media-box__desc_time'>
                      $price
                      </i> 
                  </p>

                               

                            </div>
                        </div>",SHOW_URL.$r['image']);
            }
            exit(json_encode(array('status'=>'finish','data'=>$str)));
        }
        else {
            if($category)
                $data = D('course')->where(array("publish_state" => 1,"small_category"=>$category,'big_category'=>$big_category))->order('starttime desc')->select();
            else
                $data = D('course')->where(array("publish_state" => 1,'big_category'=>$big_category))->order('starttime desc')->select();
            $str='';
            foreach ($data as $r){
                $price=$r['price']==0?'免费报名':($r['price'].'元');
                if($big_category=='专题活动')//时间配置
                    $r['starttime']=$this->time_zhuanti($r['starttime']);
                else{
                    $r['starttime']=$this->time_day($r['starttime']);
                }                $str .=sprintf("  <div  class=\"weui-media-box weui-media-box_appmsg\"style='padding: 5px'>
                                <img onclick=\"javascript:window . location . href = 'Chat/index/course?courseid=$r[course_id]'\" style='width: 90px;height: 62px;vertical-align: top;margin-bottom: 15px'  src=\"
                    %s\">
                            <div class=\"weui-media-box__bd\">
                                <a  href='Chat/index/course?courseid=$r[course_id]' class='course_title'>
                    $r[title]</a>
                                
                     <p class='weui-media-box__desc' >
                    $r[address]</p>
                    <p class='weui-media-box__desc'  >
                    $r[starttime]</p>
                     <p style='text-align: end'><i class='weui-media-box__desc_time'> $price </i> 
                  </p>

                               

                            </div>
                        </div>",SHOW_URL.$r['image']);
            }
            exit(json_encode(array('status'=>'finish','data'=>$str)));
        }





    }

    public function getDistance($lat1, $lng1, $lat2, $lng2)
    {
        $earthRadius = 6367000; //approximate radius of earth in meters
        $lat1 = ($lat1 * pi()) / 180;
        $lng1 = ($lng1 * pi()) / 180;
        $lat2 = ($lat2 * pi()) / 180;
        $lng2 = ($lng2 * pi()) / 180;
        $calcLongitude = $lng2 - $lng1;
        $calcLatitude = $lat2 - $lat1;
        $stepOne = pow(sin($calcLatitude / 2), 2) + cos($lat1) * cos($lat2) * pow(sin($calcLongitude / 2), 2);
        $stepTwo = 2 * asin(min(1, sqrt($stepOne)));
        $calculatedDistance = $earthRadius * $stepTwo;
        return round($calculatedDistance);

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

            //课程总人数
            $course=D('course')->where(array('course_id'=>session('course_id')))->find();
            $course['people_current']+=$data['people_count'];
            D('course')->save($course);
            
            if(session('aid'))
                $data['agent_openid']=session('aid');
            exit($trade->add($data));
        }

        $course=D('course');
        session('course_id',$course_id);
        $data=$course->where(array('course_id'=>$course_id))->find();
        $user_data=  $user->where(array('openid'=>session('openid')))->find();
        if($user_data)
            $data['bonus_current']=$user_data['bonus_current'];
        else
            $data['bonus_current']=0;

        $this->assign('data',$data);

        $this->assign('people_remain',$data['people_limit']-$data['people_current']);

        $this->display();
    }

    public function sortCategory(){
        $big_category=I('post.big_category');

        $category=I('post.category_name');
        if($category)
            $data =  D('course')->where(array("publish_state"=>1,"small_category"=>$category,'big_category'=>$big_category))->order('starttime desc')->select();
        else{
            $data =  D('course')->where(array("publish_state"=>1,'big_category'=>$big_category))->order('starttime desc')->select();

        }
        $str='';
        foreach ($data as $r){
            $price=$r['price']==0?'免费报名':($r['price'].'元');
            if($big_category=='专题活动')//时间配置
                $r['starttime']=$this->time_zhuanti($r['starttime']);
            else{
                $r['starttime']=$this->time_day($r['starttime']);
            }
            $str .=sprintf("  <div  class=\"weui-media-box weui-media-box_appmsg\"style='padding: 5px'>
                                <img onclick=\"javascript:window . location . href = 'Chat/index/course?courseid=$r[course_id]'\" style='width: 90px;height: 62px;vertical-align: top;margin-bottom: 15px'  src=\"
                    %s\">
                            <div class=\"weui-media-box__bd\">
                                <a  href='Chat/index/course?courseid=$r[course_id]' class='course_title'>
                    $r[title]</a>
                                
                     <p class='weui-media-box__desc' >
                    $r[address]</p>
                    
                     <p class='weui-media-box__desc'  >
                    $r[starttime]</p>
                    
                                <p style='text-align: end'><i class='weui-media-box__desc_time'> $price </i> 
                  </p>

                               

                            </div>
                        </div>",SHOW_URL.$r['image']);
        }
        exit(json_encode(array('status'=>'finish','data'=>$str)));
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
        $this->assign('agent',$this->user->getAgent());

        //判断0元试听
        if($data['price']==0||$data['price']=='0') {
            $this->assign('activity_state',D('user')->getAcitivity());
        }


//        http://www.jianpianzi.com/tpchat/index.php/Chat/trade?course_id=12&aid=&code=0011Fgud1gSwwv057xsd1a0xud11FguL&state=
        //重新获取没有注册的用户信息


        $signPackage =  $weObj->getJsSign();
        echo '<script src="https://res.wx.qq.com/open/js/jweixin-1.2.0.js"></script>
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
  var url=\'http://www.jianpianzi.com/tpchat/index.php/Chat/index/course?courseid='.$courseid.'&aid='.session('openid').'\';
          wx.onMenuShareTimeline({
              title: "'.$data['title'].'",
              desc :"'.$data['address'].'\r\n'.$data['starttime'].'",
              link: url,
              imgUrl: \''.SHOW_URL.$data['image'].'\'
              
          });
          
          wx.onMenuShareAppMessage({

            title:"'.$data['title'].'",
            desc :"'.$data['address'].'\n'.$data['starttime'].'",
            link: url,
              imgUrl: \''.SHOW_URL.$data['image'].'\'
});
  });
</script>
</html>';

        $this->display();
    }

    public function enroll(){
        $course_id=I('get.course_id');
        session('course_id',$course_id);

        $user=D('user')->where(array('openid'=>session('openid')))->find();
        $username=$user['chatname'];
        session('user_id',$user['user_id']);
        $this->assign('user',$user);
//        if(I('post.req_code')){
//            $phone=I('post.phone');
//            $code=mt_rand(1000,9999);
//            D('code')->add(array('phone'=>$phone,'code'=>$code.''));
//            exit($code.'');
//
//        }

        //验证验证码
        if(I('post.')){


            $phone=I('post.phone');
            $code=I('post.code');
//            $re=D('code')->where(array('phone'=>$phone,'code'=>$code))->find();
//            if($re){
                $userinfo=D('user')->create();
                $userinfo['user_id']=session('user_id');

                D('user')->where(array('openid'=>session('openid')))->save($userinfo);
                $data=array();
                $data['openid']=session('openid');
                $data['course_id']=session('course_id');
                $data['evidence']=D('trade')->getRandom(1,session('course_id'));
                //课程总人数
                $course=D('course')->where(array('course_id'=>session('course_id')))->find();
                $course['people_current']+=$data['people_count'];
                D('course')->save($course);

                //免费活动
                $data['trade_state']='已支付';
                D('user')->setAcitivity(1);
                exit(D('trade')->add($data));
            }


//        }

        $this->assign('username',$username);

        $this->display();
    }
}
