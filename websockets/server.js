const express = require('express')
const redis = require('redis');
const axios = require('axios')
const subscriber = redis.createClient(process.env.REDIS_URL);
// const publisher = redis.createClient("redis://broker:6379");
const app = express();
const http = require('http').createServer(app)


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
      process.env.DJANGO_API_URL + '/users/me',
      {
          headers : {
              Authorization: 'Token ' + token 
          }
      }
  )
  .then((response)=>{
      console.log("hey")
      console.log(response)
  })
  .catch((error)=>{
      console.log("hay")
      next(new Error(error + "\n\ntoken '" + token + "' is not valid"));
  })
  /*if (isValid(socket.request)) {
    next();
  } else {
    
  }*/
});


const events = []

function addSubscriber(event, id, client){
    const eventName = event + "-" + id
    if(typeof events[eventName] == "undefined") events[eventName] = []
    events[eventName].push(client)
}

function getAllIndexes(arr, val) {
    const indexes = []
    let i = -1;
    while ((i = arr.indexOf(val, i+1)) != -1){
        indexes.push(i);
    }
    return indexes;
}

io.on("connection", (client) => {
    client.on("subscribe", (data) => {
        addSubscriber(data.event, data.id, client)
    })
    client.on("disconnect", () => {
        for(let e in events){
            const indexes = getAllIndexes(events[e], client)
            for(let i in indexes){
                events[e].splice(indexes[i], 1)
            }
            if(Object.keys(events[e]).length == 0) delete events[e]
        }
    })
})

subscriber.on("message", (channel, message) => {
    let eventName = ""
    if(channel == "timeside-progress-signal"){
        const parts = message.split(":")
        eventName = "timeside-progress-signal" + "-" + parts[0]
        for(let client in events[eventName]){
            events[eventName][client].emit("timeside-progress-signal", {
                id : parts[0],
                completion : parseFloat(parts[1])
            })
        }
    }else if(channel == "timeside-done-signal"){
        eventName = "timeside-done-signal" + "-" + message
        for(let client in events[eventName]){
            events[eventName][client].emit("timeside-done-signal", {
                id : message
            })
        }
    }else if(channel == "timeside-fail-signal"){
        eventName = "timeside-fail-signal" + "-" + message
        for(let client in events[eventName]){
            events[eventName][client].emit("timeside-fail-signal", {
                id : message
            })
        }
    }else if(channel == "timeside-delete-signal"){
        eventName = "timeside-delete-signal" + "-" + message
        for(let client in events[eventName]){
            events[eventName][client].emit("timeside-delete-signal", {
                id : message
            })
        }
    }
})

subscriber.subscribe("timeside-progress-signal");
subscriber.subscribe("timeside-done-signal");
subscriber.subscribe("timeside-fail-signal");
subscriber.subscribe("timeside-delete-signal");

http.listen(socketPort, () => {
    console.log("socket server started on port " + socketPort + "...");
})


