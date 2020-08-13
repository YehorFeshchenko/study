const { ServiceBusClient } = require("@azure/service-bus");

const connectionString = process.env.SERVICE_BUS_CONNECTION_STRING || "<connection string>";
const queueName = process.env.QUEUE_NAME || "<queue name>";

async function sendMessage() {
    const sbClient = ServiceBusClient.createFromConnectionString(connectionString);
    const queueClient = sbClient.createTopicClient(queueName);
    const sender = queueClient.createSender();
 
    try {
      for (let i = 0; i < 3; i++) {
        await sender.send("Hello Service Bus");
      }
      await queueClient.close();
    } finally {
      await sbClient.close();
    }
  }

 async function receiveMessage() {
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
  }
  
export {sendMessage, receiveMessage};