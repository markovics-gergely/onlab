function Camera(ip) {
    this.ip = ip;
}
var cameras = [];
parseCameras();

var managerpanel = document.getElementById("managerpanel");
var caminfo = document.getElementById("caminfo");

$(document).on("click", ".ipPauseOrStart", function() {
    var start = "assets/start.png";
    var pause = "assets/pause.png";
    $(this).attr("src", $(this).attr("src").match(start) ? pause : start);
})

$(document).on("click", ".camera-list-item", function() {
    $(".camera-list-item").css('background-color', 'white');
    var num = $("h4.ip-addr", this).text().slice(-1);

    $(this).css('background-color', '#f0f0f0');
    var ip = document.createElement('h4');
    ip.textContent = "192.168.0." + num; 
    ip.className = "ip-addr ml-3";
    caminfo.innerHTML = "";
    caminfo.appendChild(ip);
})

var addbutton = document.getElementById("addIP");
var uniqueIpID = 0;
addbutton.onclick = function() {
    var ip = document.createElement('h4');
    ip.textContent = "192.168.0." + uniqueIpID.toString(); 
    ip.className = "ip-addr ml-3";

    var startImage = document.createElement('input');
    startImage.type = "image";
    startImage.src = "assets/start.png";
    startImage.id = "ipPauseOrStart" + uniqueIpID.toString();
    startImage.className = "ipPauseOrStart";

    var deleteImage = document.createElement('input');
    deleteImage.type = "image";
    deleteImage.src = "assets/delete.png";

    var outerdiv = document.createElement('div');
    outerdiv.className = "camera-list-item";
    outerdiv.id = "ipElement" + uniqueIpID.toString();

    var innerdiv = document.createElement('div');
    innerdiv.className = "icons ml-auto mr-3"

    innerdiv.appendChild(startImage);
    innerdiv.appendChild(deleteImage);
    outerdiv.appendChild(ip);
    outerdiv.appendChild(innerdiv);

    managerpanel.appendChild(outerdiv);

    uniqueIpID += 1;

    cameras.push(new Camera(ip.textContent));
}

function parseCameras() {
    //TODO kamerák listája fájlból cameras tömbbe
}