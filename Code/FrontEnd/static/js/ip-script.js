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
    this.beforestatus = CameraStatus.Paused;
    this.canShow = false;
}
var cameras = [];
var managerpanel = document.getElementById("managerpanel");
var caminfo = document.getElementById("caminfo");
var showDataBody = document.getElementById("showDataBody");
var showImageInterval;

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
            

            //Ha elindítható a kamera akkor fix online, tehát lehet nézni a képet
            cameras[id].canShow = true
            //makeCameraVisible($($(".ipPauseOrStart")[id]).parent());
            renderCameras();
            console.log(cameras[id].status);
        }).fail(function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText + " " + err);
            cameras[id].status = CameraStatus.Paused;
            cameras[id].canShow = false;
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
            createCamInfos();
        }).fail(function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText);
        }).always(function() {});
    }
    renderCameras();
})
$(document).on("click", ".ipShowImage", function(e) {
    e.stopPropagation();
    var id = $(".ipShowImage").index($(this));
    var ip = cameras[id].ip;
    ip = ip.replace(/[.:]/gi, "-");
    showImageInterval = setInterval(function(){ refreshImage(ip); }, 1000);
})

function createCamInfo(camera, id){
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
    aliveFrame.className = "camera-info-item alive";
    
    var alive = document.createElement('h4');
    alive.textContent = camera.CameraStatus == CameraStatus.Started ? "State: Online" :  "State: Offline";
    alive.className = "ip-addr ml-3";
    
    aliveFrame.appendChild(alive);
    caminfo.appendChild(aliveFrame);
    
    //beforependingframe
    var beforependingFrame = document.createElement('div');
    beforependingFrame.className = "camera-info-item before";
    $(beforependingFrame).css('display', 'none');

    var beforepending = document.createElement('h4');
    beforepending.textContent = camera.beforestatus == CameraStatus.Started ? "Before Pending: Online" :  "Before Pending: Offline";
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
    
    //dataframe
    var dataFrame = document.createElement('div');
    dataFrame.className = "camera-info-item";
    dataFrame.setAttribute("data-toggle", "modal");
    dataFrame.setAttribute("data-target", "#showDataModal");

    var data = document.createElement('h4');
    data.textContent = "Show Data Table";
    data.className = "ip-addr ml-3 dataButton";

    dataFrame.appendChild(data);

    $(dataFrame).on("click", function(e) {
        getJSONdata(id);
    })

    //add all
    caminfo.innerHTML = "";
    caminfo.appendChild(ipFrame);
    caminfo.appendChild(aliveFrame);
    caminfo.appendChild(beforependingFrame);
    caminfo.appendChild(imgTypeFrame);
    caminfo.appendChild(dataFrame);
}

function makeCameraVisible(parent){
    var element = parent.children(".ipShowImage");
    $(element).css("pointer-events", "auto");
    $(element).text("visibility");
}

function renderCameras() {
    managerpanel.innerHTML = "";
    cameras.forEach(function(camera) {
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

        var showimagespan = document.createElement('span');
        showimagespan.className = "btn material-icons-outlined blue-icon ipShowImage px-1";
        showimagespan.setAttribute("data-toggle", "modal");
        showimagespan.setAttribute("data-target", "#showImageModal");
        showimagespan.textContent = "visibility_off";
        

        var outerdiv = document.createElement('form');
        outerdiv.className = "camera-list-item";

        var innerdiv = document.createElement('div');
        innerdiv.className = "icons ml-auto mr-3";

        innerdiv.appendChild(showimagespan);
        innerdiv.appendChild(startspan);
        innerdiv.appendChild(deletespan);
        outerdiv.appendChild(name);
        outerdiv.appendChild(innerdiv);

        managerpanel.appendChild(outerdiv);

        if(camera.canShow) makeCameraVisible($(innerdiv));
        else $(showimagespan).css("pointer-events", "none");

        $(outerdiv).on("click", function(){
            $(".camera-list-item").css('background-color', 'white');
            var id = $(".camera-list-item").index(outerdiv);

            $(outerdiv).css('background-color', '#f0f0f0');
            createCamInfo(camera, id);

            var beforeFrame = $(caminfo).children(".before");
            beforeFrame.css('display', 'block');
            var alive = $(caminfo).children(".alive").children(".ip-addr");
            alive.text("State: Pending...");

            cameraAlive(id, alive, $(outerdiv), $(beforeFrame));
        })
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
                console.log(c);
                if (c.status == CameraStatus.Started) {
                    var camera = new Camera(c.name, c.ip, CameraStatus.Pending, c.imgType);
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
            } else cameras.push(new Camera(name, ip, selector.selectedIndex, imgType));

            renderCameras();
            $("#addIPModal").modal('toggle');
            $('#addSubmit').removeAttr("disabled");

            $('#addname').val("");
            $('#addipaddr').val("");
            $("#StatusSelect").selectedIndex = 0;
            createCamInfos();
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
    $.ajax({
        url: window.location.href + "alive:" + id,
        data: {}
    }).done(function(xhr, statusText) {
        console.log(xhr.status);
        container.text("State: Online");

        before.children(".ip-addr").text("Before Pending: Online");
        before.css('display', 'none');

        cameras[id].beforestatus = CameraStatus.Started;
    }).fail(function(xhr, statusText, err) {
        console.log(xhr.status);
        container.text("State: Offline");
        before.children(".ip-addr").text("Before Pending: Offline");
        before.css('display', 'none');
        cameras[id].canShow = false;
        cameras[id].status = CameraStatus.Paused;
        cameras[id].beforestatus = CameraStatus.Paused;
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
        camera.canShow = true;
        renderCameras();
    }).fail(function(xhr, statusText, err) {
        console.log(xhr.status);
        camera.status = CameraStatus.Paused;
        camera.canShow = false;
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
    $("#addimgtype").val("shot.jpg");
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
    $("#addimgtype").val("shot.jpg");
});

$("#showImageModal").on("hidden.bs.modal", function () {
    clearInterval(showImageInterval);
});

function refreshImage(ip){
    var element = document.getElementById("shownImage");
    element.src = "DB/cameraPhotos/" + ip + ".png?" + Date.now();
}

function getJSONdata(id) {
    $.ajax({
        type: "GET",
        url: window.location.href + "data:" + id,
        data: {},
        dataType: "json",
        success: function(data) {
            var rows = JSON.parse(data);
            rows.forEach(function(d, id){
                d.age = d.age.replace(/[\"\[\]]/gi, "");
                d.age = d.age.split(", ");
                d.age = d.age.map(Number);
                d.gender = d.gender.replace(/[\"\[\]]/gi, "");
                d.gender = d.gender.split(", ");
                d.gender = d.gender.map(Number);
                
            });
            createDataTable(rows);
            console.log(rows);
        }
    });
}

function createDataTable(data){
    showDataBody.innerHTML = "";

    let row = document.createElement("div");
    row.className = "row";
        
    let cardboxname = document.createElement("div");
    cardboxname.className = "cardbox pred-info-info col-sm-12 col-md-12 col-lg-2";

    let name = document.createElement("h4");
    name.className = "pred-id-name";
    name.textContent = "Time";

    cardboxname.appendChild(name);
    row.appendChild(cardboxname);

    let middle = document.createElement("div");
    middle.className = "cardbox show-table-middle col-sm-12 col-md-12 col-lg-7";
    let middlevalue = document.createElement("h4");
    middlevalue.className = "pred-value";
    middlevalue.textContent = "Age Data";
    
    middle.appendChild(middlevalue);
        
    row.appendChild(middle);

    let cardboxvalue = document.createElement("div");
    cardboxvalue.className = "cardbox pred-info-item col-sm-12 col-md-12 col-lg-2";
    let value = document.createElement("h4");
    value.className = "pred-value";
    value.textContent = "Gender Data";
    cardboxvalue.appendChild(value);
    row.appendChild(cardboxvalue);

    showDataBody.append(row);

    data.slice().reverse().forEach(function(rowdata){
        let row = document.createElement("div");
        row.className = "row my-1";
        
        let cardboxname = document.createElement("div");
        cardboxname.className = "cardbox pred-info-info col-sm-12 col-md-12 col-lg-2";

        let name = document.createElement("div");
        name.className = "pred-id-name";
        name.textContent = rowdata.time;

        cardboxname.appendChild(name);
        row.appendChild(cardboxname);

        let middle = document.createElement("div");
        middle.className = "cardbox show-table-middle col-sm-12 col-md-12 col-lg-7 py-1";
        rowdata.age.forEach(function(agedata){
            let middlevalue = document.createElement("div");
            middlevalue.className = "data-value mx-auto";
            middlevalue.textContent = agedata;
    
            let middlegrid = document.createElement("div");
            middlegrid.className = "datagrid mx-1";

            middlegrid.appendChild(middlevalue)

            middle.appendChild(middlegrid);
        })
        
        row.appendChild(middle);

        let cardboxvalue = document.createElement("div");
        cardboxvalue.className = "cardbox pred-info-item col-sm-12 col-md-12 col-lg-2 py-1";
        rowdata.gender.forEach(function(genderdata){
            let value = document.createElement("div");
            value.className = "data-value mx-auto";
            value.textContent = genderdata;
    
            let lastgrid = document.createElement("div");
            lastgrid.className = "datagrid mx-1";

            lastgrid.appendChild(value)

            cardboxvalue.appendChild(lastgrid);
        });
        row.appendChild(cardboxvalue);

        

        showDataBody.append(row);
    });

    var footerage = ["0-6", "6-12", "12-18", "18-26", "26-36", "36-48", "48-60", "60-100"];
    var footergender = ["Women", "Men"];

    var footer = document.getElementById("showModalDataFooter");
    footer.innerHTML = "";

    let footerrow = document.createElement("div");
    footerrow.className = "row my-2";
        
    let footercardboxname = document.createElement("div");
    footercardboxname.className = "cardbox pred-info-info col-sm-12 col-md-12 col-lg-2";

    let footername = document.createElement("div");
    footername.className = "pred-id-name";
    footername.textContent = "Data Headers:";

    footercardboxname.appendChild(footername);
    footerrow.appendChild(footercardboxname);

    let footermiddle = document.createElement("div");
    footermiddle.className = "cardbox show-table-middle col-sm-12 col-md-12 col-lg-7 py-1";
    footerage.forEach(function(agedata){
        let middlevalue = document.createElement("div");
        middlevalue.className = "data-value mx-auto";
        middlevalue.textContent = agedata;
    
        let middlegrid = document.createElement("div");
        middlegrid.className = "datagrid mx-1";

        middlegrid.appendChild(middlevalue)

        footermiddle.appendChild(middlegrid);
    })
        
    footerrow.appendChild(footermiddle);

    let footercardboxvalue = document.createElement("div");
    footercardboxvalue.className = "cardbox pred-info-item col-sm-12 col-md-12 col-lg-2 py-1";
    footergender.forEach(function(genderdata){
        let value = document.createElement("div");
        value.className = "data-value mx-auto";
        value.textContent = genderdata;
    
        let lastgrid = document.createElement("div");
        lastgrid.className = "datagrid mx-1";

        lastgrid.appendChild(value)

        footercardboxvalue.appendChild(lastgrid);
    });
    footerrow.appendChild(footercardboxvalue);

    footer.append(footerrow);
}