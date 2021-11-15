let localstream, canvas, video, cxt;

function takePhoto() {
    canvas = document.getElementById('canvas');
    canvas.width = 28;
    canvas.height = 28;
    ctx = canvas.getContext("2d");
    //Negativo
    ctx.globalCompositeOperation = 'difference';
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    //Imprimir en el canvas
    cxt.drawImage(video, 0, 0, canvas.width, canvas.height);
    let data = canvas.toDataURL('image/png');
    document.getElementById("preview").src = data;
    //Insertar en la imagen
    let img = document.getElementById("preview");
    img.src = data;
}

function turnOnCamera() {
    canvas = document.getElementById('canvas');
    cxt = canvas.getContext('2d');
    video = document.getElementById('video');
    video.width = 300;
    video.height = 300;

    if (!navigator.getUserMedia) {
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    }
    if (!window.URL) {
        window.URL = window.URL;
    }

    if (navigator.getUserMedia) {
        navigator.getUserMedia({video: true,audio: false
        }, function (stream) {
            try {
                localstream = stream;
                video.srcObject = stream;
                video.play();
            } catch (err) {
                console.log(err);
                video.srcObject = null;
            }
        }, function (error) {
            swal("Oops...", "Something went wrong!", error); 
        });
    } else {
        swal("Oops...", "Something went wrong!", "error");
        return
    }
}

function turnOffCamera() {
    video.pause();
    video.srcObject = null;
    localstream.getTracks()[0].stop();
}

$('#frmInsert').submit( (e) => {
    e.preventDefault();
    takePhoto();
    console.log($('#preview').attr('src'));
    //Enviar la imagen por metodo post al servidor
    // $.post('http://localhost/', {
    //     img: $('#preview').attr('src')
    // }, (data) => {
    //     swal("Good job!", "You clicked the button!", "success");
    // }
    // );
});


$("#camera").click(function() {
    $("#image").addClass("none");
    $("#video").removeClass("none");
    turnOnCamera();
    document.getElementById("image").value = null;
});

$("#file").click(function() {
    $("#image").removeClass("none");
    $("#video").addClass("none");
    turnOffCamera();
});