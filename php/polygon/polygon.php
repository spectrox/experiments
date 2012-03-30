<?php

class Polygon {

	protected $polygon = array();

	/**
	 * Polygon itself, with basic vector-based structure
	 * Array: [ [1,1], [2,1], [3,0], [2,-1] ]
	 *
	 * @var $polygon array
	 */

	public function set_polygon($polygon) {
		if (count($polygon)<3) return false;
		if (!isset($polygon[0]['x'])) {
			foreach ($polygon as &$point) {
				$point = array('x' => $point[0], 'y' => $point[1]);
			}
		}
		$this->polygon = $polygon;
	}

	/**
	 * Check if $polygon contains $test value
	 *
	 * @var $test array(x=>decimal, y=>decimal)
	 */

	public function calc($test) {
		$q_patt= array( array(0,1), array(3,2) );
		$end = end($this->polygon);
		$pred_pt = end($this->polygon);
		$pred_pt['x'] -= $test['x'];
		$pred_pt['y'] -= $test['y'];
		$pred_q = $q_patt[$pred_pt['y']<0][$pred_pt['x']<0];
		$w = 0;
		for ($iter = reset($this->polygon); $iter!==false;$iter=next($this->polygon)) {
			$cur_pt = $iter;
			$cur_pt['x'] -= $test['x'];
			$cur_pt['y'] -= $test['y'];
			$q = $q_patt[$cur_pt['y']<0][$cur_pt['x']<0];
			switch ($q-$pred_q) {
				case -3:
					++$w;
					break;
				case 3:
					--$w;
					break;
				case -2:
					if ($pred_pt['x']*$cur_pt['y']>=$pred_pt['y']*$cur_pt['x'])
						++$w;
					break;
				case 2:
					if (!($pred_pt['x']*$cur_pt['y']>=$pred_pt['y']*$cur_pt['x']))
						--$w;
					break;
			}
			$pred_pt = $cur_pt;
			$pred_q = $q;
		}
		
		return $w!=0;
	}

}

?>
