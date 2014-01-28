<?php

class PageController extends Controller {

	private $data = array();

	public function indexAction() {
		$pageModel = $this->model('page');
		$alias = xsCleanLatinName($this->httpRequest->arg(0)?$this->httpRequest->arg(0):'index');
		$pageModel->__set('alias',$alias);
		$pageModel->read($alias);
		$this->data = $pageModel->__get_array();
	}

	public function indexView() {
		$pageView = $this->view('page');
		$pageView->setData($this->data);
		$pageView->view();
	}

}

?>