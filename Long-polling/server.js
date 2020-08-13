const { ServiceBusClient } = require("@azure/service-bus");

const connectionString = process.env.SERVICE_BUS_CONNECTION_STRING || "Endpoint=sb://learnservicebus1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=hUU2wohQPP2QInENX4hphaO3C1Pnx5h6pa5aleLNjPg=";
const queueName = process.env.QUEUE_NAME || "learnqueue2";

async function sendMessage() {
    const sbClient = ServiceBusClient.createFromConnectionString(connectionString);
    const queueClient = sbClient.createQueueClient(queueName);
    const sender = queueClient.createSender();

    try {
        await sender.send("Hello Service Bus");
        await queueClient.close();
    } finally {
        await sbClient.close();
    }
}

/*async function receiveMessage() {
    const sbClient = ServiceBusClient.createFromConnectionString(connectionString);
    const queueClient = sbClient.createQueueClient(queueName);
    const receiver = queueClient.createReceiver(ReceiveMode.peekLock);

    const onMessageHandler = async (brokeredMessage) => {
        console.log(`Received message: ${brokeredMessage.body}`);
        await brokeredMessage.complete();
    };
    const onErrorHandler = (err) => {
        console.log("Error occurred: ", err);
    };

    try {
        receiver.registerMessageHandler(onMessageHandler, onErrorHandler, {
            autoComplete: false
        });

        await delay(5000);

        await receiver.close();
        await queueClient.close();
    } finally {
        await sbClient.close();
    }
}*/

const http = require('http');

let writeResopnse = function (res, count) {
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("Hello World!");
}

const server = http.createServer(function (req, res) {
    if (req) {
        sendMessage().catch((err) => {
            console.log("Error occurred: ", err);
        });
    }
    /*receiveMessage().catch((err) => {
        console.log("Error occurred: ", err);
    });*/
    writeResopnse(res);


}).listen(process.env.PORT || 3000);

console.log("server running on port 3000");