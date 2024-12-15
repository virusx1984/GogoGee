var file_ext = '.html';
var app_base_url = 'http://127.0.0.1:8000/';

//#region getCookie
function getCookie(name){
    var cookieValue = null;
    if(document.cookie && document.cookie !== ''){
        var cookies = document.cookie.split(';');
        for(var i = 0; i < cookies.length; i++){
            var cookie = jQuery.trim(cookies[i]);
            //? Does this cookie string begin with the name we want?
            if(cookie.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
}
//#endregion getCookie

//#region setCookie
function setCookie(name, value, days){
    var expires = '';
    if(days){
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + value + expires + '; path=/';
}
//#endregion setCookie

//#region setTopAndSideMenu
function setTopAndSideMenu(){
    var csrftoken = getCookie('csrftoken');
    var thisFilePath = new URL(window.location.href).pathname;
    var thisFileName = thisFilePath.replace('.html', '').slice(1);

    // get current user information
    curr_user_id = localStorage.getItem('curr_user_id');
    username = localStorage.getItem('curr_username');

    if(curr_user_id === null){
        window.location.href = 'login' + file_ext;
    }

    exist_ava_menu_update_dt = localStorage.getItem(curr_user_id.toString() + ':ava_menu_update_dt');

    //#region get-available-menu
    $.ajax({
        url: app_base_url + 'get-available-menu/',
        type: 'POST',
        dataType: 'json',
        data: {
            curr_user_id: curr_user_id,
            exist_ava_menu_update_dt: exist_ava_menu_update_dt == null ? 0 : exist_ava_menu_update_dt,
        },
        xhrFields: {
            withCredentials: true,
        },
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function(response){
            // check if logined
            let isLogin = response['login'];
            if(isLogin == false){
                nextUrl = window.location.pathname.replace(/^\//, '');
                window.location.href = 'login' + file_ext + '?next-url=' + encodeURIComponent(nextUrl);
            }

            let status = response['status'];
            if(sttus == 'user not match'){
                window.location.href = 'login' + file_ext;
            }
        },
        error: function(xhr, textStatus, errorThrown){
            console.error(errorThrown);
        }
    });
    //#endregion get-available-menu

}
//#endregion setTopAndSideMenu

