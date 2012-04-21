var net = require('net');
var clients = {};

var socket;

net.createServer(function(socket) {
	socket.write('Hello server!\r\n');
	socket.on('data', function(buf) {
		buf = buf.toString().trim();
		if (buf == 't1') {
			socket.write('T1 fucking great!\r\n');
		} else if (buf == 't2') {
			socket.write('T2 sucks!\r\n');
		}
		//socket.write(buf);
	});
}).on('connection', function(socket) {
	console.log('Client ' + socket.fd + ' connected');
	clients[socket.fd] = socket;
	socket.on('close', function() {
		delete clients[socket.fd];
	});
}).listen(8080);

