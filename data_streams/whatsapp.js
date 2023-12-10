// Supports ES6
// import { create, Whatsapp } from '@wppconnect-team/wppconnect';
const wppconnect = require('@wppconnect-team/wppconnect');
const fs = require('fs');

wppconnect.create({
    session: 'session-name', // Define your session name
    catchQR: (base64Qrimg, asciiQR, attempt, urlCode) => {
      console.log('QR Code received', attempt);
  
      // Convert base64 image to binary data
      let base64Image = base64Qrimg.split(';base64,').pop();
  
      // Save QR code as an image file
      fs.writeFile('qr.png', base64Image, { encoding: 'base64' }, function(err) {
        console.log('File created');
      });
    },
    statusFind: (statusSession, session) => {
      console.log('Status Session: ', statusSession);
      console.log('Session name: ', session);
    }
  })
  .then((client) => start(client))
  .catch((error) => console.log(error));
  

let output_message = ""

function message_handler(messages, i){
    let first_message = true
    for (const [key, message] of Object.entries(messages)) {
        timestamp = message['timestamp']
        const date = new Date(timestamp * 1000);
        const currentDate = new Date()
        const date_string = date.toLocaleTimeString('en-US');
        if(date.setHours(0,0,0,0) == currentDate.setHours(0,0,0,0)) {
            const isMedia = message['isMedia']
            if(isMedia){
                continue;
            }
            if (first_message){
                output_message += "Conversation "+i+": \n"
                first_message = false
            }
            output = ""
            content = message['content']
            
            fromMe = message['fromMe']
            if(fromMe){
                output+="Me  "
            }else{
                output+="Other person  "
            }
            isGroupMessage = message['isGroupMsg']
            if(isGroupMessage){
                output+="(From a group message)  "
            }
            output += date_string +": "
            output+=content+"\n\n"
            output_message+=output
        }
        
        
      }
    // for (const message in messages){
    //     console.log(message)
    //     const timestamp = message['timestamp']
    //     console.log(timestamp)
    //     const date = new Date(timestamp * 1000);
    //     const currentDate = new Date()

    //     const date_string = date.toString();
    //     console.log(date_string)
    //     if(date.setHours(0,0,0,0) == currentDate.setHours(0,0,0,0)) {
    // // Date equals today's date
    //         console.log(date_string)
    //         console.log(message['content'])
    //     }   
    //     break
    // }   
}

function start(client) {
    console.log('Starting bot...');
    
    client.onMessage(async (msg) => {
        try {
            console.log(msg.body)
            const chats = await client.listChats();
            if (msg.body == 'ping') {
                // Send a new message to the same chat
                client.sendText(msg.from, 'pong');
            } else if (msg.body == 'rping') {
                // Send a new message as a reply to the current one
                client.sendText(msg.from, 'pong', {
                    quotedMsg: msg.id.toString(),
                });
            } else if (msg.body == '!chats') {
                const chats = await client.listChats({count: 50});
                keyss = chats.keys()
                let i = 1
                for (const key of keyss){
                    id = chats[key]['id']
                    const messages = await client.getMessages(id, {count: 100})
                    message_handler(messages, i)
                    i = i + 1
                
                }
                const fs = require('fs');
                const filePath = 'data/whatsapp/whatsapp_data.txt';
                console.log(output_message)
                fs.writeFile(filePath, output_message, 'utf8', (err) => {
                    if (err) {
                        console.error(err);
                        return;
                    }
                    console.log('File has been created and written successfully');
                    console.log('Please give a moment for the server to shutdown')
                });
                
            } else if (msg.body == '!info') {
                let info = await client.getHostDevice();
                let message = `_*Connection info*_\n\n`;
                message += `*User name:* ${info.pushname}\n`;
                message += `*Number:* ${info.wid.user}\n`;
                message += `*Battery:* ${info.battery}\n`;
                message += `*Plugged:* ${info.plugged}\n`;
                message += `*Device Manufacturer:* ${info.phone.device_manufacturer}\n`;
                message += `*WhatsApp version:* ${info.phone.wa_version}\n`;
                client.sendText(msg.from, message);
            }
        } catch (e) {
            console.log(e);
        }
    });
}

