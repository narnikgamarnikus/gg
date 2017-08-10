var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
socket = new WebSocket(ws_scheme + "://" + window.location.host + "/services/");

//var element = document.getElementById('phone-numbers');

socket.onmessage = function(e) {
	data = jQuery.parseJSON(e.data)
    jobs = jQuery.parseJSON(data.jobs)
    for (job in jobs) {
        j = jobs[job]
        console.log(j)
        console.log(j.fields)
    }
    //proposals = jQuery.parseJSON(data.proposals)
    //console.log(proposals)
    //    for (proposal in proposals) {
    //    p = proposals[proposal]
    //    console.log(p)
    //    console.log(p.object.fields)
    //}
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


/*
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
proposal_socket = new WebSocket(ws_scheme + "://" + window.location.host + "/proposal/");

//var element = document.getElementById('phone-numbers');

proposal_socket.onmessage = function(e) {
	console.log(jQuery.parseJSON(e.data))
    //var a = document.createElement('a');
    //var phone = document.createTextNode(e.data);
    //a.href = 'tel:' + e.data;
    //a.appendChild(phone);
    //element.appendChild(a); 
}

if (proposal_socket.readyState == WebSocket.OPEN) proposal_socket.onopen();

*/
