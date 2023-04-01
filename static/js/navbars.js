$(document).ready(function () {
  $("#dimscreen").bind("click", function () {
    document.getElementById("dimscreen").style.display = "none";
    document.getElementById("dimscreen").style.visibility = "hidden";
    document.getElementById("mysidebar").style.width = "0px";
    document.getElementById("mysidebar").style.display = "none";
    document.getElementById("mysidebar").style.visibility = "hidden";
    document.getElementById("dimscreen").style.opacity = "0";
  });
});

function openclose() {
  // close sidebar
  if (document.getElementById("mysidebar").style.width == "201px") {
    document.getElementById("dimscreen").style.display = "none";
    document.getElementById("dimscreen").style.visibility = "hidden";
    document.getElementById("mysidebar").style.width = "0px";
    document.getElementById("mysidebar").style.display = "none";
    document.getElementById("mysidebar").style.visibility = "hidden";
    document.getElementById("dimscreen").style.opacity = "0";
  }
  // open sidebar
  else {
    document.getElementById("dimscreen").style.display = "block";
    document.getElementById("mysidebar").style.width = "201px";
    document.getElementById("mysidebar").style.display = "block";
    document.getElementById("mysidebar").style.visibility = "visible";
    document.getElementById("dimscreen").style.opacity = "0.7";
    document.getElementById("dimscreen").style.visibility = "visible";
    document.getElementById("mysidebar").style.pointerEvents = "auto";
    // document.getElementById("myheadernavbar").style.pointerEvents = "auto";
    // document.getElementById("mylogoutpopup").style.pointerEvents = "auto";
  }
}

function opencloselogoutpopup() {
  // open
  if (document.getElementById("mylogoutpopup").style.display == "block") {
    document.getElementById("mylogoutpopup").style.visibility = "hidden";
    document.getElementById("mylogoutpopup").style.display = "none";
  }
  // close
  else {
    document.getElementById("mylogoutpopup").style.display = "block";
    document.getElementById("mylogoutpopup").style.visibility = "visible";
  }
}

// setInterval(function () {
//   $.ajax({
//     type: 'GET',
//     url: 'getnotifications/',
//     success: function (response) {

//     }
//   });
// }, 1000);
