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

    //TODO indítás/leállítás szerverről

    var id = $(".ipPauseOrStart").index($(this));
    if(cameras[id].status == CameraStatus.Paused) cameras[id].status = CameraStatus.Started;
    else if(cameras[id].status == CameraStatus.Started) cameras[id].status = CameraStatus.Paused; 

    renderCameras();
})

$(document).on("click", ".ipDelete", function(e) {
    e.stopPropagation();

    //TODO törlés szerverről

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

        var startImage = document.createElement('input');
        startImage.type = "image";
        if(camera.status == CameraStatus.Paused) /*startImage.src = "../FrontEnd/assets/pause.png"; */
            startImage.setAttribute("src", "../FrontEnd/assets/pause.png");
        if(camera.status == CameraStatus.Started) startImage.src = "../FrontEnd/assets/start.png";
        startImage.className = "ipPauseOrStart";

        var deleteImage = document.createElement('input');
        deleteImage.type = "image";
        deleteImage.src = "../FrontEnd/assets/delete.png";
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
    //TODO kamerák szerverről

    //példa adat
    cameras.push(new Camera("Kamera", "192.168.0.176:8080", CameraStatus.Paused))

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
