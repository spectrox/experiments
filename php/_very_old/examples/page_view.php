<?php

class PageView extends View {

	public $data = array();

	public function setData(&$data) {
		$this->data =& $data;
		$this->data['is_admin'] = false;
		if ($this->httpRequest->arg(0)=='admin') {
			$this->data['is_admin'] = true;
		}
		$this->data['headline'] = $this->data['title'];
		$autoloader = AutoLoader::getInstance();
		if (!$this->data['title']) 
			$this->data['title'] = $autoloader->config('default_title');
		if (!$this->data['keywords'])
			$this->data['keywords'] = $autoloader->config('default_keywords');
		if (!$this->data['description'])
			$this->data['description'] = $autoloader->config('default_description');
	}

	public function view() {
		if ($this->httpRequest->is_ajax()) {
			header('Content-type: text/xml');
		}
		$suffix = ($this->httpRequest->is_ajax()?'_ajax':'');
		if ($this->httpRequest->query()=='') {
			$view = 'base';
		} else {
			$view = 'page';
		}
		$view .= $suffix;
		$this->load($view);
	}

}

?>