var net = require('net');

var server = net.createServer(function (connection) {
    console.log('client connected');

    connection.on('end', function () {
        console.log('client disconnected');
    });
    connection.write('Hello World! 2\r\n');

    server.getConnections(function (error, count) {
        console.log("Number of TCP connections = " + count);
    })
    connection.pipe(connection);
});
server.listen(3333, function () {
    console.log('server2 is listening at port 3333');
});