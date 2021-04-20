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
    $('#result').css("display", "block");
    $("#predictModal").modal('toggle');

    var name = $('#addname').val();
    var ip = $('#addipaddr').val();
    var selector = document.getElementById("StatusSelect");

    //NEM JÓ, EZT KELL MEGCSINÁLNI
    var date = document.getElementById("dateSelect");
    var interval = document.getElementById("intveralSelect");

    var normalDate = date + " " + interval.selectedIndex;
    console.log(normalDate);

    var jsondata = { "camera": ip , "date": normalDate};
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: window.location.href + "p",
        data: JSON.stringify(jsondata)
    });
});