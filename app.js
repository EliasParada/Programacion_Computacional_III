window.zIndex = 1;

$(document).ready(function() {
    const btn = document.querySelector("button.mobile-menu-button");
    const menu = document.querySelector(".mobile-menu");
    
    btn.addEventListener("click", () => {
        let module = $(this).data("module"),
            form = $(this).data("form");
        abrir_ventana(module, form);
        menu.classList.toggle("hidden");
    });

    function abrir_ventana(module, form) {
        $(`#modal-${module}_${form}.html`).modal('show').dragable();
    }
    
    $('#mnxApp a').click(function() {
        console.log($(this).data('formulario'));
    });
});