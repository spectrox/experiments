<?php

class Model {

	public $db;
	public $error_message = '';

	public function __construct() {
		$this->db = MySQL::getInstance();
	}

	public function __set($name,$value) {
		if (property_exists($this,$name)) {
			$this->$name =	$value;
		}
	}

	public function __set_array($data) {
		if (!is_array($data)) return false;
		foreach ($data as $_k=>$_v) {
			$this->__set($_k,$_v);
		}
	}

	public function __get($name) {
		if (property_exists($this,$name)) {
			return $this->$name;
		}
	}

	public function &__get_array() {
		$vars = get_class_vars(get_class($this));
		$items = array();
		foreach ($vars as $_k=>$_v) {
			$items[$_k] = $this->$_k;
		}
		return $items;
	}

	public function error() {
		return $this->error_message;
	}

	public function create() {
		$this->error_message = 'create function not defined';
		return false;
	}

	public function read() {
		$this->error_message = 'read function not defined';
		return false;
	}

	public function update() {
		$this->error_message = 'update function not defined';
		return false;
	}

	public function delete() {
		$this->error_message = 'delete function not defined';
		return false;
	}

}

?>