var net = require('net');

var server = net.createServer(function (connection) {
    console.log('client connected');

    connection.on('end', function () {
        console.log('client disconnected');
    });
    connection.write('Hello World! 1\r\n');

    server.getConnections(function (error, count) {
        console.log("Number of TCP connections = " + count);
    })
    connection.pipe(connection);
});
server.listen(2222, function () {
    console.log('server1 is listening at port 2222');
});