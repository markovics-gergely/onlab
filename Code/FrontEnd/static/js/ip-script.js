var cams = JSON.parse(localStorage.getItem('cameras'));

const CameraStatus = {
    Paused: 0,
    Started: 1
}
Object.freeze(CameraStatus)
function Camera(name, ip, status) {
    this.name = name;
    this.ip = ip;
    this.status = status;
}
var cameras = [];

var managerpanel = document.getElementById("managerpanel");
var caminfo = document.getElementById("caminfo");

parseCameras();

$(document).on("click", ".ipPauseOrStart", function(e) {
    e.stopPropagation();

    var id = $(".ipPauseOrStart").index($(this));
    if(cameras[id].status == CameraStatus.Paused){
        cameras[id].status = CameraStatus.Started;
    }
    else if(cameras[id].status == CameraStatus.Started){
        cameras[id].status = CameraStatus.Paused;
    }

    renderCameras();
})

$(document).on("click", ".ipDelete", function(e) {
    e.stopPropagation();

    var id = $(".ipDelete").index($(this));
    cameras.splice(id, 1)

    renderCameras();
})

$(document).on("click", ".camera-list-item", function() {
    $(".camera-list-item").css('background-color', 'white');

    var id = $(".camera-list-item").index($(this));
    var camera = cameras[id];

    $(this).css('background-color', '#f0f0f0');

    var ipFrame = document.createElement('div');
    ipFrame.className = "camera-info-item";

    var ip = document.createElement('h4');
    ip.textContent = camera.ip;
    ip.className = "ip-addr ml-3";

    ipFrame.appendChild(ip);

    caminfo.innerHTML = "";
    caminfo.appendChild(ipFrame);
})

function renderCameras() {
    managerpanel.innerHTML = "";
    cameras.forEach(function(camera, id){
        var ip = document.createElement('h4');
        ip.textContent = camera.name;
        ip.className = "ip-addr ml-3";

        var startA = document.createElement('a');
        if(camera.status == CameraStatus.Paused) startA.setAttribute("href", "../p:" + id);
        if(camera.status == CameraStatus.Started) startA.setAttribute("href", "../s:" + id);

        var startImage = document.createElement('img');
        startImage.type = "image";
        if(camera.status == CameraStatus.Paused) startImage.src = "../image/pause.png";
        if(camera.status == CameraStatus.Started) startImage.src = "../image/start.png";
        startImage.className = "ipPauseOrStart";

        var deleteA = document.createElement('a');
        deleteA.setAttribute("href", "../d:" + id);

        var deleteImage = document.createElement('img');
        deleteImage.type = "image";
        deleteImage.src = "../image/delete.png";
        deleteImage.className = "ipDelete";

        var outerdiv = document.createElement('div');
        outerdiv.className = "camera-list-item";

        var innerdiv = document.createElement('div');
        innerdiv.className = "icons ml-auto mr-3"

        deleteA.appendChild(deleteImage);
        startA.appendChild(startImage)
        innerdiv.appendChild(startA);
        innerdiv.appendChild(deleteA);
        outerdiv.appendChild(ip);
        outerdiv.appendChild(innerdiv);

        managerpanel.appendChild(outerdiv);
    })
}

function parseCameras() {
    //TODO kamerák szerverről

    /*for()
        cameras.push(new Camera())*/
    //példa adat
    cameras.push(new Camera("Kamera1", "192.168.0.176:8080", CameraStatus.Paused))
    cameras.push(new Camera("Kamera2", "192.168.1.176:8080", CameraStatus.Started))
    cameras.push(new Camera("Kamera3", "192.168.2.176:8080", CameraStatus.Paused))

    renderCameras();
}

function checkname(input){
    var unique = true;
    cameras.forEach(function(c){
        if(c.name == input.value){
            unique = false;
        }
    })
    if(unique) input.setCustomValidity('');
    else input.setCustomValidity('Camera Name must be unique');
}

function checkip(input){
    var ipregex = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]{1,5}$/;
    var unique = true;
    cameras.forEach(function(c){
        if(c.ip == input.value){
            unique = false;
        }
    })
    if(!unique) input.setCustomValidity('IP address must be unique');
    else if(!input.value.match(ipregex)) input.setCustomValidity('IP address must be valid');
    else input.setCustomValidity('');
}

$(".addForm").on('submit',function(e){
    e.preventDefault();
    var name = $('#addname').val();
    var ip = $('#addipaddr').val();
    var selector = document.getElementById("StatusSelect");

    cameras.push(new Camera(name, ip, selector.selectedIndex));

    renderCameras();
    $("#addIPModal").modal('toggle');
});

function saveCamerasToLocal(){
    localStorage.setItem('cameras', JSON.stringify(cameras));
}

$('.pred-link').on('click', function(){
    saveCamerasToLocal();
})
