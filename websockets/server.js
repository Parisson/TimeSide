const express = require('express')
const redis = require('redis');
const axios = require('axios')
const subscriber = redis.createClient(process.env.REDIS_URL);
const publisher = redis.createClient("redis://broker:6379");
const app = express();
const http = require('http').createServer(app)
const { v4: uuidv4 } = require('uuid');


let origins = [process.env.ORIGIN]

// Websocket test page
if(process.env.DEBUG){
    origins.push('http://localhost:' + process.env.PORT)
    const resolve = require('path').resolve
    app.set("view engine", "ejs");
    app.set("views", resolve('./test'));
    app.get('/', (req, res) => {
        res.render('index.ejs', { port: process.env.PORT })
    })
}

const io = require('socket.io')(http, {
    cors: {
        origin: origins,
        methods: ["GET", "POST"]
    }
})
const socketPort = process.env.PORT

// Auth middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token
  axios.get(
      process.env.DJANGO_API_URL + 'users/me',
      {
          headers : {
              Authorization: 'Token ' + token 
          }
      }
  )
  .then((datas) => {
      socket.details = {
          'username': datas.data.username,
          'firstName': datas.data.first_name,
          'lastName' : datas.data.last_name
      }
      next()
  })
  .catch((error)=>{
      next(new Error(error + "\n\ntoken '" + token + "' is not valid"))
  })
});


const clients = []

io.on("connection", (client) => {
    
    if(typeof clients[client.details.username] == 'undefined') clients[client.details.username] = {}
    
    const uuid = uuidv4()
    clients[client.details.username][uuid] = client
    
    client.on("disconnect", () => {
        delete clients[client.details.username][uuid]
        if(clients[client.details.username].length == 0) delete clients[client.details.username]
    })
})

subscriber.on("message", (channel, message) => {
    const parts = message.split(":")
    const clientName = parts[0]
    const taskId = parts[1]
    if(channel == "timeside-progress"){
        for(let uuid in [clientName]){
            clients[clientName][uuid].emit(
                "timeside-progress",
                {
                    taskId : taskId,
                    completion : parseFloat(parts[2])
                }
            )
        }
    }else if(channel == "timeside-done"){
        for(let uuid in clients[clientName]){
            clients[clientName][uuid].emit(
                "timeside-done",
                {
                    taskId : taskId,
                }
            )
        }
    }else if(channel == "timeside-fail"){
        for(let uuid in [clientName]){
            clients[clientName][uuid].emit(
                "timeside-fail",
                {
                    taskId : taskId,
                }
            )
        }
        
    }else if(channel == "timeside-delete"){
        for(let uuid in [clientName]){
            clients[clientName][uuid].emit(
                "timeside-delete",
                {
                    taskId : taskId,
                }
            )
        }
    }
})

subscriber.subscribe("timeside-progress");
subscriber.subscribe("timeside-done");
subscriber.subscribe("timeside-fail");
subscriber.subscribe("timeside-delete");


http.listen(socketPort, () => {
    console.log("socket server started on port " + socketPort + "...");
})
