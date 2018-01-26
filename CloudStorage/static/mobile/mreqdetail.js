//20160723
function htmlEncode(string){
    var str = string;
    if (str){
        str = str.replace(/\r\n/g,'</br>');
        str = str.replace(/\n/g,'</br>');
        str = str.replace(/\r/g,'</br>');
        str = str.replace(/ /g,"&nbsp;");
    }
    return str;
}