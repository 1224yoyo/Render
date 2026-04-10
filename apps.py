const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);

let players = {}; // 伺服器存一份地圖

app.use(express.static(__dirname + '/public')); // 你的 HTML/JS 放這裡

io.on('connection', (socket) => {
    console.log('有人進來了:', socket.id);

    // 初始化新玩家
    players[socket.id] = { x: 500, y: 500, id: socket.id };
    
    // 告訴新人目前的玩家狀況
    socket.emit('currentPlayers', players);
    // 告訴舊人有新人來了
    socket.broadcast.emit('newPlayer', players[socket.id]);

    // 收到移動訊息
    socket.on('playerMovement', (movementData) => {
        if (players[socket.id]) {
            players[socket.id].x = movementData.x;
            players[socket.id].y = movementData.y;
            // 廣播給其他人
            socket.broadcast.emit('playerMoved', players[socket.id]);
        }
    });

    socket.on('disconnect', () => {
        delete players[socket.id];
        io.emit('playerDisconnected', socket.id);
    });
});

http.listen(3000, () => { console.log('伺服器在 3000 埠跑起來囉！'); });
