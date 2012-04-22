var net = require('net');

var socket;

function Messages() {
	// working as singleton
	if (typeof Messages.instance === 'object') {
		return Messages.instance;
	}
	Messages.instance = this;

	this.users = {};
	this.debug = true;

}

Messages.prototype = {
	'log': function(message) {
		if (this.debug) console.log(message);
	},
	'add': function(socket) {
		this.users[socket.fd] = {
			'socket': socket,
			'name':   'Noname #' + socket.fd
		};
		this.log('user added #' + socket.fd);
	},
	'rename': function(socket_fd, name) {
		this.users[socket_fd].name = name;
		this.log('user #' + socket_fd + ' renamed to ' + name);
	},
	'remove': function(socket_fd) {
		delete this.users[socket_fd];
		this.log('user removed #' + socket_fd);
	},
	'send': function(from_fd, to_fd, message) {
		this.users[to_fd].socket.write('message from '
			+ this.users[from_fd].name + ': ' + message + "\r\n");
		this.log('message from #' + from_fd + ' to #' + to_fd);
	},
	'sendAll': function(socket_fd, message) {
		for (var to_fd in this.users) {
			if (to_fd == socket_fd) continue;
			this.send(socket_fd, to_fd, message);
		}
		this.log('send all from #' + socket_fd);
	}
}

var Messages = new Messages();

/* client's handler, single event handler needed to work with all client's
   connections */
net.createServer(function(socket) {
	socket.write('Hello server!\r\n');
	socket.on('data', function(buf) {

		// in case you'll be using telnet for testing needs
		buf = buf.toString().trim();

		var result;
		var matches = {
			'name': /set name ([^\:]+)/i,
			'write': /write (.*)/
		};

		if (result = buf.match(matches.name)) {

			Messages.rename(socket.fd, result[1]);

		} else if (result = buf.match(matches.write)) {

			Messages.sendAll(socket.fd, result[1]);

		}
	});
}).on('connection', function(socket) {

	// fixing new connection in the list
	console.log('Client ' + socket.fd + ' connected');

	Messages.add(socket);

	socket.on('close', function() {
		Messages.remove(socket.fd);
	});

}).listen(8080);

