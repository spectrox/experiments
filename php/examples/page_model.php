<?php

class PageModel extends Model {

	protected $id = 0;
	protected $alias = '';
	protected $title = '';
	protected $keywords = '';
	protected $description = '';
	protected $time = 0;
	protected $content = '';

	private $res = 0;

	public function __construct() {
		parent::__construct();
	}

	public function __set($name,$val) {
		$oldVal = $this->$name;
		$this->$name = $val;
		return $oldVal;
	}

	public function __set_array($data) {
		if (!is_array($data)) return false;
		foreach ($data as $k=>$v) {
			$this->__set($k,$v);
		}
	}

	public function create() {
		if (!$this->time) $this->time = time();
		$query = 'INSERT INTO `pages` '
					.'(`alias`,`title`,`keywords`,'
					.'`description`,`time`,`content`)'
				.'VALUES ("'.$this->db->escape_string($this->alias).'",'
						.'"'.$this->db->escape_string($this->title).'",'
						.'"'.$this->db->escape_string($this->keywords).'",'
						.'"'.$this->db->escape_string($this->description).'",'
						.'"'.$this->db->escape_string($this->time).'",'
						.'"'.$this->db->escape_string($this->content).'")';
		if ($this->db->query($query)) {
			$this->id = $this->db->insert_id();
			return true;
		}
		return false;
	}

	public function read($id='') {
		if ($id&&(int)$id==$id) {
			$this->__set('id',$id);
		} elseif ($id&&(int)$id!=$id) {
			$this->__set('alias',$id);
		}
		if ($this->alias) {
			$cond = '`alias`="'.$this->db->escape_string($this->alias).'"';
		} else {
			$cond = '`id`="'.(int)$this->id.'"';
		}
		$query = 'SELECT * FROM `pages` WHERE '.$cond;
		if ($this->db->query($query)) {
			$this->__set_array($this->db->fetch_array());
			return true;
		}
		return false;
	}

	public function read_list() {
		$query = 'SELECT * FROM `pages`';
		if ($this->db->query($query)) {
			return true;
		}
		return false;
	}

	public function clean() {
		$this->id = 0;
		$this->alias = '';
		$this->title = '';
		$this->keywords = '';
		$this->description = '';
		$this->time = 0;
		$this->content = '';
	}

	public function next() {
		if ($item=$this->db->fetch_array()) {
			$this->clean();
			$this->__set_array(&$item);
			return true;
		}
		return false;
	}

	public function update() {
		$query = 'UPDATE `pages` '
				.'SET `alias`="'.$this->db->escape_string($this->alias).'",'
					.'`title`="'.$this->db->escape_string($this->title).'",'
					.'`keywords`="'.$this->db->escape_string($this->keywords).'",'
					.'`description`="'.$this->db->escape_string($this->description).'",'
					.'`time`="'.$this->db->escape_string($this->time).'",'
					.'`content`="'.$this->db->escape_string($this->content).'" '
				.'WHERE `id`="'.(int)$this->id.'"';
		if ($this->db->query($query)) {
			return true;
		}
		return false;
	}

	public function delete() {
		if (!$this->id) return false;
		if ($this->db->query('DELETE FROM `pages` WHERE `id`="'.(int)$this->id.'"')) {
			return true;
		}
		return false;
	}

}

?>