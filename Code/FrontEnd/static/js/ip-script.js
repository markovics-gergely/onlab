const CameraStatus = {
    Paused: 0,
    Started: 1,
    Pending: 2
}
Object.freeze(CameraStatus)

function Camera(name, ip, status, imgType) {
    this.name = name;
    this.ip = ip;
    this.status = status;
    this.imgType = imgType;
}
var cameras = [];
var managerpanel = document.getElementById("managerpanel");
var caminfo = document.getElementById("caminfo");
var caminfos = [];

parseCameras();
createCamInfos();
$(document).on("click", ".ipPauseOrStart", function(e) {
    e.stopPropagation();

    var id = $(".ipPauseOrStart").index($(this));

    var status = cameras[id].status
    cameras[id].status = CameraStatus.Pending
    $(this).attr("disabled", "disabled");
    renderCameras();

    if (status == CameraStatus.Paused) {
        $.ajax({
            url: window.location.href + "s:" + id,
            data: {}
        }).done(function(xhr, statusText) {
            console.log(xhr.status);
            cameras[id].status = CameraStatus.Started;
            $(this).removeAttr("disabled");
            renderCameras();
            console.log(cameras[id].status);
        }).fail(function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText + " " + err);
            cameras[id].status = CameraStatus.Paused;
            $(this).removeAttr("disabled");
            renderCameras();
            showSnackBar("Camera cannot start");
            console.log(cameras[id].status);
        }).always(function() {});
    } else if (status == CameraStatus.Started) {
        $.ajax({
            url: window.location.href + "p:" + id,
            data: {}
        }).done(function(xhr, statusText) {
            console.log(xhr.status);
            cameras[id].status = CameraStatus.Paused;
            $(this).removeAttr("disabled");
            renderCameras();
            console.log(cameras[id].status);
        }).fail(function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText + " " + err);
            cameras[id].status = CameraStatus.Paused;
            $(this).removeAttr("disabled");
            renderCameras();
            showSnackBar("Camera was not alive");
            console.log(cameras[id].status);
        }).always(function() {});
    }
})
$(document).on("click", ".ipDelete", function(e) {
    e.stopPropagation();
    if (confirm("Are you sure?")) {
        var id = $(".ipDelete").index($(this));
        $.ajax({
            url: window.location.href + "d:" + id,
            data: {}
        }).done(function(xhr, statusText) {
            console.log(xhr.status);
            cameras.splice(id, 1)
            renderCameras();
        }).fail(function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText);
        }).always(function() {});
    }
    renderCameras();
})
/*$(document).on("click", ".camera-list-item", function() {
    $(".camera-list-item").css('background-color', 'white');

    var id = $(".camera-list-item").index($(this));
    var camera = cameras[id];

    $(this).css('background-color', '#f0f0f0');

    var ipFrame = document.createElement('div');
    ipFrame.className = "camera-info-item";

    var ip = document.createElement('h4');
    ip.textContent = "IP: " + camera.ip;
    ip.className = "ip-addr ml-3";

    ipFrame.appendChild(ip);

    caminfo.innerHTML = "";
    caminfo.appendChild(ipFrame);

    var aliveFrame = document.createElement('div');
    aliveFrame.className = "camera-info-item";

    var alive = document.createElement('h4');
    alive.textContent = "State: Pending...";
    alive.className = "ip-addr ml-3";

    aliveFrame.appendChild(alive);

    caminfo.appendChild(aliveFrame);

    if(!$(this).attr('disabled')){
        cameraAlive(id, alive, $(this));
    }
    else alive.textContent = "State: " + camera.CameraStatus;

    var imgTypeFrame = document.createElement('div');
    imgTypeFrame.className = "camera-info-item";

    var imgType = document.createElement('h4');
    imgType.textContent = "Image Type: " + camera.imgType;
    imgType.className = "ip-addr ml-3";

    imgTypeFrame.appendChild(imgType);

    caminfo.appendChild(imgTypeFrame);
})*/

function createCamInfos(){
    caminfos = [];
    cameras.forEach(function(camera, id){
        var infotable = document.createElement('div');
        infotable.id = "camera-info";
        infotable.className = "card-content";

        var listItem = $(".camera-list-item").index(id);
        $(listItem).css('background-color', 'white');
    
        //ipframe
        var ipFrame = document.createElement('div');
        ipFrame.className = "camera-info-item";
    
        var ip = document.createElement('h4');
        ip.textContent = "IP: " + camera.ip;
        ip.className = "ip-addr ml-3";
    
        ipFrame.appendChild(ip);
    
        //aliveframe
        var aliveFrame = document.createElement('div');
        aliveFrame.className = "camera-info-item";
    
        var alive = document.createElement('h4');
        alive.textContent = camera.CameraStatus == CameraStatus.Paused ? "State: Offline" :  "State: Online";
        alive.className = "ip-addr ml-3";
    
        aliveFrame.appendChild(alive);
        caminfo.appendChild(aliveFrame);
    
        //beforependingframe
        var beforependingFrame = document.createElement('div');
        beforependingFrame.className = "camera-info-item";
        $(beforependingFrame).css('visibility', 'false');

        var beforepending = document.createElement('h4');
        beforepending.textContent = alive.textContent;
        beforepending.className = "ip-addr ml-3";

        beforependingFrame.appendChild(beforepending);
        caminfo.appendChild(beforependingFrame);

        //imgtypeframe
        var imgTypeFrame = document.createElement('div');
        imgTypeFrame.className = "camera-info-item";
    
        var imgType = document.createElement('h4');
        imgType.textContent = "Image Type: " + camera.imgType;
        imgType.className = "ip-addr ml-3";
    
        imgTypeFrame.appendChild(imgType);
    
        //add all
        infotable.appendChild(ipFrame);
        infotable.appendChild(aliveFrame);
        infotable.appendChild(beforependingFrame);
        infotable.appendChild(imgTypeFrame);

        caminfos.push(infotable);

        $(listItem).on("click", function(){
            $(".camera-list-item").css('background-color', 'white');
    
            $(listItem).css('background-color', '#f0f0f0');
            caminfo = infotable;

            if(!$(listItem).attr('disabled')){
                beforependingFrame.css('visibility', 'true');
                cameraAlive(id, alive, $(listItem), $(beforependingFrame));
            }
        })
    })
}

function renderCameras() {
    managerpanel.innerHTML = "";
    cameras.forEach(function(camera, id) {
        var name = document.createElement('h4');
        name.textContent = camera.name;
        name.className = "ip-addr ml-3";

        var startspan = document.createElement('span');
        startspan.className = "btn material-icons-outlined blue-icon ipPauseOrStart px-1";
        if (camera.status == CameraStatus.Paused) startspan.textContent = "play_arrow";
        else if (camera.status == CameraStatus.Started) startspan.textContent = "pause";
        else if (camera.status == CameraStatus.Pending) startspan.textContent = "pending";

        var deletespan = document.createElement('span');
        deletespan.className = "btn material-icons-outlined blue-icon ipDelete px-1";
        deletespan.textContent = "delete";

        var outerdiv = document.createElement('form');
        outerdiv.className = "camera-list-item";

        var innerdiv = document.createElement('div');
        innerdiv.className = "icons ml-auto mr-3";

        innerdiv.appendChild(startspan);
        innerdiv.appendChild(deletespan);
        outerdiv.appendChild(name);
        outerdiv.appendChild(innerdiv);

        managerpanel.appendChild(outerdiv);
    })
    createCamInfos();
}
function parseCameras() {
    $.ajax({
        type: "GET",
        url: window.location.href + "clist",
        data: {},
        dataType: "json",
        success: function(data) {
            var d = data.clist;
            d.forEach(function(c, id) {
                console.log(c);
                if (c.status == CameraStatus.Started) {
                    var camera = new Camera(c.name, c.ip, CameraStatus.Pendin, c.imgType);
                    cameras.push(camera);
                    cameraStartable(id, camera);
                } else {
                    var camera = new Camera(c.name, c.ip, c.status, c.imgType);
                    cameras.push(camera);
                }
            });
            renderCameras();
            cameraCheck();
        }
    });
}
function checkname(input) {
    var unique = true;
    cameras.forEach(function(c) {
        if (c.name == input.value) {
            unique = false;
        }
    })
    if (unique) input.setCustomValidity('');
    else input.setCustomValidity('Camera Name must be unique');
}
function checkip(input) {
    var ipregex = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]{1,5}$/;
    var unique = true;
    cameras.forEach(function(c) {
        if (c.ip == input.value) {
            unique = false;
        }
    })
    if (!unique) input.setCustomValidity('IP address must be unique');
    else if (!input.value.match(ipregex)) input.setCustomValidity('IP address must be valid');
    else input.setCustomValidity('');
}

$(".addForm").on('submit', function(e) {
    e.preventDefault();
    $('#addSubmit').attr("disabled", "disabled");

    var name = $('#addname').val();
    var ip = $('#addipaddr').val();
    var selector = document.getElementById("StatusSelect");
    var imgType = $('#addimgtype').val();

    var jsondata = { "name": name, "ip": ip, "status": selector.selectedIndex, "imgType": imgType }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: window.location.href + "a",
        data: JSON.stringify(jsondata),
        success: function(xhr, statusText) {
            console.log(xhr.status);
            if (selector.selectedIndex == 1) {
                var camera = new Camera(name, ip, 2)
                cameras.push(camera);
                cameraStartable(cameras.indexOf(camera), camera);
            } else cameras.push(new Camera(name, ip, selector.selectedIndex));

            renderCameras();
            $("#addIPModal").modal('toggle');
            $('#addSubmit').removeAttr("disabled");

            $('#addname').val("");
            $('#addipaddr').val("");
            $("#StatusSelect").selectedIndex = 0;
        },
        error: function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText);
            $('#addSubmit').removeAttr("disabled");
        }
    });
});

function saveCamerasToLocal() {
    localStorage.setItem('cameras', JSON.stringify(cameras));
}

$('.pred-link').on('click', function() {
    saveCamerasToLocal();
})

function showSnackBar(text) {
    var snackbar = document.getElementById("snackbar");

    snackbar.textContent = text;

    // Add the "show" class to DIV
    snackbar.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function() { snackbar.className = snackbar.className.replace("show", ""); }, 3000);
}

function cameraAlive(id, container, parent, before) {
    parent.attr("disabled", "disabled");
    $.ajax({
        url: window.location.href + "alive:" + id,
        data: {}
    }).done(function(xhr, statusText) {
        console.log(xhr.status);
        container.textContent = "State: Online";
        before.children(".ip-addr").textContent = container.textContent;
        before.css('visibility', 'false');
        parent.removeAttr("disabled");
    }).fail(function(xhr, statusText, err) {
        console.log(xhr.status);
        container.textContent = "State: Offline";
        before.children(".ip-addr").textContent = container.textContent;
        before.css('visibility', 'false');
        cameras[id].status = CameraStatus.Paused;
        parent.removeAttr("disabled");
        renderCameras();
    });
}

function cameraStartable(id, camera) {
    $.ajax({
        url: window.location.href + "alive:" + id,
        data: {}
    }).done(function(xhr, statusText) {
        console.log(xhr.status);
        camera.status = CameraStatus.Started
        renderCameras();
    }).fail(function(xhr, statusText, err) {
        console.log(xhr.status);
        camera.status = CameraStatus.Paused;
        renderCameras();
    });
}

function cameraCheck() {
    $.ajax({
        url: window.location.href + "atstart",
        data: {}
    }).done(function(xhr, statusText) {
        console.log(xhr.status);
    }).fail(function(xhr, statusText, err) {
        console.log(xhr.status);
    });
}

$(document).on("click", "#expand-button", function(e) {
    $("#expand-button").blur();
    $("#expand-button").hideFocus = true;
    if($("#expand-span").text() === "expand_more"){
        $("#advanced-modal").removeAttr("hidden");
        $("#expand-span").text("expand_less");
    }
    else if($("#expand-span").text() === "expand_less"){
        $("#advanced-modal").attr("hidden", "hidden");
        $("#expand-span").text("expand_more");
    }
})

$("#addIPModal").on("hidden.bs.modal", function () {
    $("#advanced-modal").attr("hidden", "hidden");
    $("#expand-span").text("expand_more");
});