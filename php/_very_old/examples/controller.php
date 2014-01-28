<?php

class Controller {

	public static $autoloader;
	public static $httpRequest;

	public function __construct() {
		$this->autoloader =& AutoLoader::getInstance();
		$this->httpRequest =& HttpRequest::getInstance();
		// nothing here
	}

	public function indexAction() {
		
	}

	public function model($name) {
		$this->autoloader->load($name,'models');
		$modelName = xsGetModelName($name);
		return new $modelName();
	}

	public function view($name) {
		$this->autoloader->load($name,'views');
		$viewName = xsGetViewName($name);
		return new $viewName();
	}

}

?>