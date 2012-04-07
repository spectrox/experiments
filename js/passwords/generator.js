
function GeneratePassword(options) {
	this.input = '';
	this.inputId = '';
	this.nSymbols = '';
	this.nMaxAttempts = 5;
	this.nAttempts = 10;
	this.nACount = 0;
	this.nCount = 0;
	this.result = '';
	this.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',0,1,2,3,4,5,6,7,8,9];
	this.lCount = this.letters.length-1;
	var self = this;
	this.start = function() {
		this.result = '';
		this.nACount = 0;
		this.nCount = 0;
		this.generate();
	}
	this.generate = function() {
			var n, s, t;
			if (self.nACount==0) self.nAttempts = Math.round(Math.random()*self.nMaxAttempts)+3;
			t = Math.round(Math.random()*self.lCount);
			s = self.letters[t];
			self.printResult(self.result+s);
			if (self.nACount==self.nAttempts) {
				self.result += s;
				self.nACount = 0;
				self.nCount++;
			} else {
				self.nACount++;
			}
			if (self.nCount<self.nSymbols) {
				setTimeout(self.generate,30);
			}
		}
	this.printResult = function(r) {
			this.input.val(r);
		}
	this.init = function(options) {
			this.inputId = options['input_id'];
			this.input = $('#'+options['input_id']);
			this.nSymbols = options['symbols'];
		}
	this.init(options);
}

function InputSlider(options) {
	this.blSlider = '';
	this.blSliderId = '';
	this.blValue = '';
	this.blValueId = '';
	this.blPointId = '';
	this.blTextId = '';
	this.nStart = 0;
	this.nEnd = 10;
	this.nValue = 0;
	this.mDown = false;
	this.mLeft = 0;
	this.mLast = 0;
	var self = this;
	this.addBlocks = function() {
			this.blSlider.addClass('slider');
			this.blSlider.css('width',((this.nEnd-this.nStart+1)*20)+'px');
			var o = 0, bl;
			for (var i=this.nStart;i<=this.nEnd;i++) {
				bl = $('<div class="slider_back"><span>'+i+'</span></div>').css('left',(o*20+1)+'px').appendTo(this.blSlider);
				if (i==this.nEnd) {
					bl.css('border-bottom-color','#fff');
				}
				o++;
			}
			$('<div class="slider_text" id="'+this.blTextId+'"></div>').appendTo(this.blSlider);
			$('<div class="slider_point" id="'+this.blPointId+'"></div>').appendTo(this.blSlider);
			if (this.blValue.val()!=1) {
				$('#'+this.blPointId).css('left',((this.blValue.val()-this.nStart)*20)+'px');
			}
		}
	this.setPosition = function(pageX,offsetLeft) {
			if (!self.mLast) self.mLast = offsetLeft;
			var diff = pageX-self.mLast;
			var p = self.mLeft+diff;
			self.mLeft = p;
			self.mLast = pageX;
			if (p<0) p = 0;
			if (p>20*(self.nEnd-self.nStart)) p = 20*(self.nEnd-self.nStart);
			var v = Math.round(p/20);
			p = v*20;
			v += self.nStart;
			$('#'+self.blValueId).val(v);
			//$('#'+self.blTextId).html(v);
			$('#'+self.blPointId).css('left',p+'px');
		}
	this.setEvents = function(self) {
			$('#gp_result').click(function() {
					$(this).select();
				});
			$('#'+self.blSliderId).mousedown(function(e) {
					self.mDown = true;
					self.setPosition(e.pageX,this.offsetLeft);
					self.mLeft = (parseInt($('#'+self.blPointId).css('left'))?parseInt($('#'+self.blPointId).css('left')):0);
					return false;
				});
			//$('#'+self.blPointId).mousedown(function(e) {
			//		self.mLeft = (parseInt($('#'+self.blPointId).css('left'))?parseInt($('#'+self.blPointId).css('left')):0);
			//		self.mLast = e.pageX;
			//		return false;
			//	});
			$('#'+self.blSliderId).mouseup(function(e) {
					self.mDown = false;
					return false;
				});
			$('#'+self.blSliderId).click(function(e) {
					self.setPosition(e.pageX,this.offsetLeft);
					return false;
				});
			$('#'+self.blSliderId).mousemove(function(e) {
					if (self.mDown) {
						var diff = e.pageX-self.mLast;
						var p = self.mLeft+diff;
						self.mLeft = p;
						self.mLast = e.pageX;
						if (p<0) p = 0;
						if (p>20*(self.nEnd-self.nStart)) p = 20*(self.nEnd-self.nStart);
						var v = Math.round(p/20);
						p = v*20;
						v += self.nStart;
						$('#'+self.blValueId).val(v);
						//$('#'+self.blTextId).html(v);
						$('#'+self.blPointId).css('left',p+'px');
					}
				});
		}
	this.init = function(options) {
			this.blSlider = $('#'+options['bl_slider']);
			this.blSliderId = options['bl_slider'];
			this.blPointId = this.blSliderId+'_point';
			this.blTextId = this.blSliderId+'_text';
			this.blValue = $('#'+options['bl_value']);
			this.blValueId = options['bl_value'];
			this.nStart = options['start'];
			this.nEnd = options['end'];
			this.nValue = (options['value']?options['value']:options['start']);
			this.addBlocks();
			this.setEvents(this);
		}
	this.init(options);
}

function WebDevPage() {
	this.page = '';
	this.content = '#content';
	this.pageHome = function() {
			var bl = this.createBlock('gen_pass');
			bl.html('<p>Welcome on-board!</p>');
			this.addBlock(bl);
		}
	this.pageRandom = function() {
			// password generator
			var bl = this.createBlock('gen_pass');
			bl.html('<h3>Password generator</h3><div class="fl"><p>Select number of symbols and press "&raquo;" button.</p><div id="gp_slider"></div><input type="hidden" name="gp_slider_value" id="gp_slider_value" value="8"/></div><div class="fl"><input type="submit" class="submit" value="&raquo;"/></div><div class="fr"><input type="text" id="gp_result" class="result" name="gp_result"/></div>');
			// password generating function
			this.addForm(bl,function() {
					var n = $('#gp_slider_value').val();
					var gp = new GeneratePassword({
							'input_id':	'gp_result',
							'symbols':	$('#gp_slider_value').val()
						});
					gp.start();
					return false;
				});
			var inputSlider = InputSlider({
					bl_slider: 'gp_slider',
					bl_value: 'gp_slider_value',
					start: 1,
					end: 16,
					value: 8
				});
			// end of password generator block
		}
	this.createBlock = function(cl) {
			return $('<div class="block'+(cl?' '+cl:'')+'"></div>');
		}
	this.addForm = function(obj,hnd) {
			var form = $('<form></form>').appendTo(this.content);
			obj.append('<div class="cb"></div>');
			form.html(obj);
			form.submit(hnd);
		}
	this.addBlock = function(bl) {
			bl.appendTo(this.content);
			$(this.content).append('<div class="cb"></div>');
		}
	this.clear = function() {
			$(this.content).html('');
		}
	this.set = function(hash) {
			this.page = hash;
			this.clear();
			switch (this.page) {
				case '#home':
					this.pageHome();
					break;
				case '#random':
					this.pageRandom();
					break;
			}
		}
}

function WebDev() {
	this.path = '';
	this.title = 'spectrox.ru — break down this fuckin\' world!';
	this.menuBlock = '#menu ul';
	this.page = null;
	var self = this;
	this.menu = {
			'#home':	'Home page',
			'#random':	'Random tools'
		}
	this.buildMenu = function() {
			for(item in this.menu) {
				$(this.menuBlock).append('<li><a href="'+item+'">'+item.charAt(1).toUpperCase()+item.substr(2)+'</a></li>');
			}
		}
	this.setTitle = function() {
			var title = self.menu[self.path] + ' | ' + self.title;
			$('head title').html(title);
		}
	this.checkLocation = function() {
			if (window.location.hash!=self.path) {
				self.setLocation(window.location.hash);
			} else if (window.location.hash=='') {
				window.location.hash = '#home';
			}
		}
	this.setLocation = function(hash) {
			self.path = hash;
			self.setTitle();
			self.page.set(hash);
		}
	this.setEvents = function() {
			setInterval(this.checkLocation,500);
		}
	this.init = function() {
			this.page = new WebDevPage();
			this.buildMenu();
			this.setEvents();
		}
	this.init();
}
