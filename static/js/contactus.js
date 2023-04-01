$(document).ready(function () {
    setTimeout(() => {
        let query = window.matchMedia("(max-width: 450px)");
        if (query.matches) {
            console.log("hello")
            document.getElementById("changepasswordchildrendivtextdesc").style.flexDirection="column";
            document.getElementById("changepasswordchildrendivtextdesc").style.justifyContent="center";
            document.getElementById("changepasswordchildrendivtextdesc").style.alignItems="center";
        }
    }, 100);
});