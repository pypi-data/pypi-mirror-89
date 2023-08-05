<?php
require_once("../lib/rb.php");
require_once("../db.php");
/*Require RedBeanPHP */
/*//////////////////////////////////////////////////////////////////////*/

$options = json_decode(file_get_contents("setup_auth.json"),true);
if(isset($_POST['cols']))
	$data = $_POST['cols'];
else
	die();
$error = "0";

if(!isset($_POST['input']))
	die();

if($_POST['input'][0] != "0")
{
	$error = 1;
	echo $error;
	exit();
}

if($_POST['input'][1] != "1")
{
	$error = 1;
	echo $error;
	exit();
}

foreach ($data as $key => $value)
{
	if(preg_match('/[A-Z]/', $key)){
		$data[strtolower($key)] = $value;
		unset($data[$key]); 
	}
}

for($i = 0; $i < count($options['login']); $i++)
{
	$col_lg = strtolower($options['login'][$i]);
	$user = R::findOne($options['tab'],$col_lg." = ?",[$data[$col_lg]]);
	if($user) break;
}

if(!$user)
{
	$error = 1;
	echo $error;
	exit();
}

if(isset($_POST['f2ab']) and $_POST['f2ab'] == "1" and isset($_POST['f2abscript']))
	include(trim($_POST['f2abscript']).".php");
else
{
	require_once('../GoogleAuthenticator.php');
	$ga = new GoogleAuthenticator;

	if(isset($options['subproc']))
	{
		include $options['subproc'][0].".php"; 

		if(!$ga->checkCode($options['subproc'][1]($user),$_POST['f2a']))
		{
			echo 2;
			exit();
		}
	}
	else
	{
		if(!$ga->checkCode($user->f2a,$_POST['f2a']))
		{
			echo 2;
			exit();
		}
	}
}

if($error == "0")
{
	session_start();

	if(R::findOne($options['tab2'],"ip = ? and user_ide = ? and ban = 1 LIMIT 1",[$_SERVER['REMOTE_ADDR'],$user->id]))
	{
		$error = '12';
		echo $error;
		exit();
	}
	
	if( isset($options['remtime']) and isset($data['remember']) and $data['remember'] == "true")
		$time2 = $options['remtime'];
	else if(isset($options['logtime']))
		$time2 = $options['logtime'];
	else
		$time2 = 300;

	$domain = ($_SERVER['HTTP_HOST'] != 'localhost') ? $_SERVER['HTTP_HOST'] : false;
	$hash = hash("sha256",$user->id);

	if(strval($options['hsessions']) == "all")
		$ses = R::findOne($options['tab2'],"hash = ?",[$hash]);
	else
		$ses = R::findOne($options['tab2'],"ip = ? and user_ide = ?",[$_SERVER['REMOTE_ADDR'],$user->id]);

	if(!$ses)
		$ses = R::dispense($options['tab2']);

	setcookie("nvg_auth_user", $hash, time() + $time2,"/");
	
	$ses->user_ide = $user->id;
	$ses->ses_ide = session_id();
	$ses->user_agent = $_SERVER['HTTP_USER_AGENT'];
	$ses->ip = $_SERVER['REMOTE_ADDR'];
	$ses->hash = $hash;
	if(!isset($options['invis']) or $options['invis'] != "true")
	{
		$ses->time = time();
		$ses->is_online = true;
	}
	if(!$ses->ftime)
		$ses->ftime = time();
	$ses->time2 = $time2;
	$ses->domain = $domain;
	R::store($ses);
	if(isset($options['successauth']))
	{
		include($options['successauth'][0]);
		$options['successauth'][1]($options, $data);
	}
}

echo $error;
?>