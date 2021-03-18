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
    if(cameras[id].status == CameraStatus.Paused) cameras[id].status = CameraStatus.Started;
    else if(cameras[id].status == CameraStatus.Started) cameras[id].status = CameraStatus.Paused; 

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

        var startImage = document.createElement('input');
        startImage.type = "image";
        if(camera.status == CameraStatus.Paused) startImage.src = "/static/assets/pause.png"; /*startImage.setAttribute("src", "/static/assets/pause.png");*/
        if(camera.status == CameraStatus.Started) startImage.src = "/static/assets/start.png"; /*startImage.setAttribute("src", "/static/assets/start.png");*/
        startImage.className = "ipPauseOrStart";

        var deleteImage = document.createElement('input');
        deleteImage.type = "image";
        deleteImage.src = "/static/assets/delete.png";
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
    cameras.push(new Camera("First", "192.168.0.0", CameraStatus.Started))
    cameras.push(new Camera("Second", "192.168.0.1", CameraStatus.Paused))
    cameras.push(new Camera("Third", "192.168.0.2", CameraStatus.Paused))
    cameras.push(new Camera("Fourth", "192.168.0.4", CameraStatus.Started))

    renderCameras();
}

$.validator.addMethod('ValidateIPaddress', function (value) {
        if(value == "") return false;
        var ipregex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        cameras.forEach(function(c){
            if(c.ip == value){
                return false;
            }
        })
        if (value.match(ipregex)){
            $("#addipaddr").removeClass('is-invalid')
            return true;
        }
        return false;
    },
    function(value){
    }
)
$.validator.addMethod('ValidateName', function (value) {
        if(value == "") return false;
        cameras.forEach(function(c){
            if(c.name == value){
                return false;
            }
        })
        $("#addname").removeClass('is-invalid')
        return true;
    },
    function(value){
    }
)

$("#addForm").validate({
    rules: {
        addname: {
            ValidateName:true
        },
        addipaddr : {
            ValidateIPaddress:true
        }
    },
    errors: {
        addname: $("#addname").addClass('is-invalid'),
        addipaddr : $("#addipaddr").addClass('is-invalid')
    }
})
$(function(){
    $('#addForm').on('submit', function (e) {
        e.preventDefault();

        console.log(e);
        var name = $("#addname").val();
        var ip = $("#addipaddr").val();
    
        $("#addname").val('');
        $("#addipaddr").val('');
    
        var newCamera = new Camera(name, ip, CameraStatus.Started);
    
        cameras.push(newCamera);
        $('#addIPModal').modal('toggle');
    
        renderCameras();

        return false;
    })
})


