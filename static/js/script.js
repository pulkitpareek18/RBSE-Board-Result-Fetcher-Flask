let twelfth = document.getElementById('twelfth');
let tenth = document.getElementById('tenth');
let streamContainer = document.getElementById('streamContainer');


function showHide(){
    if(twelfth.checked){
        streamContainer.style.display = "flex";
    }else{
        streamContainer.style.display = "none";
    }
}


if(twelfth.checked){
    streamContainer.style.display = "flex";
}else{
    streamContainer.style.display = "none";
}