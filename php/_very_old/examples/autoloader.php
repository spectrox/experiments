<?php

defined('__XS_STANDALONE') or define('__XS_STANDALONE',true);

define('__XS_PRIVATE',__DIR__);

header('Cache-Control: no-store, no-cache, must-revalidate');
header('Cache-Control: post-check=0, pre-check=0',false);
header('Pragma: no-cache'); 

session_start();

$autoloader = AutoLoader::getInstance();

class AutoLoader {

	private static $_instance;
	private static $db;
	private static $config = array();
	private static $controller = '';
	private static $action = '';
	private static $params = array();
	private static $controllerClass;

	public static function getInstance() {
		if (!(self::$_instance instanceof self)) {
			self::$_instance = new self();
		}
		return self::$_instance;
	}

	public function config($name,$val='') {
		if ($val) {
			$this->config[$name] = $val;
		} else {
			return $this->config[$name];
		}
	}

	public function mod_exists($name,$type) {
		$type = preg_replace('/[^a-zA-Z0-9\-_\.]/','',$type);
		$name = preg_replace('/[^a-zA-Z0-9\-_\.]/','',$name);
		if (!strstr($name,'.php')) $name .= '.php';
		$mod = ($type?$type.'/':'').$name;
		if (file_exists(__DIR__.'/'.$mod)) {
			return $mod;
		}
		return false;
	}

	public function load($name,$type='',$data=array()) {
		$mod = $this->mod_exists($name,$type);
		if ($mod) {
			include_once __DIR__.'/'.$mod;
			return true;
		}
		return false;
	}

	private function configure() {
		$this->config = array(
				'default_controller'	=> 'page',
				'default_action'		=> 'index',
				'default_title'			=> '',
				'default_keywords'		=> '',
				'default_description'	=> ''
			);
	}

	public function __construct() {
		$this->configure();
		$this->init();
	}

	private function checkCache() {
		$httpRequest = HttpRequest::getInstance();
		$cacheName = $httpRequest->getCacheName();
		$cacheFile = __DIR__.'/cache/'.$cacheName;
		if (file_exists($cacheFile)) {
			echo file_get_contents($cacheFile);
			return true;
		}
		return false;
	}

	private function init() {
		// check cache
		$this->load('httpRequest','components');
		if ($this->checkCache()) {
			return true;
		}
		// autoloading
		$components = array('mysql','controller','model','view','url','template');
		$helpers = array('variable','lang');
		$models = array('variable');
		// loading helpers
		foreach ($helpers as $mod) {
			$this->load($mod,'helpers');
		}
		// loading components
		foreach ($components as $mod) {
			$this->load($mod,'components');
		}
		// loading models
		foreach ($models as $mod) {
			$this->load($mod,'models');
		}
		// init mysql
		$db = MySQL::getInstance();
		$db->connect();
		// default title
		$this->config('default_title',xsGetVariable('default_title'));
		$this->config('default_keywords',xsGetVariable('default_keywords'));
		$this->config('default_description',xsGetVariable('default_description'));
		// loading page controller
		$this->loadController();
	}

	private function loadController() {
		$httpRequest = HttpRequest::getInstance();
		if ($httpRequest->arg(0)&&
				$this->mod_exists(xsCleanLatinName($httpRequest->arg(0)),'controllers'))
		{
			$this->controller = xsCleanLatinName($httpRequest->arg(0));
			if ($httpRequest->arg(1)) {
				$this->action = xsCleanLatinName($httpRequest->arg(1));
			} else {
				$this->action = $this->config['default_action'];
			}
		} else {
			$this->controller = $this->config['default_controller'];
			$this->action = $this->config['default_action'];
		}
		$this->params = $httpRequest->getParams();
		$this->load($this->controller,'controllers');
	}

	public function start() {
		$controllerName = xsGetControllerName($this->controller);
		$actionName = xsGetActionName($this->action);
		if (!class_exists($controllerName)) return false;
		$this->controllerClass = new $controllerName();
		if (!method_exists($this->controllerClass,$actionName)) return false;
		call_user_func_array(array($this->controllerClass,$actionName),$this->params);
		if (method_exists($this->controllerClass,$this->action.'View')) {
			call_user_func_array(array($this->controllerClass,$this->action.'View'),array());
		} elseif (method_exists($this->controllerClass,'indexView')) {
			call_user_func_array(array($this->controllerClass,'indexView'),array());
		}
		$this->end();
	}

	public function end() {
		$db = MySQL::getInstance();
		$db->close();
	}

}

?>