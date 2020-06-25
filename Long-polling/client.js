const http = require('http');

const options = {
    port: 3000,
    path: '/',
    method: 'GET'
};

let counter = 0;

let makeRequest = async function () {
    const request = http.request(options, (response) => {
        response.on('data', (d) => {
            process.stdout.write(d);
            //console.log(response.url);
        })
    });

    request.on('error', (err) => {
        console.error(err);
    });

    request.end();
    await new Promise((resolve, reject) => {
        resolve(console.log('done'));
    });
}

for (var i = 0; i < 50000; i++) {
    makeRequest();
    console.log(counter++);
}