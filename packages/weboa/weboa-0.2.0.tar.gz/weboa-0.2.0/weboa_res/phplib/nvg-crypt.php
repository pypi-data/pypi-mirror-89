<?php
/*From PHP 5.6*/

class nvgCrypt
{
	public function __construct($private_key = 'ab86d144e3f080b61c7c2e43')
	{
		$this->pkey = $private_key;
	}

	public function encrypt($message, $cipher = "AES-128-CBC")
	{
		$ivlen = openssl_cipher_iv_length($cipher);
		$iv = openssl_random_pseudo_bytes($ivlen);
		$ciphertext_raw = openssl_encrypt($message, $cipher, $this->pkey, $options=OPENSSL_RAW_DATA, $iv);
		$hmac = hash_hmac('sha256', $ciphertext_raw, $this->pkey, $as_binary=true);
		$ciphertext = base64_encode( $iv.$hmac.$ciphertext_raw );
		return $ciphertext;
	}
	
	public function decrypt($ciphertext, $cipher = "AES-128-CBC")
	{
		$c = base64_decode($ciphertext);
		$ivlen = openssl_cipher_iv_length($cipher);
		$iv = substr($c, 0, $ivlen);
		$hmac = substr($c, $ivlen, $sha2len=32);
		$ciphertext_raw = substr($c, $ivlen+$sha2len);
		$message = openssl_decrypt($ciphertext_raw, $cipher, $this->pkey, $options=OPENSSL_RAW_DATA, $iv);
		$calcmac = hash_hmac('sha256', $ciphertext_raw, $this->pkey, $as_binary=true);
		return (hash_equals($hmac, $calcmac)) ? $message : 'Error';
	}
	
}

?>