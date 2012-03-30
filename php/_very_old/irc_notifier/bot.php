<?php

include 'db.php';

$db = new database();
$db->connect('localhost','spx_planet','root','');

$irc = new processing('irc.mozilla.org','6667','#mozilla-ru','spx','pass');
$irc->connect();
$irc->listening();

$db->close();

class irc {

	private $sock;
	private $last;
//	private $proc;
	public $state;

	function connect() {
		$this->sock = fsockopen($this->host,$this->port);
		$this->write('NICK '.$this->nick);
		while (!$this->eof($this->sock)) {
			$str=$this->gets();
			if (preg_match('/Looking up your hostname/i',$str)) {
				$this->write('USER '.$this->nick.' 0 0 '.$this->nick);
			} elseif (preg_match('/PING :([^\n]+)\n/i',$str,$m)) {
				$this->write('PONG :'.trim($m[1]));
			} elseif (preg_match('/'.$this->nick.' MODE/i',$str)) {
				$this->write('JOIN '.$this->channel);
				return 1;
			}
		}
		return 0;
	}

	function check_planet() {
		global $db;
		if ($db->num_rows($res=$db->query('SELECT posts.*, rss_list.user as user from posts INNER JOIN rss_list ON posts.rid=rss_list.id WHERE posts.id>'.($this->last_id?$this->last_id:'0').' ORDER by posts.id ASC'))) {
			while ($post=$db->fetch_array($res)) {
				$this->write('PRIVMSG '.$this->channel.' :Блоги: '.$post['user'].': '.$post['title'].' #'.$post['id']);
				$db->query('UPDATE posts SET `querys`="'.($post['querys']+1).'" WHERE id='.$post['id']);
				$this->last_id = $post['id'];
			}
		}
	}

	function eof() {
		return feof($this->sock);
	}

	function write($str) {
		return fwrite($this->sock,$str."\n");
	}

	function gets() {
		return fgets($this->sock);
	}

	function listening() {
		while ($this->state) {
			if ($this->last+10<time()) {
				$this->check_planet();
				$this->last = time();
			}
			$str = $this->gets();
//			$this->proc->check_string($str);
			$this->check_string($str);
		}
	}

	function close() {
		fclose($this->sock);
	}

}

class processing extends irc {

	public $last_id;

	function processing($host,$port,$channel,$nick,$pass) {
		global $db;
		$this->host = $host;
		$this->port = $port;
		$this->channel = $channel;
		$this->nick = $nick;
		$this->pass = $pass;
		$this->state = 1;
		if ($db->num_rows($res=$db->query('SELECT id from posts ORDER by id DESC LIMIT 1'))) {
			list($this->last_id) = $db->fetch_array($res);
		}
		if (!$this->last_id)
			$this->last_id = (string)'0';
		$this->last = time();
//		$this->proc = new processing();
	}

	function is_ping($str) {
		if (preg_match('/PING :([^\n]+)\n/i',$str,$m)) {
			$this->write('PONG :'.trim($m[1]));
			return 1;
		}
		return 0;
	}

	function to_bot($str) {
		if (preg_match('/:([^\!]+)\!([^\@]+)\@([^\s]+) ([^\s]+) ([^\s]+) :([^\n]+)\n/i',$str,$m)) {
			if ($m[4]=='PRIVMSG'&&trim($m[5])==$this->nick) {
				return Array('user'=>trim($m[1]),'text'=>trim($m[6]));
			}
		}
	}

	function content($str) {
		$str = html_entity_decode($str);
		$str = preg_replace('/<a(.*)href="([^"]+)"(.*)>([^<]+)<\/a>/isU','$4 ( $2 )',$str);
		$str = preg_replace('/<img(.*)src="([^"]+)"(.*)>/isU',' IMG ( $2 )',$str);
		$str = trim(strip_tags(preg_replace('/<br([\s]*)\/>/i',"\n",$str)));
//		if (strlen($str)>200) {
//			$str = substr($str,0,254).'...';
//		}
		return $str;
	}

	function content_split($str) {
		$str = preg_replace('([\n]+)',"\n",preg_replace('([\s]+)',' ',str_replace("\n"," ",$str)));
		if (preg_match_all('/([^\s\n]+)/i',$str,$m)) {
			$m = $m[1];
			$i = 0;
			foreach($m as $chunk) {
				if (strlen($out[$i])>220) {
					$i++;
				}
				if (strlen($out[$i].' '.$chunk)>220) {
					$i++;
				}
				if ($out[$i]) {
					$out[$i] .= ' ';
				}
				$out[$i] .= $chunk;
			}
		} else {
			return Array((string)$str);
		}
		return $out;
	}

	function check_id($user,$id) {
		global $db;
		$id = (int)str_replace('#','',$id);
		if ($db->num_rows($res=$db->query('SELECT posts.*, rss_list.user as user from posts INNER JOIN rss_list ON posts.rid=rss_list.id WHERE posts.id='.$id))) {
			$post = $db->fetch_array($res);
			$this->write('PRIVMSG '.$user.' :'.$post['user']);
			$this->write('PRIVMSG '.$user.' :'.$post['title']);
			$c = $this->content_split($this->content($post['content']));
//			$c = explode("\n",$content);
			foreach ($c as $str) {
				$str = trim($str);
				$this->write('PRIVMSG '.$user.' :'.$str);
			}
			$this->write('PRIVMSG '.$user.' :'.$post['link']);
		}
	}

	function send_last($user,$num) {
		global $db;
		$num = (int)$num;
		if (!$num)
			$num = 10;
			if ($db->num_rows($res=$db->query('SELECT posts.*, rss_list.user as user from posts INNER JOIN rss_list ON posts.rid=rss_list.id ORDER by id DESC LIMIT '.$num))) {
				while ($post=$db->fetch_array($res)) {
					$this->write('PRIVMSG '.$user.' :'.$post['user'].': '.$post['title'].' #'.$post['id']);
				}
				$this->write('PRIVMSG '.$user.' :end;');
			}
	}

	function check_string($str) {
		if (!$this->is_ping($str)) {
			if ($r=$this->to_bot($str)) {
				$mess = $r['text'];
				if (strstr($mess,' ')) {
					$t = explode(' ',$mess);
				} else {
					$t[0] = $mess;
				}
				switch ($t[0]) {
					case 'last':
						$this->send_last($r['user'],$t[1]);
						break;
					case 'link':
						
						break;
					case 'text':
						
						break;
					default:
						$this->check_id($r['user'],$t[0]);
				}
			}
		}
	}

}

?>