<?php
require_once("../lib/rb.php");
require_once("../db.php");
/*Require RedBeanPHP */
/*//////////////////////////////////////////////////////////////////////*/

$data = json_decode(file_get_contents("setup_logout.json"),true);
$error = 0;
session_start();
if(isset($data['myscript_start']))
{
	include($data['myscript_start'][0]);
	$data['myscript_start'][1]($data);
}

if($error==0)
{
	if(isset($data['advance']) and $data['advance'] == true and isset($data['tab']))
	{
		if(isset($_COOKIE['nvg_auth_user']))
		{
			$ses = R::findOne($data['tab'],"hash = ?",[$_COOKIE['nvg_auth_user']]);
			if($ses)
			{
				$domain = ($_SERVER['HTTP_HOST'] != 'localhost') ? $_SERVER['HTTP_HOST'] : false;

				$ses->hash = null;
				$ses->time = time();
				$ses->is_online = false;
				$ses->domain = $domain;
				R::store($ses);
				@setcookie("nvg_auth_user",$hash, -1,'/');
			}
			else
				$error = 4;
		}
		else
			$error = 3;
	}
	else
	{
		if(isset($_SESSION["nvg_auth_user"]) and isset($_SESSION["ua"]) and isset($_SESSION["ip"]))
		{
			unset($_SESSION['nvg_auth_user']);
			unset($_SESSION['ua']);
			unset($_SESSION['ip']);
		}
		else
			$error = 1;
	}

	if($error==0)
	{
		if(isset($data['success']))
		{
			include($data['success'][0]);
			$data['success'][1]($data);
		}
	}
}
else
{
	if (isset($data['error']))
	{
		include($data['error'][0]);
		$data['error'][1]($data, $error);
	}
}
echo $error;
exit();
?>