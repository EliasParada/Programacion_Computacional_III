window.zindex = 1;

$(document).ready(function(e){
    $("#mnxAppAcademica a").click(function(event){
        event.preventDefault();

        let modulo = $(this).data("modulo"),
            formulario = $(this).data("formulario");
        abrir_ventana(modulo, formulario);
    });
    
});
function abrir_ventana(modulo, formulario){
    $(`#${modulo}_${formulario}`).load(`${modulo}/${modulo}_${formulario}.html`)
        .draggable()
        .click(function(e){
            $(this).css("z-index", ++zindex);
        });
}