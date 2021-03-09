function Camera(name, ip) {
    this.name = name;
    this.ip = ip;
}
var cameras = [];

var managerpanel = document.getElementById("managerpanel");
var caminfo = document.getElementById("caminfo");

parseCameras();

$(document).on("click", ".ipPauseOrStart", function() {
    var start = "assets/start.png";
    var pause = "assets/pause.png";
    $(this).attr("src", $(this).attr("src").match(start) ? pause : start);
})

$(document).on("click", ".ipDelete", function() {
    var id = $(".ipDelete").index($(this));
    cameras.splice(id, 1)

    renderCameras();
})

$(document).on("click", ".camera-list-item", function() {
    $(".camera-list-item").css('background-color', 'white');

    var id = $(".camera-list-item").index($(this));
    var camera = cameras[id];

    $(this).css('background-color', '#f0f0f0');
    var ip = document.createElement('h4');
    ip.textContent = camera.ip;
    ip.className = "ip-addr ml-3";

    caminfo.innerHTML = "";
    caminfo.appendChild(ip);
})

var addbutton = document.getElementById("addIP");
var uniqueIpID = 0;
addbutton.onclick = function() {
    var newCamera = new Camera("asd", "192.168.0." + uniqueIpID.toString());
    uniqueIpID++;
    cameras.push(newCamera);

    renderCameras();
}

function renderCameras() {
    managerpanel.innerHTML = "";
    cameras.forEach(function(camera, id){
        var ip = document.createElement('h4');
        ip.textContent = camera.name;
        ip.className = "ip-addr ml-3";

        var startImage = document.createElement('input');
        startImage.type = "image";
        startImage.src = "assets/start.png";
        startImage.className = "ipPauseOrStart";

        var deleteImage = document.createElement('input');
        deleteImage.type = "image";
        deleteImage.src = "assets/delete.png";
        deleteImage.className = "ipDelete";

        var outerdiv = document.createElement('div');
        outerdiv.className = "camera-list-item";

        var innerdiv = document.createElement('div');
        innerdiv.className = "icons ml-auto mr-3"

        innerdiv.appendChild(startImage);
        innerdiv.appendChild(deleteImage);
        outerdiv.appendChild(ip);
        outerdiv.appendChild(innerdiv);

        managerpanel.appendChild(outerdiv);
    })
}

function parseCameras() {
    //TODO kamerák listája fájlból cameras tömbbe
    cameras.push(new Camera("First", "192.168.0.0"))
    cameras.push(new Camera("Second", "192.168.0.1"))
    cameras.push(new Camera("Third", "192.168.0.2"))
    cameras.push(new Camera("Fourth", "192.168.0.4"))

    renderCameras();
}