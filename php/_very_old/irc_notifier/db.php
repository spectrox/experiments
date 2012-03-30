<?php

class database {

	private $mysql;

	function connect($db_host,$db_name,$db_user,$db_pass) {
		$this->mysql = mysql_connect($db_host,$db_user,$db_pass);
		mysql_select_db($db_name,$this->mysql);
	}

	function query($q) {
		return mysql_query($q,$this->mysql);
	}

	function escape_string($str) {
		return mysql_escape_string($str);
	}

	function num_rows($r) {
		return mysql_num_rows($r);
	}

	function fetch_array($r) {
		return mysql_fetch_array($r);
	}

	function fetch_assoc($r) {
		return mysql_fetch_assoc($r);
	}

	function insert_id() {
		return mysql_insert_id($this->mysql);
	}

	function affected_rows() {
		return mysql_affected_rows($this->mysql);
	}

	function close() {
		mysql_close($this->mysql);
	}

}

?>