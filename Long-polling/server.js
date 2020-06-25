const http = require('http');

let writeResopnse = function (res) {
    res.eventNames('data');
    res.write('Hello world!');
    res.end();
}

const server = http.createServer(function (req, res) {
    //console.log(req.url);
    setTimeout(result => writeResopnse(res, 60000))
}).listen(3000);

console.log('server running on port 3000');