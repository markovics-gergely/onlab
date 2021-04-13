const CameraStatus = {
    Paused: 0,
    Started: 1,
    Pending: 2
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
    console.log(status);
    console.log(cameras[id].status);
})
$(document).on("click", ".ipDelete", function(e) {
    e.stopPropagation();
    if (confirm("Are you sure?")) {
        var id = $(".ipDelete").index($(this));
        $(this).children(".ipDelete").attr("src", "FrontEnd/static/image/pending.png");
        renderCameras();
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
$(document).on("click", ".camera-list-item", function() {
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

    cameraAlive(id, alive)
})

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
                if (c.status == CameraStatus.Started) {
                    var camera = new Camera(c.name, c.ip, CameraStatus.Pending);
                    cameras.push(camera);
                    cameraStartable(id, camera);
                } else {
                    var camera = new Camera(c.name, c.ip, c.status);
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

    var jsondata = { "name": name, "ip": ip, "status": selector.selectedIndex }
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

function cameraAlive(id, container) {
    $.ajax({
        url: window.location.href + "alive:" + id,
        data: {}
    }).done(function(xhr, statusText) {
        console.log(xhr.status);
        container.textContent = "State: Online";
    }).fail(function(xhr, statusText, err) {
        console.log(xhr.status);
        container.textContent = "State: Offline";
        cameras[id].status = CameraStatus.Paused;
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