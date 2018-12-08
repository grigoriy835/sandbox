var connect;

$(document).ready(function(){
    connect = new Connect();

    connect.login.keypress(function(e){
        if(e.keyCode==13){
            var data = {
                id: connect.id,
                name: this.value
            };
            connect.handle('setName',data)
        }
    });

    connect.message.keypress(function(e){
        if(e.keyCode==13){
            var data = {
                id: connect.id,
                message: this.value
            };
            this.value = '';
            connect.handle('message',data)
        }
    });

    setTimeout(function(){
        connect.handle('init',null);
    }, 2000)
});

function Connect(){
    var self = this,
        data;

    this.id = 0;
    this.sock = new SockJS('http://chat.local:8080/data');
    this.sock.onmessage = function(e){
        data = JSON.parse(e.data);
        self.handle(data.event, data.data);
    };

    this.handle = function(event, data){
        if(typeof(this.handlers[event]) === 'function'){
            this.handlers[event](data);
        }
    };

    this.users = $('#users');
    this.history = $('#history');
    this.message = $('#message');
    this.login = $('#login');

    this.handlers = [];
    this.handlers['init'] = function(data){
        self.sock.send(JSON.stringify({command: 'init', data: null}));
    };

    this.handlers['getId'] = function(id){
        self.id = id;
    };

    this.handlers['setName'] = function(data){
        self.sock.send(JSON.stringify({command: 'setName', data: data}));
    };

    this.handlers['alertNewName'] = function(data){
        $('#'+data.id).html(data.name);
    };

    this.handlers['listUsers'] = function(users){
        for(var user in users){
            self.users.html(self.users.html()+'<div class="participant" id="'+users[user].id+'">'+users[user].name+'</div>');
        }
    };

    this.handlers['message'] = function(data){
        self.sock.send(JSON.stringify({command: 'newMessage', data: data}));
    };

    this.handlers['newParticipant'] = function(data){
        self.users.html(self.users.html()+'<div class="participant" id="'+data.id+'">'+data.name+'</div>');
    };

    this.handlers['alertNewMessage'] = function(data){
        self.history.html(self.history.html()+'<div class="message" id="message-'+data.id+'">'+data.message+'</div>');
    };

    this.handlers['participantLeave'] = function(data){
        $('#'+data.id).remove();
    };
}