function changeImage(id){
    var start = "assets/start.png";
    var pause = "assets/pause.png";
    var imgElement = document.getElementById(id);

    imgElement.src = (imgElement.src.match(start))? pause : start;
}

function clickOnIP(id){
    /*var ipElement = document.getElementsByClassName('card-content')[1];
    ipElement.removeChild();*/

    var num = id.slice(-1);

    var ipElement = document.getElementById(id);
    if(ipElement.style.backgroundColor.match('white')){
        ipElement.style.backgroundColor = '#f0f0f0';

        var ip = document.createElement('h4');
        ip.textContent = "192.168.0." + num; 
        ip.className = "ip-addr ml-3";
        document.getElementsByClassName('card-content')[1].appendChild(ip);
    }
    else
        ipElement.style.backgroundColor = 'white';

}

var uniqueIpID = 0;
function addIP(){
    var ip = document.createElement('h4');
    ip.textContent = "192.168.0." + uniqueIpID.toString(); 
    ip.className = "ip-addr ml-3";

    var startImage = document.createElement('input');
    startImage.type = "image";
    startImage.src = "assets/start.png";
    startImage.id = "ipPauseOrStart" + uniqueIpID.toString();
    startImage.setAttribute("onclick", "changeImage(id);");

    var deleteImage = document.createElement('input');
    deleteImage.type = "image";
    deleteImage.src = "assets/delete.png";

    var outerdiv = document.createElement('div');
    outerdiv.className = "camera-list-item";
    outerdiv.id = "ipElement" + uniqueIpID.toString();
    outerdiv.setAttribute("onclick", "clickOnIP(id);");

    var innerdiv = document.createElement('div');
    innerdiv.className = "icons ml-auto mr-3"

    innerdiv.appendChild(startImage);
    innerdiv.appendChild(deleteImage);
    outerdiv.appendChild(ip);
    outerdiv.appendChild(innerdiv);

    document.getElementsByClassName('card-content')[0].appendChild(outerdiv);

    uniqueIpID += 1;
}
