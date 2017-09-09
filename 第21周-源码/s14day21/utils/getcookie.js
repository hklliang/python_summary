/**
 * Created by Administrator on 2017/9/9.
 */
function getcookie() {
    var cookies = document.cookie
    temp = cookies.split(';')
    cookie_list = []
    for (var i = 0; i < temp.length; i++) {
        cookie_list.push(temp[i].split('='))

    }
    return cookie_list
}

function setcookie(cookie_list, expired_day) {


    var Days = expired_day;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    cookies_str_list = []
    for (var i = 0; i < cookie_list.length; i++) {
        cookie_name = cookie_list[i][0];
        cookie_value = cookie_list[i][1];
        str = cookie_name + '=' + cookie_value + ';expires=' + exp.toGMTString() + ';'

        cookies_str_list.push(str);
    }
    cookies_str = cookies_str_list.join('');
    document.cookie = cookies_str;
    return cookies_str
}

function setcookie2(expired_day) {
    var cookies = document.cookie
    var temp = cookies.split(';')
    var exp = new Date();
    cookies_str_list = []
    exp.setTime(exp.getTime() + expired_day * 24 * 60 * 60 * 1000);
    for (var i = 0; i < temp.length; i++) {

        str=temp[i]+';expires=' + exp.toGMTString() + ';'
        cookies_str_list.push(str);
    }
    cookies_str = cookies_str_list.join('');
    document.cookie = cookies_str;
    return cookies_str
}