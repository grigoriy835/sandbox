var Handlers = function(clientConn){
    var self = this;
    this.clientConn = clientConn;
    this.connId = 0;
    this.connName = '';

    this.handle = function(command,data){
        if(typeof(this.handlers[command]) === 'function'){
            this.handlers[command](data);
        }else{
            this.handlers['default'](data);
        }
    };

    this.handlers = [];
    this.handlers['default'] = function(data){
    };
    this.handlers['init'] = function(data){
        self.handle('giveId', null);
        self.connName = 'хач-' + self.connId;
        var connData = {
            id: self.connId,
            name: self.connName
        };
        var users = [];

        for (var id in connections){
            users.push({
                id:id,
                name:connections[id].connName
            });
            if(id != self.connId)
                connections[id].handle('newParticipant', connData)
        }

        data = {
            event: 'listUsers',
            data: users
        };
        self.clientConn.write(JSON.stringify(data))
    };

    this.handlers['giveId'] = function(data){
        data = {
            event: 'getId',
            data: self.connId
        };
        self.clientConn.write(JSON.stringify(data))
    };

    this.handlers['newParticipant'] = function(data){
        data = {
            event: 'newParticipant',
            data: data
        };
        self.clientConn.write(JSON.stringify(data))
    };

    this.handlers['setName'] = function(data){
        connections[data.id].connName = data.name;
        for (var id in connections){
            connections[id].handle('alertNewName', data)
        }
    };

    this.handlers['alertNewName'] = function(data){
        data = {
            event: 'alertNewName',
            data: data
        };
        self.clientConn.write(JSON.stringify(data))
    };

    this.handlers['newMessage'] = function(data){
        for (var id in connections){
            connections[id].handle('alertNewMessage', data)
        }
    };

    this.handlers['alertNewMessage'] = function(data){
        data = {
            event: 'alertNewMessage',
            data: data
        };
        self.clientConn.write(JSON.stringify(data))
    };

    this.handlers['quit'] = function(){
        var data = {
            id: self.connId
        };
        for (var id in connections){
            connections[id].handle('alertParticipantLeave', data)
        }
    };

    this.handlers['alertParticipantLeave'] = function(data){
        data = {
            event: 'participantLeave',
            data: data
        };
        self.clientConn.write(JSON.stringify(data))
    };
};

getNewId = function(){
    var newId = 0;
    for(var id in connections){
        newId = newId>id ? newId : id;
    }
    return ++newId;
};