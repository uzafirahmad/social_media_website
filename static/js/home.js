$(document).ready(function () {

});
document.addEventListener('DOMContentLoaded', () => {

    var convert = function (convert) {
        return $("<span />", { html: convert }).text();
        //return document.createElement("span").innerText;
    };

    for (var i = 0; i < document.getElementsByClassName("postinhometextofpost").length; i++) {
        str = document.getElementsByClassName("postinhometextofpost")[i].innerHTML;
        str2 = convert(str)
        document.getElementsByClassName("postinhometextofpost")[i].innerHTML = str2.replace("<div><br></div>", "<br>");
    }

});