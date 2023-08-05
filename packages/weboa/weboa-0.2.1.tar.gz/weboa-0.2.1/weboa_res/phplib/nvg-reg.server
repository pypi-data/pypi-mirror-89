<?php
require_once("../lib/rb.php");
require_once("../db.php");
/*Require RedBeanPHP */
/*//////////////////////////////////////////////////////////////////////*/

$options = json_decode(file_get_contents("setup_reg.json"),true);
$data = $_POST['cols'];

if(isset($options['myscript_start']))
{
	include($options['myscript_start'][0]);
	$options['myscript_start'][1]($data, $options);
}

function array_merge_in($el)
{
	if(count($el) != 1)
		$el = array_merge(...$el);
	return $el;
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

function checkRep($el)
{
	if(count($el) > 1)
		return count(array_unique($el)) === 1;
	else
		return true;
}

function checkReq($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, $options['req']))
		return !empty(trim($el));
	else
		return true;
}

function checkUni($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, $options['uniq']))
		return !R::find($options['tab'], $column.' = ?',array($el));
	else
		return true;
}

function whitelist($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, array_keys($options['whitelist'])))
	{
		if(count(array_unique(array_merge(str_split($el),$options['whitelist'][$column]))) == count(array_unique($options['whitelist'][$column])))
			return true;
		else
		{
			if(is_array($options['whitelist_force']))
			{
				if(isset($options['whitelist_force'][$column]))
				{
					if($options['whitelist_force'][$column]==0)
					{
						global $data;

						preg_match_all("/(".implode($options['whitelist'][$column], '|').")/", $el, $matches);
						$data[$column][0] = implode($matches[0],'');
					}
					else
						return false;
				}
				else
					return false;
			}
			else
			{
				if($options['whitelist_force']==0)
				{
					global $data;

					preg_match_all("/(".implode($options['whitelist'][$column], '|').")/", $el, $matches);
					$data[$column][0] = implode($matches[0],'');
				}
				else
					return false;
			}
		}
	}
	else
		return true;
}

function blacklist($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, array_keys($options['blacklist'])))
	{
		if($c != 0)
		{
			if(is_array($options['blacklist_force']))
			{
				if(isset($options['blacklist_force'][$column]) and $options['blacklist_force'][$column]==0)
				{
					global $data;
					$data[$column][0] = str_replace($options['blacklist'][$column],'',$el,$c);
					return true;
				}
				else
					return false;
			}
			else
			{
				if($options['blacklist_force']==0)
				{
					global $data;
					$data[$column][0] = str_replace($options['blacklist'][$column],'',$el,$c);
					return true;
				}
				else
					return false;
			}
		}
		else
			return true;
	}
	else
		return true;
}

function checkEmail($column, $el, $TorF)
{
	if(!$TorF)
		return true;
	
	global $options;

	if(in_array($column, $options['email']))
		return filter_var($el, FILTER_VALIDATE_EMAIL);
	else
		return true;
}

function checkMinLen($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, array_keys($options['minlen'])))
		return strlen($el) > $options['minlen'][$column];
	else
		return true;
}

function checkMaxLen($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, array_keys($options['maxlen'])))
		return strlen($el) < $options['maxlen'][$column];
	else
		return true;
}

function checkRules($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	
	if(in_array($column, array_keys($options['rule'])))
		return !empty( array_intersect(str_split($el), array_merge_in($options['rule'][$column])[0]) );
	else
		return true;
}

function Ntrim($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;
	return in_array($column, array_keys($options['ntrim'])) and in_array($el[0], array_map('strval',$options['ntrim'][$column]),true);
}

function checkTempEmail($column, $el, $TorF)
{
	if(!$TorF)
		return true;

	global $options;

	if(in_array($column, $options['tempEmail']))
	{
		$curl = curl_init("https://api.nvg-group.com/tempEmail.php?list");
	    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
	    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
	    $res = curl_exec($curl);
	    curl_close($curl);
	    $res = json_decode($res,true);

		return !in_array($el, $res);
	}
	else
		return true;
}

function HtmlSpChars($column, $TorF)
{
	if(!$TorF)
		return true;

	global $options, $data;
	
	if(in_array(strtolower($column), $options['html']))
		$data[$column][0] = htmlspecialchars($data[$column][0]);

}

function makeSpaces($column, $TorF)
{
	if(!$TorF)
		return true;

	global $options, $data;
	
	if(in_array(strtolower($column), $options['nospace']) || in_array(strtolower($column), $options['hash']))
		$data[$column][0] = trim($data[$column][0]);
	else
		$data[$column][0] = preg_replace('/\s+/', '', trim($data[$column][0]));

}

function makeCase($column, $TorF)
{
	if(!$TorF)
		return true;
	
	global $options, $data;

	if(in_array(strtolower($column), array_keys($options['case'])))
	{
		switch ($options['case'][strtolower($column)][0]) {
			case 1:
				if($options['case'][strtolower($column)][1]==1)
					$data[$column][0][0] = strtoupper($data[$column][0][0]);
				else
					$data[$column][0] = strtoupper($data[$column][0]);
				break;

			case -1:
				if($options['case'][strtolower($column)][1]==1)
					$data[$column][0][0] = strtolower($data[$column][0][0]);
				else
					$data[$column][0] = strtolower($data[$column][0]);
				break;

			default:
				return true;
				break;
		}
	}
	else
		return true;

}

function makeHash($column, $TorF)
{
	if(!$TorF)
		return true;

	global $options, $data;
	
	if(in_array(strtolower($column), $options['hash']))
		$data[$column][0] = password_hash($data[$column][0], PASSWORD_BCRYPT, ['cost' => 12]);
	else
		$data[$column][0] = strip_tags($data[$column][0]);
}

function cutUTF($column, $TorF)
{
	if(!$TorF)
		return true;

	global $options, $data;
	
	if(in_array(strtolower($column), $options['utf8']))
		$data[$column][0] = preg_replace('/[\x00-\x1F\x7F\xA0]/u', '', $data[$column][0]);
}

/*///////PROGRAM///////*/

$error = 0;

if(isset($options['tab']))
{
	$di = R::dispense($options['tab']);

	if(isset($options['g-recaptcha']))
	{
		if(!empty($data["g-recaptcha"]))
		{
			if(!googleCheck($options['g-recaptcha'][1], $data["g-recaptcha"]))
				$error = '12';
		}
		else
			$error = '12';
	}

	if(isset($options['recaptcha']))
	{
		if(!empty($data["recaptcha"]))
		{
			if(!googleCheck($options['recaptcha'][1], $data["recaptcha"][0]))
				$error = '12';
		}
		else
			$error = '12';
	}

	if($error == '12')
	{
		echo $error;
		die();
	}

	foreach ($data as $key1 => $value1)
	{
		if($key1=="recaptcha" or $key1=="g-recaptcha")
			continue;

		if(isset($options['hidecols']) and in_array($key1, $options['hidecols']))
			continue;

		$column = strtolower($key1);
		$my_element = strtolower($value1[0]);

		if(isset($options['autoauth']))
		{
			if(isset($options['autoauth_id']) and $key1 == $options['autoauth_id'])
				$autoauth_id = $key1;
		}

		if(checkRep($value1))
		{
			if(checkReq($column, $my_element, isset($options['req'])))
			{
				if(checkUni($column, $my_element, isset($options['uniq'])))
				{
					if(whitelist($column, $my_element, isset($options['whitelist'])))
					{
						if(blacklist($column, $my_element, isset($options['blacklist'])))
						{
							if(Ntrim($column, $value1[0], isset($options['ntrim'])))
							{
								if(checkEmail($column, $value1[0], isset($options['email'])))
								{
									if(checkMinLen($column, $my_element, isset($options['minlen'])))
									{
										if(checkMaxLen($column, $my_element, isset($options['maxlen'])))
										{
											if(checkRules($column, $my_element, isset($options['rule'])))
											{
												HtmlSpChars($key1, isset($options['html']));
												makeSpaces($key1, isset($options['nospace']));
												makeCase($key1, isset($options['case']));
												makeHash($key1, isset($options['hash']));
												cutUTF($key1, isset($options['utf8']));
												$di->$column = $data[$key1][0];
											}
											else
											{
												$error = '11 '.$column;
												break;
											}
										}
										else
										{
											$error = '10 '.$column;
											break;
										}
									}
									else
									{
										$error = '9 '.$column;
										break;
									}
								}
								else
								{
									$error = '8 '.$column;
									break;
								}
							}
							else
							{
								$error = '7 '.$column;
								break;
							}
						}
						else
						{
							$error = '6 '.$column;
							break;
						}
					}
					else
					{
						$error = '5 '.$column;
						break;
					}
				}
				else
				{
					$error = '4 '.$column;
					break;
				}
			}
			else
			{
				$error = '3 '.$column;
				break;
			}
		}
		else
		{
			$error = '2 '.$column;
		}
	}

	if(isset($options['excols']))
	{
		foreach ($options['excols'] as $key2 => $value2)
		{
			if(isset($value2))
			{
				if(is_array($value2))
				{
					if($value2[0] == "func" and count($value2) > 1 and is_string($value2[1]))
					{
						if(isset($value2[2]))
							$di->$key2 = $value2[1](json_encode($value2[2]));
						else
							$di->$key2 = $value2[1]();
					}
					else
						$di->$key2 = json_encode($value2);
				}
				else
					$di->$key2 = $value2;
			}
			else
				$di->$key2 = NULL;
		}
	}

}
else
	$error = 1;

if($error==0)
{
	R::store($di);

	if(isset($options['autoauth']))
	{
		if($autoauth_id)
		{
			$user = R::findOne($options['tab'],strtolower($autoauth_id)." = ?",[$data[$autoauth_id][0]]);

			if($user)
			{
				session_start();
				
				$_SESSION['nvg_auth_user'] = $user->id;
				$_SESSION['ua'] = $_SERVER['HTTP_USER_AGENT'];
				$_SESSION['ip'] = $_SERVER['REMOTE_ADDR'];

				if(isset($options['autoauth_advance']) and $options['autoauth_advance'] == "true")
				{
					$domain = ($_SERVER['HTTP_HOST'] != 'localhost') ? $_SERVER['HTTP_HOST'] : false;
					$hash = hash("sha256",$user->id);

					setcookie("nvg_auth_user",$hash, time() + 1296000,'/');
					$ses = R::dispense($options['autoauth_tab2']);
					
					$ses->user_ide = $user->id;
					$ses->ses_ide = session_id();
					$ses->user_agent = $_SERVER['HTTP_USER_AGENT'];
					$ses->ip = $_SERVER['REMOTE_ADDR'];
					$ses->hash = $hash;
					$ses->time = time();
					$ses->ftime = time();
					$ses->is_online = true;
					$ses->time2 = 1296000;
					$ses->domain = $domain;
					R::store($ses);
				}
			}
		}
	}
	if (isset($options['successreg']))
	{
		include($options['successreg'][0]);
		$options['successreg'][1]($options, $data);
	}
}
else
{
	if (isset($options['errorreg']))
	{
		include($options['errorreg'][0]);
		$options['errorreg'][1]($options, $data, $error);
	}
}

echo $error;
?>