/**
 * Created by grigoryev on 13.02.15.
 */
var http = require('http'),
    sockjs = require('sockjs'),
    handler = require('./requestHandler');


function start(){
    var server = sockjs.createServer(),
        http_srv = http.createServer();

    server.installHandlers(http_srv, {prefix:'/data'});
    http_srv.listen(8080);

    server.on('connection', handler.handle);
}

exports.start = start;