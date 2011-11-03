var http = require('http');
var amqp = require('amqp');
var sockjs = require('sockjs');
var node_static = require('node-static');

var config = require('./config');


var client_id = '' + Math.random();

var conn;
var amqpSetup = function() {
    var queue = conn.queue('mud-' + client_id, {durable: false, exclusive: true},
                           function() {
                               queue.subscribe(
                                   function(msg) {
                                       got_msg(msg);
                                   });
                           });
};

conn = amqp.createConnection({url: config.amqp_url});
conn.on('ready', amqpSetup);


var sockjs_opts = {
    sockjs_url: "http://cdn.sockjs.org/sockjs-0.1.min.js",
    disabled_transports: ['websocket']
};


var register = {};
function got_msg(raw_msg) {
    var d = JSON.parse(raw_msg.data.toString('utf-8'));
    var id = d.id, msg=d.data;
    if(id in register) {
        register[id](msg);
    }
};

var sjs = new sockjs.Server(sockjs_opts);
sjs.on('open', function(s) {
           var id = '' + Math.random();
           register[id] = function(msg) {
               s.send(msg);
           };
           console.log(id + " created");
           s.on('message', function(e) {
                    conn.publish('mud', {data: e.data,
                                         'reply-to': 'mud-' + client_id,
                                         id: id});
                });
           s.on('close', function() {
                    conn.publish('mud', {data: '',
                                         closed: true,
                                         'reply-to': 'mud-' + client_id,
                                         id: id});
                    console.log(id + " deleted");
                    delete register[id];
                });
       });


var static_directory = new node_static.Server(__dirname + '/static');

var server = http.createServer();
server.addListener('request', function(req, res) {
                       try {
                           static_directory.serve(req, res);
                       } catch (x) {}
                   });
server.addListener('upgrade', function(req,res){
                       res.end();
                   });

sjs.installHandlers(server, {prefix:'[/]mud'});

console.log(' [*] Listening on 0.0.0.0:' + config.port);
server.listen(config.port, '0.0.0.0');
