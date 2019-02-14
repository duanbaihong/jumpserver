var rowHeight=1,colWidth=1;function WSSHClient(){}WSSHClient.prototype._generateEndpoint=function(a){console.log(a);return("https:"==window.location.protocol?"wss://":"ws://")+document.URL.match(/\/\/(.*?)\//)[1]+"/ws/applications"+document.URL.match(/(\?.*)/)};
WSSHClient.prototype.connect=function(a){var c=this._generateEndpoint(a);if(window.WebSocket)this._connection=new WebSocket(c);else if(window.MozWebSocket)this._connection=MozWebSocket(c);else{a.onError("WebSocket Not Supported");return}this._connection.onopen=function(){a.onConnect()};this._connection.onmessage=function(b){try{a.onData(b.data)}catch(e){b=JSON.parse(b.data.toString()),a.onError(b.error)}};this._connection.onclose=function(b){a.onClose()}};WSSHClient.prototype.send=function(a){this._connection.send(JSON.stringify({data:a}))};
function openTerminal(a){var c=new WSSHClient;try{var b=localStorage.getItem("term-row");var e=localStorage.getItem("term-col")}catch(f){b=35,e=100}b||(b=35);e||(e=100);var d=new Terminal({rows:b,cols:e,useStyle:!0,screenKeys:!0});d.open();d.on("data",function(a){c.send(a)});$(".applications").detach().appendTo("#term");d.write("Connecting...");c.connect($.extend(a,{onError:function(a){d.write("Error: "+a+"\r\n")},onConnect:function(){c.send({resize:{rows:b,cols:e}});d.write("\r")},onClose:function(){d.write("Connection Reset By Peer")},
onData:function(a){d.write(a)}}));return{term:d,client:c}}
$(document).ready(function(){$("#ssh").show();var a=openTerminal({});console.log(rowHeight);try{$("#term-row")[0].value=localStorage.getItem("term-row"),$("#term-col")[0].value=localStorage.getItem("term-col")}catch(c){$("#term-row")[0].value=35,$("#term-col")[0].value=100}$("#col-row").click(function(){var c=$("#term-col").val(),b=$("#term-row").val();localStorage.setItem("term-col",c);localStorage.setItem("term-row",b);a.term.resize(c,b);a.client.send({resize:{rows:b,cols:c}});$("#ssh").show()});
$(".applications").mouseleave(function(){$(".termChangBar").slideDown()});$(".applications").mouseenter(function(){$(".termChangBar").slideUp()})});