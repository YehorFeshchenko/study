const http = require('http');

const data = JSON.stringify({
    firstName: "Low",
    lastName: "Skill",
    phoneNumber: 4444444444,
    isActive: true,
});

const options = {
    port: 3000,
    path: '/contacts/post',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length,
    }
};

/*let makeRequest = async function () {
    let data = '';

    const request = http.request(options, (response) => {
        response.on('data', (d) => {
            //process.stdout.write(d);
            data += d;
        })
    });

    request.on('error', (err) => {
        console.log(err);
    });

    request.write(data);
    request.end();
    await new Promise((resolve, reject) => {
        resolve(console.log('done'));
    });
}

makeRequest();*/ 

const req = http.request(options, (res) => {
    let data = '';

    console.log('Status Code:', res.statusCode);

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        console.log('Body: ', JSON.parse(data));
    });

}).on("error", (err) => {
    console.log("Error: ", err.message);
});

req.write(data);
req.end();