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

    //TODO predikció
});