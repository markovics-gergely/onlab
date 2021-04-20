var cameras = JSON.parse(localStorage.getItem('cameras'));

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
    ip = ip.replaceAll(".", "-")
    ip = ip.replaceAll(":", "-")

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

            var resp = response.responseText; //JSON-re response.responseJSON
            resp = resp.replaceAll('\\n', "</p><p>");
            resp = resp.replaceAll('"', '<p>');
            console.log(resp);
            $('#result').html(resp);
        },
        error: function(xhr, statusText, err) {
            console.log("Error: " + xhr.status + " " + statusText);
            $('#predictpopup').removeAttr("disabled");

            $('#result').text("Error Predicting");
        }
    });
});