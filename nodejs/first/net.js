var net = require('net');
var clients = {};

var socket;

/* client's handler, single event handler needed to work with all client's
   connections */
net.createServer(function(socket) {
	socket.write('Hello server!\r\n');
	socket.on('data', function(buf) {
		// in case you'll be using telnet for testing needs
		buf = buf.toString().trim();
		if (buf == 't1') {
			socket.write('T1 fucking great!\r\n');
		} else if (buf == 't2') {
			socket.write('T2 sucks!\r\n');
		}
		//socket.write(buf);
	});
}).on('connection', function(socket) {
	// fixing new connection in the list
	console.log('Client ' + socket.fd + ' connected');
	clients[socket.fd] = socket;
	socket.on('close', function() {
		// killing connection on close event
		delete clients[socket.fd];
	});
}).listen(8080);

