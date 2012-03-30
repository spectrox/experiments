<?php

include 'db.php';

$db = new database();
$db->connect('localhost','spx_planet','root','');

$rss = new rss();
$rss->parse_list();

$db->close();

class rss {

	function parse(&$rss) {
		global $db;
		$xml = new SimpleXMLElement($rss['link'],0,1);
		$i = 0;
		foreach ($xml->children() as $x) {
//			print_r($x);
			if ($x->id&&$x->id==$rss['last']) break;
			if ($x->id) {
				if (!$i) {
					$new = $x->id;
					$i = 1;
				}
				$l = $x->link[sizeof($x->link)-1];
				$r = $l->attributes();
				$link = $r['href'];
				if ($x->content) {
					$text = $x->content;
				} elseif ($x->summary) {
					$text = $x->summary;
				}
				if (!$db->num_rows($db->query('SELECT * from posts WHERE `link`="'.$db->escape_string($link).'"'))) {
					$db->query('INSERT into posts (`rid`,`time`,`title`,`content`,`link`) VALUES ("'.$rss['id'].'","'.time().'","'.$db->escape_string($x->title).'","'.$db->escape_string($text).'","'.$db->escape_string($link).'")');
				}
			}
			//echo print_r($x)."\n";
		}
		//$db->query('UPDATE rss_list SET last="'.$db->escape_string($new).'" WHERE id='.$rss['id']);
	}

	function parse_list() {
		global $db;
		if ($db->num_rows($res=$db->query('SELECT * from rss_list ORDER by id ASC'))) {
			while ($rss=$db->fetch_array($res)) {
				$this->parse($rss);
			}
		}
	}

}

?>