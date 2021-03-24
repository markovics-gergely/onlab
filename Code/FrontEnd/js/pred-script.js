var cameras = JSON.parse(localStorage.getItem('cameras'));

function appendCameras(){
    $('#CameraNameSelect').empty();
    cameras.forEach(function(c, id) {
        $('#CameraNameSelect').append('<option value="' + id + '">' + c.name + ' - ' + c.ip + '</option>');
    });
}

appendCameras();

/*$('#dateSelect').datepicker({
    todayBtn: "linked",
    language: "hu",
    autoclose: true,
    todayHighlight: true
});*/

$(".predictForm").on('submit',function(e){
    e.preventDefault();
    $('#result').css("display", "block");
    $("#predictModal").modal('toggle');
});