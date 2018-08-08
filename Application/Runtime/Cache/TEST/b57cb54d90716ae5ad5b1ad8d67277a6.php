<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>这个是数组的遍历！！！</h1><br>
<?php if(is_array($arr)): foreach($arr as $k=>$vo): ?><h1>这个是数组的value:<?php echo ($vo); ?></h1><?php endforeach; endif; ?>

<br>

<h1>这个是字典的遍历！！！</h1><br>
<?php if(is_array($dic)): foreach($dic as $k=>$vo): ?><h1>这个是字典的key:<?php echo ($k); ?></h1><br>
    <h1>这个是字典的value:<?php echo ($vo); ?></h1><?php endforeach; endif; ?>



</body>
</html>