var app = require('express')();
var bodyParser = require("body-parser");
var server = require('http').Server(app);
var _ = require('underscore')._;
var net = require('net');
var uuid = require('node-uuid');
var http = require('http');
var querystring = require('querystring');

app.use(bodyParser.urlencoded({ extended: false }));

var io = require('socket.io').listen( server )
server.listen(8000);

var people = {};
var things = {};
var cameras = {};
var sockets = [];

//var thing_sockets = [];

function getfecha(){
	var currentdate = new Date(); 
var datetime = "Last Sync: " + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
                return datetime;
}


app.post('/sensor_value/', function(req, res){
	var identifier = req.body.identifier;
	var key = req.body.key;
	var value = parseFloat(req.body.value);
	console.log(req.body.value);
    io.to(key).emit('sensor_values',identifier,value);
    res.end("yes");

});

app.post('/order_controller/', function(req, res){
	var identifier = req.body.identifier;
	var key_thing = req.body.key;
	var value_thing = parseFloat(req.body.value);

	_.find(things, function(key,value) {
		if (key.name === key_thing){
				if(key.socket.write("<"+identifier+":"+value_thing+">")){
				}
			}
	});





    io.to(key_thing).emit('controller_order',identifier,value_thing);
    res.end("yes");

});



io.sockets.on('connection', function (socket) {
	console.log("Algo se conecto")
    
    socket.on('joinserver',function(name,type,things_id){

		var inRoom = {};

		if(type === 'user'){
			console.log('User Join');
			people[socket.id] = {"name" : name, "inroom": things_id, "socket": socket ,"camera":""};
			sizePeople = _.size(people);
			for(var i in things_id){
				
				var match = false;
				_.find(things, function(key,value) {
					if (key.name === things_id[i])
						return match = true;
				});
				_.find(cameras, function(key,value) {
					
					if (key.name === things_id[i])
						return match = true;
				});


				if (match) {
					socket.emit('isconected',things_id[i],true,2);
				}
				else{
					socket.emit('isconected',things_id[i],false,2);
				}
				socket.join(things_id[i]);

			}

		}

		if (type === 'camera'){
			console.log('Cam Conected!!')
			cameras[name]={};
			cameras[name].name = name;
			cameras[name].socket = socket;
			cameras[name].people = [];
			socket.emit('people',cameras[name].people.length);
			io.to(name).emit('isconected',name,true,1);
		}



		/*if(type === 'thing'){
			console.log('is a thing');
			things[socket.id] = {"name": name};
			socket.join(name);
			io.to(name).emit('isconected',things[socket.id].name,true);
		}*/

		sockets.push(socket);
		
    });

    socket.on('joinCamera',function(key){

    	people[socket.id].camera = key;
    	cameras[key].people.push(socket.id);
    	cameras[key].socket.emit('people',cameras[key].people.length);
    });

    socket.on('liveStream',function(key, data){
    	if(data !== undefined){
    	dataencode = data.toString('base64');
    	console.log("Imagen Recibida")
    	io.to(key).emit('Streaming',dataencode);

    	}
    });


    socket.on('really_disconected',function(thing_id){
		var match = false;
		_.find(things, function(key,value) {
			if (key.name === thing_id)
				return match = true;
		});
		if(match){
			socket.emit('isconected',thing_id,true,2);
		}
		else{
			socket.emit('isconected',thing_id,false,2);
		}

    });




    socket.on('disconnect', function() {

 			_.find(cameras, function(key,value) {

					if (key.socket.id === socket.id){
						io.to(key.name).emit('isconected',key.name,false,1);
						delete cameras[key.name];
					}


				});

 			for(key in people){
 				if(key === socket.id){
 					if (people[socket.id].camera !== ""){
 						console.log(people[socket.id].camera);

 						for(a in cameras[people[socket.id].camera].people){
 							if (cameras[people[socket.id].camera].people[a] === socket.id){
 								cameras[people[socket.id].camera].people.splice(a,1);
 							}
 						}
 						cameras[people[socket.id].camera].socket.emit('people',cameras[people[socket.id].camera].people.length);
 					}
    				delete people[socket.id];
 				}
 			}   	
   });

});


//Manage TCP Connection Things
//
//

var PORT = 3005;

var tcpServer = net.createServer(function (socket) {

});

tcpServer.on('connection',function(socket){
	
	//console.log('num of connections on port 3005: ' + tcpServer.connections);

	socket.on('data',function(data){
		if(typeof socket.id === "undefined"){
			var recibido = data.toString();
			console.log(recibido);
			if(recibido.indexOf('key:') != -1)
			{
				
				var buffer = new Array(32);
				uuid.v4(null, buffer, 0);
				uuid.v4(null, buffer, 16);

				var id_socket = uuid.unparse(buffer);
				socket.id = id_socket;

				var key = recibido.split(":")[1];

				//thing_sockets.push(socket);
				//thing_sockets[thing_sockets.length-1].id = socket.id;
				things[socket.id] = {"name": key,"socket":socket, "heartbeat":0};
				things[socket.id].socket.setTimeout(5000);
				io.to(key).emit('isconected',key,true,2);
				console.log("Socket "+things[socket.id].name+" conectado         "+getfecha());
			}

		}
		else{
			var recibido = data.toString();
			if(recibido.indexOf('heartbeat') != -1){

				things[socket.id].heartbeat = 1;
				console.log("Anadiendo latido "+things[socket.id].name+" heartbeat: "+things[socket.id].heartbeat);

			}
			else if(recibido.indexOf('valor') != -1){
				var res = recibido.split("@");
				console.log('Recibido Valor de' + res[1] + " del identificador " + res[2] + " con el valor " +res[3])
				identifier = res[2];
				key = res[1];
				value = parseInt(Math.round(parseFloat(res[3])));
   				io.to(key).emit('sensor_values',identifier,value);

   				var data = querystring.stringify({
      				key: key,
      				identifier: identifier,
      				value: res[3]
    			});
    			var options = {
    				host: 'localhost',
   	 				port: 8080,
    				path: '/sensor_value/',
    				method: 'POST',
    				headers: {
        				'Content-Type': 'application/x-www-form-urlencoded',
        				'Content-Length': Buffer.byteLength(data)
    				}
				};
				var req = http.request(options, function(res) {
    				res.setEncoding('utf8');
    				res.on('data', function (chunk) {
        				console.log("body: " + chunk);
    				});
				});

				req.write(data);
				req.end();

			}
		}
//send data to guest socket.io chat server
	});

	socket.on('close',function(){
		for(key in things){
			if(key === socket.id){
				//console.log("Socket "+things[key].name+" desconectado      "+getfecha());
				io.to(things[socket.id].name).emit('isconected',things[socket.id].name,false,1);
				delete things[socket.id];
			}
 		} 
 		//socket.destroy();
	});
	socket.on('error',function(err){
		console.error("error", err);
	});



	socket.on('timeout',function(){
		console.log("TimeOut");
		things[socket.id].heartbeat = 0;
		console.log('Esperando para desconexion');
		setTimeout( function(i){
			if (typeof things[socket.id] != 'undefined') {
			if(things[socket.id].heartbeat > 0){
				console.log("Desconexion Abortada");
			}

			else{
				for(key in things){
				if(key === socket.id){
					console.log("Socket "+things[key].name+" desconectado      "+getfecha());
					io.to(things[socket.id].name).emit('isconected',things[socket.id].name,false,1);
					delete things[socket.id];
				}
	 		} 
				socket.destroy();
			}
		}
            
        }, 5000 );


	});
	
});

tcpServer.listen(PORT);

console.log('Server TCP Thing listening on localhost:'+ PORT);