<?php
require_once("../lib/rb.php");
require_once("../db.php");
/*Require RedBeanPHP */
/*//////////////////////////////////////////////////////////////////////*/

if(!isset($_POST) or empty($_POST))
	die();

$options = json_decode(file_get_contents("setup_auth.json"),true);
$data = $_POST['cols'];

if(isset($options['myscript_start']))
{
	include($options['myscript_start'][0]);
	$options['myscript_start'][1]($data, $options);
}

foreach ($data as $key => $value)
{
	if(preg_match('/[A-Z]/', $key)){
		$data[strtolower($key)] = $value;
		unset($data[$key]); 
	}
}

function in_array_all($needles, $haystack, $any = false) {
	if($any)
		return !empty(array_intersect($needles, $haystack));
	else
   		return empty(array_diff($needles, $haystack));
}

function googleCheck($secret, $gresp)
{
	$url = 'https://www.google.com/recaptcha/api/siteverify';
	$url_data = array('secret' => $secret, 'response' => $gresp, 'remoteip' => $_SERVER['REMOTE_ADDR']);
	$curl = curl_init($url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($url_data));
    $res = curl_exec($curl);
    curl_close($curl);
    $res = json_decode($res);
    return $res->success;
}

function checkMinLen($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, array_keys($options['minlen'])))
	{
		return strlen($el) > $options['minlen'][$column];
	}
	else
		return true;
}

function checkMaxLen($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, array_keys($options['maxlen'])))
	{
		return strlen($el) < $options['maxlen'][$column];
	}
	else
		return true;
}

/*///////PROGRAM///////*/

$error = "0";

if(isset($options['tab']))
{
	if(isset($options['g-recaptcha']))
	{
		if(!empty($data["g-recaptcha"]))
		{
			if(!googleCheck($options['g-recaptcha'][1], $data["g-recaptcha"]))
				$error = '2';
		}
		else
			$error = '2';
	}
	if(isset($options['recaptcha']))
	{
		if(!empty($data["recaptcha"]))
		{
			if(!googleCheck($options['recaptcha'][1], $data["recaptcha"]))
				$error = '2';
		}
		else
			$error = '2';
	}

	if($error == '2')
	{
		echo json_encode([$error,0]);
		exit();
	}

	if(!is_array($options['login']))
		$options['login'] = [$options['login']];

	if(in_array_all($options['login'], array_keys($data)))
	{
		if(in_array($options['password'], array_keys($data)))
		{
			$user = 0;
			for($i = 0; $i < count($options['login']); $i++)
			{
				$col_lg = strtolower($options['login'][$i]);
				$col_ps = strtolower($options['password']);

				$user = R::findOne($options['tab'],$col_lg." = ?",[$data[$col_lg]]);
				if($user && !in_array($_SERVER['REMOTE_ADDR'], $options['denyip']) )
				{
					if(checkMaxLen($col_lg,$data[$col_lg],isset($options['maxlen'])) && checkMaxLen($col_ps,$data[$col_ps],isset($options['maxlen'])))
					{
						if(checkMinLen($col_lg,$data[$col_lg],isset($options['minlen'])) && checkMinLen($col_ps,$data[$col_ps],isset($options['minlen'])))
						{
							if(password_verify($data[$col_ps],$user->$col_ps))
							{
								if(isset($options['excols']))
								{
									$eeee = 0;
									foreach ($options['excols'] as $key2 => $value2)
									{
										if(!R::findOne($options['tab'],$col_lg." = ? and ".$key2.$value2[0]."?",[$data[$col_lg],$value2[1]]))
										{
											$eeee = 1;
											$error = '10';
											break;
										}
									}
									if($eeee==0)
										$error = '0';
								}
								else
									$error = '0';
							}
							else
								$error = '9';
						}
						else
							$error = '8';
					}
					else
						$error = '7';
				break;
				}
				else
					$error = '6';
			}
		}
		else
			$error = '5';
	}
	else
		$error = '4';
}
else
	$error = 1;

$is2fa = false;
if($error=="0")
{
	session_start();
	if($user)
	{
		$is2fa = (isset($user->f2a_active)) ? $user->f2a_active : false;
		$_SESSION['nvg_auth_user'] = $user->id;
		$_SESSION['ua'] = $_SERVER['HTTP_USER_AGENT'];
		$_SESSION['ip'] = $_SERVER['REMOTE_ADDR'];

		if(isset($options['advance']) and $options['advance'] == "true")
		{
			if( isset($options['remtime']) and isset($data['remember']) and $data['remember'] == "true")
				$time2 = $options['remtime'];
			else if(isset($options['logtime']))
				$time2 = $options['logtime'];
			else
				$time2 = 300;

			$domain = ($_SERVER['HTTP_HOST'] != 'localhost') ? $_SERVER['HTTP_HOST'] : false;

			$hash = hash("sha256",$user->id);

			if(isset($options['limitip']))
			{
				if(count(R::find($options['tab2'],"ip = ? and is_online = ? and user_ide = ?",[$_SERVER['REMOTE_ADDR'],1,$user->id])) > $options['limitip'])
				{
					$error = '11';
					echo json_encode([$error,$is2fa]);
					exit();
				}
			}	

			if(R::findOne($options['tab2'],"ip = ? and user_ide = ? and ban = 1 LIMIT 1",[$_SERVER['REMOTE_ADDR'],$user->id]))
			{
				$error = '12';
				echo json_encode([$error,$is2fa]);
				exit();
			}

			if(!$is2fa)
			{		
				if(strval($options['hsessions']) == "all")
					$ses = R::findOne($options['tab2'],"hash = ?",[$hash]);
				else
					$ses = R::findOne($options['tab2'],"ip = ? and user_ide = ?",[$_SERVER['REMOTE_ADDR'],$user->id]);

				if(!$ses)
					$ses = R::dispense($options['tab2']);

				setcookie("nvg_auth_user",$hash, time() + $time2,'/');
				
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
		}
	}
}
else
{
	if (isset($options['errorauth']))
	{
		include($options['errorauth'][0]);
		$options['errorauth'][1]($options, $data, $error);
	}
}


echo json_encode([$error,$is2fa]);
exit();
?>