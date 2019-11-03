var socket = io();

socket.on('connect', function() {
    socket.send({data: 'I\'m connected!'});
});

socket.on('my json', function(msg) {
    processResponse(msg)
});

function sendMessage() {
    console.log('Hello world!');
    socket.emit('my event',{query: document.getElementById("query").value});
}

function processResponse(response){
    tbody0=""
    tbody1=""
    for (i = 0; i < response.length; i++) {
        if (i < response.length/2) {
            tbody0 += getRowString(i+1, response[i], false);
            continue;
        }
        tbody0 += getRowString(i+1, response[i], true);
        tbody1 += getRowString(i+1, response[i], false);
    }
    console.log(document.getElementById("resultsBody0"));
    console.log(document.getElementById("resultsBody1"));
    document.getElementById("resultsBody0").innerHTML = tbody0;
    document.getElementById("resultsBody1").innerHTML = tbody1;
}

function getRowString(i,rowData, isMobileOnly) {
  classString=""
  if (isMobileOnly) {
    classString=' class="mobile-only"'
  }
  return "<tr"+classString+"><td>"+i+"</td><td>"+rowData['word']+'</td><td class="text-right">'+rowData['score'].toFixed(2)+'</td></tr>';
}
