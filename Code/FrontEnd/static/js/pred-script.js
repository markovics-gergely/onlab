var cameras = JSON.parse(localStorage.getItem('cameras'));
var colorBuffer = [];
var genderInterval = [];
var ageInterval = [];

$(".stat-table").css("display", "none");
$(".graph-table").css("display", "none");

function appendCameras(){
    $('#CameraNameSelect').empty();
    cameras.forEach(function(c, id) {
        $('#CameraNameSelect').append('<option value="' + id + '">' + c.name + ' - ' + c.ip + '</option>');
    });
}
appendCameras();

$('#dateInput').on('change', function () {
    var dateNow = new Date().toJSON().slice(0, 10)
    var pickedDate = $('input').val();
    if(pickedDate < dateNow) this.setCustomValidity('Date must be in the future');
    else this.setCustomValidity('');
});

$(".predictForm").on('submit',function(e){
    e.preventDefault();
    $('#predictpopup').attr("disabled", "disabled");
    $('#result').css("display", "block");
    $("#predictModal").modal('toggle');

    var ipID = $('#CameraNameSelect').prop('selectedIndex');
    var ip = cameras[ipID].ip;
    ip = ip.replaceAll(".", "-");
    ip = ip.replaceAll(":", "-");

    var date = $("#dateInput").val();
    var intervalID = $("#intervalSelect").prop('selectedIndex');
    var fullDate = new Date(date);

    fullDate.setHours(intervalID * 2);
    $('#result').text("Pending...");

    var jsondata = { "camera": ip, "date": fullDate };
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: window.location.href + "p",
        data: JSON.stringify(jsondata),
        success: function(xhr, statusText, response) {
            console.log(xhr.status);
            $('#predictpopup').removeAttr("disabled");
            $('#result').css("display", "none");

            var resp = JSON.parse(response.responseText);
            loadData(resp);
            $(".stat-table").css("display", "flex");
            loadImages();
        },
        error: function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText);
            $('#predictpopup').removeAttr("disabled");

            $('#result').text("Error Predicting");
        }
    });
});

function loadImages(){
    $.ajax({
        url: window.location.href + "img",
        data: {}
    }).done(function(xhr, statusText) {
        console.log(xhr.status);
        let i;
        for(i = 0; i < 6; i++){
            createImage(i);
        }
        $(".graph-table").css("display", "flex");
    }).fail(function(xhr, statusText, err) {
        console.log("Error: " + xhr.status + " " + statusText);
    }).always(function() {});
}

function loadData(json){
    let ageBuffer = json["ageBuffer"];
    let genderBuffer = json["genderBuffer"];
    let agePercentBuffer = json["agePercentBuffer"];
    let genderPercentBuffer = json["genderPercentBuffer"];

    ageInterval = json["ageIntervalInfo"];
    genderInterval = json["genderIntervalInfo"];

    colorBuffer = json["colorBuffer"];
    createList(ageBuffer, agePercentBuffer, ageInterval, "age-con", "ageper-con");
    createList(genderBuffer, genderPercentBuffer, genderInterval, "gender-con", "genderper-con");
}

function createList(buffer, percentBuffer, interval, numid, perid){
    var root = document.getElementById(numid);
    var rootpercent = document.getElementById(perid);

    buffer.forEach((num, id) => {
        let row = document.createElement("div");
        row.className = "row";
        
        let cardboxname = document.createElement("div");
        cardboxname.className = "cardbox pred-info-info col-sm-12 col-md-12 col-lg-3";

        let name = document.createElement("h4");
        name.className = "pred-id-name";
        name.textContent = interval[id];

        cardboxname.appendChild(name);
        row.appendChild(cardboxname);

        let cardboxvalue = document.createElement("div");
        cardboxvalue.className = "cardbox pred-info-item col-sm-12 col-md-12 col-lg-8";

        let value = document.createElement("h4");
        value.className = "pred-value";
        value.textContent = num + " predicted";

        cardboxvalue.appendChild(value);
        row.appendChild(cardboxvalue);

        root.appendChild(row);

        let rowpercent = document.createElement("div");
        rowpercent.className = "row";

        let cardboxpercentname = document.createElement("div");
        cardboxpercentname.className = "cardbox pred-info-info col-sm-12 col-md-12 col-lg-3";
        cardboxpercentname.innerHTML = cardboxname.innerHTML;

        let cardboxpercentvalue = document.createElement("div");
        cardboxpercentvalue.className = "cardbox pred-info-item col-sm-12 col-md-12 col-lg-8";

        let percentvalue = document.createElement("h4");
        percentvalue.className = "pred-value";
        percentvalue.textContent = percentBuffer[id] + "%";
        cardboxpercentvalue.appendChild(percentvalue);

        rowpercent.appendChild(cardboxpercentname);
        rowpercent.appendChild(cardboxpercentvalue);

        rootpercent.appendChild(rowpercent);
    });
}

function createImage(id){
    let image = document.getElementById("plotImage" + id);
    let palette = document.getElementById("colorPalette" + id);

    image.src = "../../DB/predPhotos/predImage" + id +".png";
    if(id < 3){
        let ageID;
        for(ageID = 0; ageID < 8; ageID++){
            let frame = document.createElement("div");
            frame.className = "colorFrame";
            
            let dot = document.createElement("div");
            dot.className = "colorDot";
            $(dot).css("backgroundColor", colorBuffer[ageID]);
            let value = document.createElement("h4");
            value.className = "pred-value";
            value.textContent = ageInterval[ageID];

            frame.appendChild(dot);
            frame.appendChild(value);

            palette.appendChild(frame);
        }
    }
    else {
        let genderID;
        for(genderID = 0; genderID < 2; genderID++){
            let frame = document.createElement("div");
            frame.className = "colorFrame";
            
            let dot = document.createElement("div");
            dot.className = "colorDot";

            $(dot).css("backgroundColor", colorBuffer[8 + genderID]);

            let value = document.createElement("h4");
            value.className = "pred-value";
            value.textContent = genderInterval[genderID];

            frame.appendChild(dot);
            frame.appendChild(value);

            palette.appendChild(frame);
        }
    }
}