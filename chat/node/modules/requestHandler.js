var eventsHandlers = require('./eventsHandler'),
    conections = {};

function handle(conn){
    conn.on('data', function(data){
        data = JSON.parse(data);

        eventsHandlers.handle(data.command, data.data);
    });

    conn.on('close', function(){
        eventsHandlers.handle('quit', null);
    })
}

exports.handle = handle;