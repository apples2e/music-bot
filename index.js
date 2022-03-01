const { Client , Intents , Collection}  = require('discord.js')
const client = new Client({intents:32767})
const fs = require('fs')
const {prefix , token} = require('./config.json')
const {DiscordTogether} = require('discord-together')
client.discordTogether = new DiscordTogether(client);
module.exports = client;
const mongoose = require("mongoose")

mongoose.connect("mongodb+srv://applesee:1234@cluster0.if7ro.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", {
useNewUrlParser: true ,  useUnifiedTopology: true 
}).then(console.log("데이터베이스 연결 완료"))

client.once('ready',()=>{
    console.log("봇이 준비됨")
})
client.commands = new Collection()

const commandsFile = fs.readdirSync('./commands').filter(file => file.endsWith('.js'))

for(const file of commandsFile){
    const command = require(`./commands/${file}`)
    client.commands.set(command.name , command)
}

client.on('messageCreate' , message=>{
    if(!message.content.startsWith(prefix)) return
    const args = message.content.slice(prefix.length).trim().split(/ +/)
    const commandName = args.shift()
    const command = client.commands.get(commandName)
    if (!command) return
    try{
        command.execute(message,args)
    } catch (error) {
        console.error(error)
    }
})

client.on('messageCreate',message=>{
    if(message.content == `${prefix}유튜브`){
        const channel = message.member.voice.channel
        if(!channel) return message.reply("음성채널에 접속해주세요!")
        client.discordTogether.createTogetherCode(channel.id, 'youtube').then(invite =>{
            return message.channel.send(invite.code)
        })
    }
})

client.login("OTQ3MDg0NjczMzEyNTIyMjUx.YhoHVg.qjXfBHPy5NYcXl79ts9IePnaKlk")
