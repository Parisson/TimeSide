import express from 'express'
import redis from 'redis'
import axios from 'axios'
import http from 'http'
import { v4 as uuidv4 } from 'uuid'
import resolve from 'path'
import { Server } from "socket.io";

const subscriber = redis.createClient(process.env.REDIS_URL);
// const publisher = redis.createClient("redis://broker:6379");
const app = express();
const server = http.createServer(app)


let origins = [process.env.ORIGIN]

// Websocket test page
if(process.env.DEBUG){
    origins.push('http://localhost:' + process.env.PORT)
    
    app.set("view engine", "ejs");
    app.set("views", resolve.resolve('./test'));
    app.get('/', (req, res) => {
        res.render('index.ejs', { port: process.env.PORT })
    })
}

const io = new Server(server, {
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
    
    let taskId = null
    if(typeof parts[1] !== "undefined") taskId = parts[1]

    let experienceId = null
    if(typeof parts[2] !== "undefined") experienceId = parts[2]

    let itemId = null
    if(typeof parts[3] !== "undefined") itemId = parts[3]

    let completion = null
    if(typeof parts[4] !== "undefined") completion = parseFloat(parts[4])

    switch(channel){
        case "timeside-task-start":
            for(let uuid in clients[clientName]){
                clients[clientName][uuid].emit(
                    "timeside-task-start",
                    {
                        taskId : taskId,
                    }
                )
            }
            break  
        case "timeside-experience-start":
            for(let uuid in clients[clientName]){
                clients[clientName][uuid].emit(
                    "timeside-experience-start",
                    {
                        taskId : taskId,
                        experienceId : experienceId,
                        itemId : itemId
                    }
                )
            }
            break 
        case "timeside-experience-progress":
            for(let uuid in clients[clientName]){
                clients[clientName][uuid].emit(
                    "timeside-experience-progress",
                    {
                        taskId : taskId,
                        experienceId : experienceId,
                        itemId : itemId,
                        completion : completion
                    }
                )
            }
            break
        case "timeside-experience-done":
            for(let uuid in clients[clientName]){
                clients[clientName][uuid].emit(
                    "timeside-experience-done",
                    {
                        taskId : taskId,
                        experienceId : experienceId,
                        itemId : itemId,
                    }
                )
            }
            break
        case "timeside-experience-fail":
            for(let uuid in clients[clientName]){
                clients[clientName][uuid].emit(
                    "timeside-experience-fail",
                    {
                        taskId : taskId,
                        experienceId : experienceId,
                        itemId : itemId,
                    }
                )
            }
            break    
    }
})

subscriber.subscribe("timeside-task-start");
subscriber.subscribe("timeside-experience-start");
subscriber.subscribe("timeside-experience-progress");
subscriber.subscribe("timeside-experience-done");
subscriber.subscribe("timeside-experience-fail");


server.listen(socketPort, () => {
    console.log("socket server started on port " + socketPort + "...");
})
