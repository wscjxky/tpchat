<?php
namespace Admin\Controller;
vendor('Wechat.wechat', '' ,'.php');
class UserController extends BaseController {
    public  function __construct() {
        parent::__construct();
        //message_result用户储存查询结果
        // 订单 支付 发货状态
        $this->weObj = new \Wechat();
        $this->user=D('user');
    }

    public function index(){
        $data=D('user')->select();
        foreach ($data as $user) {
            $trade_count=count($this->user->getTradeArr($user['openid']));
            if($trade_count==0){
                $user['user_level']='学弱';
            }
            else if($trade_count<=10){
                $user['user_level']='学民';

            }
            else if($trade_count<=50){
                $user['user_level']='学霸';

            }
            else if($trade_count<=100){
                $user['user_level']='学神';

            }
            else if($trade_count<=200){
                $user['user_level']='超神';

            }
            else if($trade_count<=500){
                $user['user_level']='专家';

            }
            else {
                $user['user_level']='大神';

            }
            D('user')->save($user);
        }
        $data=D('user')->select();
        foreach ($data as $user) {
            $trade_count=count($this->user->getTradeArr($user['openid']));
            if($trade_count==0){
                $user['user_level']='学弱';
            }
            else if($trade_count<=10){
                $user['user_level']='学民';

            }
            else if($trade_count<=50){
                $user['user_level']='学霸';

            }
            else if($trade_count<=100){
                $user['user_level']='学神';

            }
            else if($trade_count<=200){
                $user['user_level']='超神';

            }
            else if($trade_count<=500){
                $user['user_level']='专家';

            }
            else {
                $user['user_level']='大神';

            }
            D('user')->save($user);
        }
        foreach ($data as $key=>$user) {
            $data[$key]['agent']=D('user')->getAgent($user['agent']);
        }

        $this->assign('count',count($data));
        $this->assign('data',$data);
        $this->display();
    }

    public function sendLog(){
        if(I('post.')){
            $message_result=session('message_result');
            $data=M('log')->create();
            foreach ($message_result as $item){
                $data['openid']=  $item['openid'];
                $data['admin_id']=session('admin_id');
                $data['admin_username']=session('admin_username');
                var_dump($data);
                var_dump(M('log')->add($data));
            }
            $this->success('发送成功',U('User/index'));
        }
        $this->display();
    }

    public function sendTemple(){
            if(I('post.')) {
                $data = array(
                    'touser' => '',
                    'template_id' => "Uv50VGgxnVFYF-zxsKd5PSyowrVJ6-Pvc_fqIEGA934",
                    'url' => I('post.link'),
                    'appid' => "wxfdf007a79f182aed",
                    'pagepath' => "",
                    'data' => array(
                        "first" => array("value" => I('post.1'), "color" => "#173177"),
                        "keyword1" => array("value" => I('post.2'), "color" => "#173177"),
                        "keyword2" => array("value" => I('post.3'), "color" => "#173177"),
                        "keyword3" => array("value" => I('post.4'), "color" => "#173177"),
                        "remark" => array("value" => I('post.5'), "color" => "#173177")
                    )
                );
                $users = session('message_result');
                foreach ($users as $user) {
                    $data['touser'] = $user['openid'];
                    if ($this->weObj->sendTemplateMessage($data))
                        $this->success('发送成功', U('User/index'));
                }
            }


        $this->display();
    }

    public function message(){

        $data=M('user')->select();
        $this->assign('data',$data);
        $this->display();
    }

    public function timeSearch($keyword){
        $courses = D('course')->query("
                        SELECT*
             FROM  `course`  
            WHERE  title  like '%$keyword%' AND publish_state=1");
        $result_id=array();
        //得到时间段内指定课程题目的课程
        foreach ($courses as $item){
            if($this->compareTime(substr($item['starttime'],0,10))){
                array_push($result_id,$item['course_id']);
            }

        }
        if(empty($result_id)){
            return null;
        }
        //根据这些id查询用户
        $query='';
        foreach ($result_id as $id){
            $query.=$id.' or  b.course_id=';
        }
        $query.=$id;

        $result = M('user')->query("SELECT DISTINCT a.openid ,a.chatname,a.phone,a.province,a.gender,a.createtime,a.bonus_current,a.agent
             FROM  `user`  a

             INNER JOIN `trade` b

			ON  b.openid=a.openid
            WHERE  b.course_id  = $query");
        return $result;
    }


    public function compareTime($time)
    {
        $curr_time = strtotime($time);
        if(I('post.starttime')&&I('post.endtime')) {
            $timeBegin1 = strtotime(I('post.starttime'));
            $timeEnd1 = strtotime(I('post.endtime'));
            if ($curr_time >= $timeBegin1 && $curr_time <= $timeEnd1) {
                return true;
            }
            return false;

        }
        else if(I('post.starttime')&&!I('post.endtime')) {
            $timeBegin1 = strtotime(I('post.starttime'));
            if ($curr_time >= $timeBegin1) {
                return true;
            }
            return false;

        }
        else if(!I('post.starttime')&&I('post.endtime')) {
            $timeEnd1 = strtotime(I('post.endtime'));
            if ($curr_time <= $timeEnd1) {
                return true;
            }
            else
                return false;

        }
        else{
            return true;
        }

    }

    public function search()
    {
        $data_url = '';
        $result='';
        if ($keyword = I('post.keyword')) {
            if (I('post.act') == "course_title") {
//                $result = M('user')->query("
//                        SELECT DISTINCT a.openid ,a.chatname,a.phone,a.province,a.gender,a.createtime,a.bonus_current,a.agent
//             FROM  `user`  a
//
//            INNER JOIN `trade` b
//
//            ON  a.openid=b.openid
//
//            WHERE  b.course_title  like '%" . I('post.keyword') . "%'");
                $result=$this->timeSearch($keyword);
                if(!$result)
                    exit("没有查询到相关记录");
                //去重
                array_unique($result);
                foreach ($result as $v) {
                        $data_url .= "<tr>
                    <td >$v[openid]</td>
                    <td > $v[chatname]  </td>
                     <td > $v[phone]  </td>

                    <td > $v[province]    $v[city]  </td>
                    <td> $v[gender]  </td>
                    <td > $v[createtime]  </td>
                    <td > $v[bonus_current]  </td>
                    <td > $v[agent]  </td>
                </tr>";
                }

            }
            else if (I('post.act') == "user_name") {
                $result = M('user')->query("
                        SELECT *
             FROM  `user`  a

            WHERE  `chatname`  like '%" . $keyword . "%'");
                foreach ($result as $v) {
                    $data_url .= "<tr>
                    <td >$v[openid]</td>
                    <td > $v[chatname]  </td>
                    <td > $v[phone]  </td>
                    <td > $v[province]    $v[city]  </td>
                    <td> $v[gender]  </td>
                    <td > $v[createtime]  </td>
                    <td > $v[bonus_current]  </td>
                    <td > $v[agent]  </td>
                </tr>";
                }
            }
        }



        else {
            $result = M('user')->select();
            foreach ($result as $v) {
                $data_url .= "<tr>
                    <td >$v[openid]</td>
                    <td > $v[chatname]  </td>
                    <td > $v[phone]  </td>
                    <td > $v[province]    $v[city]  </td>
                    <td> $v[gender]  </td>
                    <td > $v[createtime]  </td>
                    <td > $v[bonus_current]  </td>
                    <td > $v[agent]  </td>
                </tr>";
            }
        }
        if(!$result)
            exit("没有查询到相关记录");
        session('message_result',$result);
        $url_str = "<thead>
        <tr>
            <th>用户id</th>
            <th>用户微信名</th>
            <th>用户手机号</th>
            <th>用户地址</th>
            <th>用户性别</th>
            <th>关注时间</th>
            <th>用户积分</th>
            <th>顾问级别</th>
        </tr>
        </thead>
        <tbody> " . $data_url;
        exit(($url_str));
    }


    public function reply(){
        if($advice_id=I('get.advice_id')){
            if(IS_POST){
                $re=M('advice')->where(array('advice_id'=>$advice_id))->save(array('reply'=>I('post.content')));
                if($re)
                    $this->success('回复成功！',U('User/advice'));
            }
        }
        $this->display();

    }

    public function handlecash()
    {
        $user=$this->user->where(array('openid'=>I('post.id')))->find();
        $user['cash_cost']=$user['cash_submit'];
        $user['cash_submit']=0;
        D('user')->save($user);
        exit('ok');

    }
    public function handleagent()
    {
        $user=$this->user->where(array('openid'=>I('post.id')))->find();
        if(I('post.act')=='cancel')
            $user['agent']=0;
        if(I('post.act')=='confirm')
            $user['agent']=1;
        D('user')->save($user);
        exit('ok');


    }
}