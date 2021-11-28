$(document).ready(function(e){
    fillTab('tabPrd', 'products');
    $("#tabs li a").click(function(){
        let active = $("#tabs li a.active").data('tab');
        $(`#${active}`).html("");

        let tab = $(this).data("tab"),
            module = $(this).data("module");
        fillTab(tab, module);
    });
});
function fillTab(tab, module){
    window.console.clear();
    window.console.log($(`#${tab}`), `tabs/${module}.html`);
    $(`#${tab}`).load(`tabs/${module}.html`);
}