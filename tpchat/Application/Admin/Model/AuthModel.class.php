<?php
namespace Model;
use Think\Model;

//权限model模型类
class AuthModel extends Model{
	//自定义方法实现权限信息的添加
//	function saveData($authinfo){
//		//两个步骤
//		//根据已有的4个字段生成一条记录
//		$newid=$this->add($authinfo);
//		//根据新纪录的主键id进一步制作auth_path和auth_level
//		//auth_path处理：顶级/非顶级权限
//		if($authinfo['auth_pid']==0){
//			//顶级
//			$path=$newid;
//		}else{
//			//非顶级全路径：上级权限全路径-本身记录id值
//			$pinfo=$this->find($authinfo['auth_pid']);
//			$p_path=$pinfo['auth_path'];
//			$path=$p_path."-".$newid;
//		}
//		//auth_level处理:全路径变为数组后元素个数减一的结果
//		$level=count(explode('-',$path))-1;
//
//		$sql="update sw_auth set auth_path='$path',auth_level='$level' where auth_id='$newid'";
//		return $this->execute($sql);
//	}
//
	
}