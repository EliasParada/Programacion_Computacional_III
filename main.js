function clearForms(form) {
    $(`form`).find('input:text, input:password, input:file, input[type=date], input[type=email], input[type=tel], input[type=number], select, textarea').val('');
    $(`form`).data('action', 'create');
    $(`form`).data('id', 0);
}

function adminPetition(url, data, method, next, form = null) {
    console.log('adminPetition>', url, data, method, next, 'Hay tabla?', form);
    if (method == "GET") {
        $.get(url, (res) => {
            res = res.response;
            console.log('GET petition response is',res);
            if (res[0] != false) {
                if (form != null) {
                    clearForms(form);
                }
                showToast(res[1], 'green rounded toast-mobile');
                nextStep(next, res[0]);
            } else {
                showToast(res[1], 'red rounded toast-mobile');
            }
        }, 'json');
    } else if (method == "POST") {
        $.post(url, JSON.stringify(data), (res) => {
            res = res.response;
            console.log('POST petition response is', res);
            if (res[0] != false) {
                if (form != null) {
                    clearForms(form);
                }
                showToast(res[1], 'green rounded toast-mobile');
                nextStep(next, res[0]);
            } else {
                showToast(res[1], 'red rounded toast-mobile');
            }
        }, 'json');
    }
}

function nextStep(step, data) {
    console.log('nextStep>', step, data);
    switch (step) {
        case 'selectCategories':
            showSltCategories(data);
            break;
        case 'tableCategories':
            showCategories(data);
            break;
        case 'reloadCategories':
            adminPetition('http://localhost:3000/show_categories', {}, 'GET', 'tableCategories');
            break;
        case 'selectProviders':
            showSltProviders(data);
            break;
        case 'tableProviders':
            showProviders(data);
            break;
        case 'reloadProviders':
            adminPetition('http://localhost:3000/show_providers', {}, 'GET', 'tableProviders');
            break;
        case 'selectProducts':
            showSltProducts(data);
            break;
        case 'tableProducts':
            showProducts(data);
            break;
        case 'reloadProducts':
            adminPetition('http://localhost:3000/show_products', {}, 'GET', 'tableProducts');
            break;
        case 'selectFeatures':
            showSltFeatures(data);
            break;
        case 'tableFeatures':
            showFeatures(data);
            break;
        case 'reloadFeatures':
            adminPetition('http://localhost:3000/show_features', {}, 'GET', 'tableFeatures');
            break;
        case 'selectUsers':
            showSltUsers(data);
            break;
        case 'tableUsers':
            showUsers(data);
            break;
        case 'reloadUsers':
            adminPetition('http://localhost:3000/show_users', {}, 'GET', 'tableUsers');
        default:
            break;
    }
}

function showToast(message, type) {
    console.log('showToast', message, type);
    
    if (message.hasOwnProperty('code')) {
        if (message.code[0] == 1062) {
            console.log('Duplicate entry');
            console.log(message.code[1].includes('ux_dui'));
            if (message.code[1].includes('ux_dui')) {
                message.msg = 'El DUI ya existe';
            } else if (message.code[1].includes('ux_tag')) {
                message.msg = 'El nombre de usuario ya existe';
            }
        }
    }
    M.toast({
        html: message.msg,
        classes: type
    });
}

function fillTab(tab, module){
    window.console.clear();
    window.console.log($(`#${tab}`), `tabs/${module}.html`);
    $(`#${tab}`).load(`tabs/${module}.html`);
}

$(document).ready(function(){
    $('select').formSelect();
    $('.tabs').tabs();
    $("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: 'absolute'});
    $('textarea#txtCatDescription, input#txtCatName, #txtProvName, #txtProvPhone, #txtProvEmail').characterCounter();
    $('#vidContainer').hide();
    $('.sidenav').sidenav();

    $("#tabs li a").each(function(index){
        if ($(this).hasClass('active')) {
            fillTab($(this).data('tab'), $(this).data('module'));
        }
    });
    $("#tabs li a").click(function(){
        let active = $("#tabs li a.active").data('tab');
        $(`#${active}`).html("");

        let tab = $(this).data("tab"),
            module = $(this).data("module");
        fillTab(tab, module);
    });
});