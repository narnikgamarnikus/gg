var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
socket = new WebSocket(ws_scheme + "://" + window.location.host + "/bet/");

//var element = document.getElementById('phone-numbers');

socket.onmessage = function(e) {
	console.log(jQuery.parseJSON(e.data))
    //var a = document.createElement('a');
    //var phone = document.createTextNode(e.data);
    //a.href = 'tel:' + e.data;
    //a.appendChild(phone);
    //element.appendChild(a); 
}

socket.onopen = function() {
    socket.send("connect");
}

socket.onclose = function() {
    socket.send("disconnect");   
}

if (socket.readyState == WebSocket.OPEN) socket.onopen();



