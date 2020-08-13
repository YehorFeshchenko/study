var net = require('net');

var client = net.connect({ port: 4444 }, function () {
    console.log('connected to server!');
});
client.on('data', function (data) {
    console.log(data.toString());
    setTimeout(res => {
        client.end();
    }, 30000);
});
client.on('end', function () {
    console.log('disconnected from server');
});