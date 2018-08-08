<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>这个是 <?php echo ($test); ?>!!!!!</h1>
<form method="get" action="get1">
    <a>你的名字：</a><input  type="text" name="name"><br>
    <a>你的年龄：</a><input  type="text" name="age"><br>
    <button type="submit">提交</button>
</form>

</body>
</html>