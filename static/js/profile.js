var indexofuploadbutton = "";
var cropper;
var imageFile;
var base64ImageString;
var cropX;
var cropY;
var cropWidth;
var cropHeight;
let b64Encoded;
let serialid;
const imageForm = document.getElementById("uplaodpfpform");
const csrf = document.getElementById("csrfmiddlewaretoken");
let serialofpost;
let vidsize;
let serialofmorebutton;
const MAX_WIDTH = 150;
const MAX_HEIGHT = 150;
const MIME_TYPE = "image/jpeg";
const QUALITY = 0.7;
var tobesenttoserver;
var globalblobimage;
var IMAGE_WIDTH;
var IMAGE_HEIGHT;

$(document).ready(function () {
    $(".profilepagefootercontentssubsection").bind("click", function () {
        var divs = $(".profilepagefootercontentssubsection");
        var i = divs.index($(this));
        if (document.getElementsByClassName("profilepagefootercontentssubsectioncrossbutton")[i].style.display != "flex") {
            if (document.getElementsByClassName("profilepagefootercontentssubsectionpostsmasterdiv")[i].style.display == "flex") {
                document.getElementsByClassName("profilepagefootercontentssubsectionheaderminussign")[i].style.display = "none";
                document.getElementsByClassName("profilepagefootercontentssubsectionheaderplussign")[i].style.display = "block";
                document.getElementsByClassName("profilepagefootercontentssubsectionpostsmasterdiv")[i].style.display = "none";
            } else {
                document.getElementsByClassName("profilepagefootercontentssubsectionheaderminussign")[i].style.display = "block";
                document.getElementsByClassName("profilepagefootercontentssubsectionheaderplussign")[i].style.display = "none";
                document.getElementsByClassName("profilepagefootercontentssubsectionpostsmasterdiv")[i].style.display = "flex";
            }
        }
    });

    $(".profilepagefootercontentsubsectiondeleteattachments").bind("click", function () {
        var divs = $(".profilepagefootercontentsubsectiondeleteattachments");
        indexofdeletebutton = divs.index($(this));
        i = indexofdeletebutton;
        // $(".previewImg").cropper('destroy')
        $(".previewImg").eq(i).attr('src', '');
        $(".uploadedvideocontainer").eq(i).attr('src', '');
        document.getElementsByClassName("profilepagefootercontentsubsectionattachimagebutton")[i].style.display = "flex";
        document.getElementsByClassName("profilepagefootercontentsubsectiondeleteattachments")[i].style.display = "none";
        document.getElementsByClassName("uploadedvideocontainer")[i].style.display = "none";
        cropper.reset();
        cropper.destroy();
        cropper.clear();
        // document.getElementsByClassName("previewImg")[i].style.display = "none";
    });

    $(".profilepagefootercontentsubsectionattachimagebutton").bind("click", function () {
        var divs = $(".profilepagefootercontentsubsectionattachimagebutton");
        indexofuploadbutton = divs.index($(this));
    });

    $(".profilepagefootercontentssubsectioncrossbutton").bind("click", function () {
        var divs = $(".profilepagefootercontentssubsectioncrossbutton");
        serialid = divs.index($(this));
    });

    $(".profilepagefootercontentsubsectionpostbutton").bind("click", function () {
        var divs = $(".profilepagefootercontentsubsectionpostbutton");
        serialofpost = divs.index($(this));
        const csrf = document.getElementsByName('csrfmiddlewaretoken')
        const fd = new FormData()
        serialidpostthesubsection = document.getElementsByClassName("profilepagefootercontentssubsectionheadernumber")[serialofpost].innerHTML
        serialidpostthesubsection = String(serialidpostthesubsection).substring(10)
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        if (document.getElementsByClassName("previewImg")[serialofpost].getAttribute('src') != "") {
            var croppedimage = cropper.getCroppedCanvas({ fillColor: '#36393F' }).toDataURL("image/jpeg", 0.9);
            tobeappendedimgwidth = $(document.getElementsByClassName("previewImg")[serialofpost]).width()
            tobeappendedimgheight = $(document.getElementsByClassName("previewImg")[serialofpost]).height()
            tobeappended = isImageSizeValid(croppedimage)
            if (tobeappended == null) {
                alert("upload an image smaller than 15MB")
                return;
            }
            else {
                const img = new Image();
                img.src = croppedimage;
                img.onerror = function () {
                    URL.revokeObjectURL(this.src);
                    // Handle the failure properly
                    console.log("Cannot load image");
                };


                img.onload = function () {
                    URL.revokeObjectURL(this.src);
                    const [newWidth, newHeight] = calculateSize(img, MAX_WIDTH, MAX_HEIGHT);
                    const canvas = document.createElement("canvas");
                    canvas.width = newWidth;
                    canvas.height = newHeight;
                    const ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0, newWidth, newHeight);
                    canvas.toBlob(
                        (blob) => {
                            // Handle the compressed image. es. upload or save in local state
                            // displayInfo('Original file', file);
                            // displayInfo('Compressed file', blob);
                            var reader = new FileReader();
                            reader.readAsDataURL(blob);
                            reader.onloadend = function () {
                                tobesenttoserver = reader.result;
                                fd.append('post_image', tobesenttoserver)
                                fd.append('post_video', null)
                                fd.append('post_text', document.getElementsByClassName("profilepagefootercontentsubsectionedittablediv")[serialofpost].innerHTML)
                                fd.append('post_serial', serialidpostthesubsection)
                                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                                $.ajax({
                                    type: 'POST',
                                    url: 'addpost/',
                                    enctype: 'multipart/form-data',
                                    headers: {
                                        'X-CSRFToken': csrftoken
                                    },
                                    data: fd,
                                    cache: false,
                                    contentType: false,
                                    processData: false
                                })
                                    .done(function (data) { reloadpage() })
                            }
                        },
                        MIME_TYPE,
                        QUALITY
                    );
                };
            }
        }
        else if (document.getElementsByClassName("uploadedvideocontainer")[serialofpost].getAttribute('src') != null) {
            if (vidsize >= (24 * 1024 * 1024)) {
                alert("upload a video smaller than 24MB")
                return;
            }
            else {
                vidfile = $('#fileInput')[0].files[0];
                fd.append('post_video', vidfile)
                fd.append('post_image', null)
                fd.append('post_serial', serialidpostthesubsection)
                fd.append('post_text', document.getElementsByClassName("profilepagefootercontentsubsectionedittablediv")[serialofpost].innerHTML)
                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                $.ajax({
                    type: 'POST',
                    url: 'addpost/',
                    enctype: 'multipart/form-data',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: fd,
                    cache: false,
                    contentType: false,
                    processData: false
                })
                    .done(function (data) { reloadpage() })
                    .fail(function () { alert("Post Failed"); });
            }
        }
        else {
            fd.append('post_video', null)
            fd.append('post_image', null)
            fd.append('post_serial', serialidpostthesubsection)
            fd.append('post_text', document.getElementsByClassName("profilepagefootercontentsubsectionedittablediv")[serialofpost].innerHTML)
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            $.ajax({
                type: 'POST',
                url: 'addpost/',
                enctype: 'multipart/form-data',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: fd,
                cache: false,
                contentType: false,
                processData: false
            })
                .done(function (data) { reloadpage() })
                .fail(function () { alert("Post Failed"); });
        }
    });

    $(".profilepagefootercontentsubsectionattachimagebutton").bind("click", function () {
        var divs = $(".profilepagefootercontentsubsectionattachimagebutton");
        serialofpost = divs.index($(this));
    });

    $(".profilepagefootercontentssubsectionsubmittedpostschildrendivbuttondivbutton").bind("click", function () {
        var divs = $(".profilepagefootercontentssubsectionsubmittedpostschildrendivbuttondivbutton");
        serialofmorebutton = divs.index($(this));
        posthash = document.getElementsByClassName("profilepagefootercontentssubsectionsubmittedpoststimedivhash")[serialofmorebutton].innerHTML
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: 'POST',
            url: 'delete_post/',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'posthash': posthash,
            },
        })
            .done(function (data) { reloadpage(); })
            .fail(function () { alert("Delete failed") });
    });

    //For Card Number formatted input
    var cardNum = document.getElementById('cr_no');
    cardNum.onkeyup = function (e) {
        if (this.value == this.lastValue) return;
        var caretPosition = this.selectionStart;
        var sanitizedValue = this.value.replace(/[^0-9]/gi, '');
        var parts = [];

        for (var i = 0, len = sanitizedValue.length; i < len; i += 4) {
            parts.push(sanitizedValue.substring(i, i + 4));
        }

        for (var i = caretPosition - 1; i >= 0; i--) {
            var c = this.value[i];
            if (c < '0' || c > '9') {
                caretPosition--;
            }
        }
        caretPosition += Math.floor(caretPosition / 4);

        this.value = this.lastValue = parts.join(' ');
        this.selectionStart = this.selectionEnd = caretPosition;
    }

    //For Date formatted input
    var expDate = document.getElementById('exp');
    expDate.onkeyup = function (e) {
        if (this.value == this.lastValue) return;
        var caretPosition = this.selectionStart;
        var sanitizedValue = this.value.replace(/[^0-9]/gi, '');
        var parts = [];

        for (var i = 0, len = sanitizedValue.length; i < len; i += 2) {
            parts.push(sanitizedValue.substring(i, i + 2));
        }

        for (var i = caretPosition - 1; i >= 0; i--) {
            var c = this.value[i];
            if (c < '0' || c > '9') {
                caretPosition--;
            }
        }
        caretPosition += Math.floor(caretPosition / 2);

        this.value = this.lastValue = parts.join('/');
        this.selectionStart = this.selectionEnd = caretPosition;
    }
});

function previewFile() {
    i = indexofuploadbutton;
    var file = $("input[type=file]").get(0).files[0];
    if (file) {
        document.getElementsByClassName("profilepagefootercontentsubsectiondeleteattachments")[i].style.display = "block";
        document.getElementsByClassName("profilepagefootercontentsubsectionattachimagebutton")[i].style.display = "none";
        const fileType = file['type'];
        const validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];
        if (validImageTypes.includes(fileType)) { // if image uploaded
            const reader = new FileReader();
            reader.onload = function (e) {
                var image = e.target.result;
                imageField = document.getElementsByClassName("previewImg")[i];
                document.getElementsByClassName("profilepagefootercontentsubsectiondeleteattachments")[i].style.display = "block";
                document.getElementsByClassName("profilepagefootercontentsubsectionattachimagebutton")[i].style.display = "none";
                imageField.src = image;
                imageFile = image;
                var startIndex = image.indexOf("base64,") + 7
                var base64str = image.substr(startIndex)
                var decoded = atob(base64str)
                cropper = new Cropper(imageField, {
                    aspectRatio: 4 / 5,
                    zoomable: false,
                    // background: false,
                    // viewMode: 1,
                    crop(event) {
                        event.stopPropagation();
                        event.preventDefault(); //Most important
                        console.log("CROP START");
                        console.log("x: " + event.detail.x);
                        console.log("y: " + event.detail.y);
                        console.log("width: " + event.detail.height);
                        console.log("height: " + event.detail.width);
                        // setImageCropProperties(
                        //     image,
                        //     event.detail.x,
                        //     event.detail.y,
                        //     event.detail.width,
                        //     event.detail.height
                        // )
                    }
                })
            };
            reader.readAsDataURL(file);
        } else { // if video uploaded
            vidsize = file.size;
            let blobURL = URL.createObjectURL(file);
            $(".uploadedvideocontainer").eq(i).css("display", "block");
            $(".uploadedvideocontainer").eq(i).attr("src", blobURL);
            // document.querySelector("video")[i].src = blobURL;
        }
    }
}

function opencloseeditprofile() {
    console.log($(window).width())
    if($(window).width()<450){
        document.getElementById("profilepageheaderfollowers").style.display="none";
        document.getElementById("profilepageheadersubscriptionfeeandinputdiv").style.justifyContent="flex-start";
        document.getElementById("profilepageheadersubscriptionfeeandinputdiv").style.width="160px";
    }
    var fee = document.getElementById("profilepageheadersubscriptionfeebold").innerHTML.substring(1);
    screendiv = document.getElementById("screen")
    document.getElementById("profilepageheadercanceleditbutton").style.display = "flex";
    document.getElementById("profilepageheaderaddsectionbutton").style.display = "none";
    // document.getElementById("profilepageheadersubscribebutton").style.display = "none";
    // document.getElementById("profilepageheadermessagebutton").style.display = "none";
    document.getElementById("profileheaderseemorebutton").style.display = "none";
    document.getElementById("addsectionpopupsubdivsselect").style.display = "block";
    element = document.getElementById("profilepageheaderinfoarea");
    document.getElementById("profilepageheaderinfoareaedit").innerHTML = document.getElementById("profilepageheaderinfoarea").innerHTML;
    document.getElementById("profilepageheaderinfoarea").style.display = "none";
    document.getElementById("profilepageheadereditprofilebutton").style.display = "none";
    document.getElementById("profilepageheadersaveprofilebutton").style.display = "flex";
    document.getElementById("profilepageheaderinfoareaedit").style.display = "block";
    document.getElementById("profilepageheadersubscriptionfee").style.display = "none";
    document.getElementById("profilepageheadersubscriptionfeeedit").style.display = "flex";
    document.getElementById("profilepageheadersubscriptionfeeeditinput").value = fee;
    document.getElementById("profileheaderseemorebutton").style.visibility = "hidden";
    document.getElementById("profilepageheaderusernameeditdiv").style.display = "flex";
    document.getElementById("profilepageheaderusernameedit").value = document.getElementById("profilepageheaderusername").innerHTML.substring(1);
    document.getElementById("addsectionpopupsubdivsselect").style.display = "block";
    document.getElementById("profilepageheaderusername").style.display = "none";

    timezoneval = document.getElementById("editprofiletimezoneedittexts").innerHTML;
    selectedvar = document.getElementById("addsectionpopupsubdivsselect");
    selectedvar.value = timezoneval.substring(18);
    timezonetext = timezoneval.substring(0, 18);
    document.getElementById("editprofiletimezoneedittexts").innerHTML = timezonetext;

    var headerheight = document.getElementById('profilepageheader').clientHeight;
    var footerheight = document.getElementById('profilepagefooter').clientHeight;
    var newheight = String(headerheight) + 'px';
    var newheight2 = String(footerheight) + 'px';
    document.getElementById("dimscreenoverfooter").style.visibility = "visible";
    document.getElementById("dimscreenoverfooter").style.top = newheight;
    document.getElementById("dimscreenoverfooter").style.height = newheight2;
    screendiv.scrollTo(0, 0);
    document.getElementById("profilepageheaderinfoareaedit").addEventListener("input", function () {
        var headerheight = document.getElementById('profilepageheader').clientHeight;
        var footerheight = document.getElementById('profilepagefooter').clientHeight;
        var newheight = String(headerheight) + 'px';
        var newheight2 = String(footerheight) + 'px';
        document.getElementById("dimscreenoverfooter").style.visibility = "visible";
        document.getElementById("dimscreenoverfooter").style.top = newheight;
        document.getElementById("dimscreenoverfooter").style.height = newheight2;
    }, false);
}

function isOverflown(element) {
    if (element.scrollHeight > element.clientHeight) {
        document.getElementById("profileheaderseemorebutton").style.visibility = "visible";
        document.getElementById("profilepagefootercontentseemoredescriptionbutton").style.visibility = "visible";
    } else {
        document.getElementById("profileheaderseemorebutton").style.visibility = "hidden";
        document.getElementById("profilepagefootercontentseemoredescriptionbutton").style.visibility = "hidden";
    }
}

function closeprofilemorebuttonpop() {
    document.getElementById("dimscreen3").style.visibility = "hidden";
    document.getElementById("moreprofileoptionspopup").style.display = "none";
}

function openprofilemorebuttonpopup() {
    document.getElementById("dimscreen3").style.visibility = "visible";
    document.getElementById("moreprofileoptionspopup").style.display = "flex";
}

function seemoreinfo() {
    screendiv = document.getElementById("screen")
    if (document.getElementById("profileheaderseemorebutton").innerHTML == "See more") {
        document.getElementById("profilepageheaderinfoarea").style.maxHeight = "none";
        document.getElementById("profileheaderseemorebutton").innerHTML = "See less";
        screendiv.scrollTo(0, 0);
    } else {
        document.getElementById("profilepageheaderinfoarea").style.maxHeight = "100px";
        document.getElementById("profileheaderseemorebutton").innerHTML = "See more";
        screendiv.scrollTo(0, 0);
    }
}

function openaddsectiondiv() {
    screendiv = document.getElementById("screen")
    document.getElementById("addsectionpopup").style.display = "flex";
    document.getElementById("dimscreen3").style.visibility = "visible";
    screendiv.scrollTo(0, 0);
}

function closeaddsectionpopup() {
    document.getElementById("addsectionpopup").style.display = "none";
    document.getElementById("dimscreen3").style.visibility = "hidden";
}

function seemoredescription() {
    if (document.getElementById("profilepagefootercontentseemoredescriptionbutton").innerHTML == "See more") {
        document.getElementById("profilepagefootercontentsdescriptioninfo").style.maxHeight = "none";
        document.getElementById("profilepagefootercontentseemoredescriptionbutton").innerHTML = "See less";
    } else {
        document.getElementById("profilepagefootercontentsdescriptioninfo").style.maxHeight = "100px";
        document.getElementById("profilepagefootercontentseemoredescriptionbutton").innerHTML = "See more";
    }
}

function editsectionfunc() {
    var headerheight = document.getElementById('profilepageheader').clientHeight;
    var footerheaderheight = document.getElementById('profilepagefooterheadings').clientHeight;
    var newheight = String(footerheaderheight + headerheight) + 'px';
    document.getElementById("dimscreenoverheader").style.visibility = "visible";
    document.getElementById("dimscreenoverheader").style.height = newheight;

    document.getElementById("profilepagefootertopbuttonsaddsubsectionbutton").style.display = "none";
    document.getElementById("profilepagefootercontentssectionviewabletotext").style.display = "none";
    document.getElementById("profilepagefootertopcanceleditbutton").style.display = "flex";
    document.getElementById("profilepagefootertopbuttonsdeletesectionbutton").style.display = "flex";
    document.getElementById("profilepagefootercontentsviewableselectandrenamesectionmasterdiv").style.display = "flex";

    document.getElementById("profilepagefootertopbuttonseditsectionbutton").style.display = "none";
    document.getElementById("profilepagefootercontentseemoredescriptionbutton").style.visibility = "hidden";
    document.getElementById("profilepagefooterdescriptionareaedit").style.display = "block";
    document.getElementById("profilepagefootertopbuttonssavechangesbutton").style.display = "flex";
    document.getElementById("profilepagefooterdescriptionareaedit").innerHTML = document.getElementById("profilepagefootercontentsdescriptioninfo").innerHTML;
    document.getElementById("profilepagefootercontentsdescriptioninfo").style.display = "none";
    console.log(document.getElementById("profilepagefootercontentssectiontitle").innerHTML)
    document.getElementById("profilepagefootercontentsviewableselectchilddivinput").value = document.getElementById("profilepagefootercontentssectiontitle").innerHTML
    var elements = document.getElementsByClassName('profilepagefootercontentssubsectioncrossbutton');
    for (var i = 0; i < elements.length; i++) {
        document.getElementsByClassName("profilepagefootercontentssubsectioncrossbutton")[i].style.display = "flex";
    }

    var elements = document.getElementsByClassName('profilepagefootercontentssubsectionpostsmasterdiv');
    for (var i = 0; i < elements.length; i++) {
        document.getElementsByClassName("profilepagefootercontentssubsectionpostsmasterdiv")[i].style.display = "none";
    }

    var elements = document.getElementsByClassName('profilepagefootercontentssubsectionheaderminussign');
    for (var i = 0; i < elements.length; i++) {
        document.getElementsByClassName("profilepagefootercontentssubsectionheaderminussign")[i].style.display = "none";
        document.getElementsByClassName("profilepagefootercontentssubsectionheaderplussign")[i].style.display = "block";
    }

    viewableto = document.getElementById("profilepagefootercontentssectionviewabletotextbold").innerHTML;
    selectedvar = document.getElementById("profilepagefootercontentsviewableselect");
    console.log(viewableto)
    selectedvar.value = viewableto;
    if(!document.getElementById('profilepagefootercontentsdescriptionheadingtext').textContent.includes('Section Description')){
        document.getElementById('profilepagefootercontentsdescriptionheadingtextspan').innerHTML="Section Description";
    }
}

function deletesection() {
    document.getElementById("dimscreen3").style.visibility = "visible";
    document.getElementById("confirmdeletesection").style.display = "flex";
    screendiv = document.getElementById("screen")
    screendiv.scrollTo(0, 0);
    document.getElementById("deletesectionwarning").style.display = "block";
    document.getElementById("deletesubsectionwarning").style.display = "none";
    document.getElementById("yesimsuredeletesecbutton").style.display = "block";
    document.getElementById("yesimsuredeletesecbutton2").style.display = "none";
}

function deletesubsection() {
    document.getElementById("dimscreen3").style.visibility = "visible";
    document.getElementById("confirmdeletesection").style.display = "flex";
    screendiv = document.getElementById("screen")
    screendiv.scrollTo(0, 0);
    document.getElementById("deletesectionwarning").style.display = "none";
    document.getElementById("deletesubsectionwarning").style.display = "block";
    document.getElementById("yesimsuredeletesecbutton").style.display = "none";
    document.getElementById("yesimsuredeletesecbutton2").style.display = "block";
}

function closeconfirmdeletesection() {
    document.getElementById("dimscreen3").style.visibility = "hidden";
    document.getElementById("confirmdeletesection").style.display = "none";
}

function profilesetuppopup() {
    screendiv = document.getElementById("screen")
    screendiv.scrollTo(0, 0);
    document.getElementById("helpsetupprofilepopup").style.display = "flex";
    document.getElementById("dimscreen3").style.visibility = "visible";
}

function reloadpage() {
    location.reload();
}

function closeprofilesetuphelppopup() {
    document.getElementById("helpsetupprofilepopup").style.display = "none";
    document.getElementById("dimscreen3").style.visibility = "hidden";
}

function copytoclipboard() {
    navigator.clipboard.writeText(window.location.href);
}

function submiteditsection() {
    document.getElementById("profilepagefootercontentsdescriptioninfotextarea").value = document.getElementById("profilepagefooterdescriptionareaedit").innerHTML;
    document.getElementById('editsectionform').submit();
}

function submitallforms() {
    document.getElementById("my-textarea").value = document.getElementById("profilepageheaderinfoareaedit").innerHTML;
    document.getElementById('savechangesform').submit();
}

function closedisplayuploadedprofilepic() {
    location.reload();
    document.getElementById("displayuploadedprofilepic").style.display = "none";
    document.getElementById("dimscreen3").style.visibility = "hidden";
    clearInputFile(document.getElementById("profilepicinput"));
}

function cropprofilepicture() {
    screendiv = document.getElementById("screen")
    screendiv.scrollTo(0, 0);
    imgInp = document.getElementById("profilepicinput");
    const [file] = imgInp.files;
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            var image = e.target.result;
            imageField = document.getElementById("displayuploadedprofilepiccontainer");
            document.getElementById("dimscreen3").style.visibility = "visible";
            imageField.src = image;
            imageFile = image;
            var startIndex = image.indexOf("base64,") + 7
            var base64str = image.substr(startIndex)
            var decoded = atob(base64str)
            document.getElementById("displayuploadedprofilepic").style.display = "flex";
            document.getElementById("displayuploadedprofilepic").style.transform = "translate(-50%,-50%)";
            cropper = new Cropper(imageField, {
                aspectRatio: 1 / 1,
                zoomable: false,
                viewMode: 1,
                crop(event) {
                    event.stopPropagation();
                    event.preventDefault(); //Most important
                    console.log("CROP START");
                    console.log("x: " + event.detail.x);
                    console.log("y: " + event.detail.y);
                    console.log("width: " + event.detail.height);
                    console.log("height: " + event.detail.width);
                    // setImageCropProperties(
                    //     image,
                    //     event.detail.x,
                    //     event.detail.y,
                    //     event.detail.width,
                    //     event.detail.height
                    // )
                }
            })
        };
        reader.readAsDataURL(file);
    }
}

function saveuploadedprofilepic() {
    checker = isImageSizeValid1(imageFile)
    let tobesenttoserver;
    var croppedimage = cropper.getCroppedCanvas().toDataURL("image/jpeg", 0.9);
    if (checker != null) {
        // const blobURL = URL.createObjectURL(croppedimage);
        const img = new Image();
        img.src = croppedimage;
        img.onerror = function () {
            URL.revokeObjectURL(this.src);
            // Handle the failure properly
            console.log("Cannot load image");
        };

        img.onload = function () {
            URL.revokeObjectURL(this.src);
            const [newWidth, newHeight] = calculateSize1(img, MAX_WIDTH, MAX_HEIGHT);
            const canvas = document.createElement("canvas");
            canvas.width = newWidth;
            canvas.height = newHeight;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, newWidth, newHeight);
            canvas.toBlob(
                (blob) => {
                    // Handle the compressed image. es. upload or save in local state
                    // displayInfo('Original file', file);
                    // displayInfo('Compressed file', blob);
                    var reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = function () {
                        tobesenttoserver = reader.result;
                        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                        $.ajax({
                            type: 'POST',
                            url: 'crop_image/',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                            data: {
                                'image': tobesenttoserver,
                            },
                        })
                    }
                },
                MIME_TYPE,
                QUALITY
            );
        };
    }
    else {
        alert("Upload an image smaller than 15MB")
    }
    reloadpage()
}

function isImageSizeValid1(image) {
    var startIndex = image.indexOf("base64,") + 7
    var base64str = image.substr(startIndex)
    var decoded = atob(base64str)
    if (decoded.length >= (15 * 1024 * 1024)) {
        return null
    }
    else {
        return image
    }
}

function isImageSizeValid(image) {
    var startIndex = image.indexOf("base64,") + 7
    var base64str = image.substr(startIndex)
    var decoded = atob(base64str)
    if (decoded.length >= (15 * 1024 * 1024)) {
        return null
    }
    else {
        return image
    }
}

function deletesubsectionfunc() {
    wannadelsubsection = document.getElementsByClassName("profilepagefootercontentssubsectionheadernumber")[serialid];
    wannadelsubsectionhtml = String(wannadelsubsection.innerHTML);
    serialidoftobedeletedsubsec = wannadelsubsectionhtml.substring(10);
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: 'POST',
        url: 'deletesubsection/',
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            'serialid': serialidoftobedeletedsubsec,
        },
    })
        .done(function (data) { reloadpage() })
        .fail(function () { alert("Delete Failed"); });
}


function calculateSize(img, maxWidth, maxHeight) {
    let width = img.width;
    let height = img.height;

    // calculate the width and height, constraining the proportions
    if (width > height) {
        if (width > maxWidth) {
            height = Math.round((height * maxWidth) / width) * 7;
            width = maxWidth * 7;
        }
    } else {
        if (height > maxHeight) {
            width = Math.round((width * maxHeight) / height) * 7;
            height = maxHeight * 7;
        }
    }
    return [width, height];
}

function calculateSize1(img, maxWidth, maxHeight) {
    let width = img.width;
    let height = img.height;

    // calculate the width and height, constraining the proportions
    if (width > height) {
        if (width > maxWidth) {
            height = Math.round((height * maxWidth) / width);
            width = maxWidth;
        }
    } else {
        if (height > maxHeight) {
            width = Math.round((width * maxHeight) / height);
            height = maxHeight;
        }
    }
    return [width, height];
}

function getCanvasBlob(canvas) {
    return new Promise(function (resolve, reject) {
        canvas.toBlob(function (blob) {
            resolve(blob)
        })
    })
}


function openfollowuserpopup() {
    document.getElementById("dimscreen3").style.visibility = "visible";
    document.getElementById("paytofollowpopupmasterdiv").style.display = "flex";
}

function closefollowuserpopup() {
    document.getElementById("dimscreen3").style.visibility = "hidden";
    document.getElementById("paytofollowpopupmasterdiv").style.display = "none";
}

document.addEventListener('DOMContentLoaded', () => {
    bioarea = document.getElementById("profilepageheaderinfoarea");
    if (bioarea.scrollHeight > bioarea.clientHeight) {
        document.getElementById("profileheaderseemorebutton").style.display = "block";
    }
    else {
        document.getElementById("profileheaderseemorebutton").style.display = "none";
    }

    descarea = document.getElementById("profilepagefootercontentsdescriptioninfo");
    if (descarea.scrollHeight > descarea.clientHeight) {
        document.getElementById("profilepagefootercontentseemoredescriptionbutton").style.display = "block";
    }
    else {
        document.getElementById("profilepagefootercontentseemoredescriptionbutton").style.display = "none";
    }

});

document.addEventListener('DOMContentLoaded', () => {
    limit(document.getElementById("profilepageheadersubscriptionfeeeditinput"))
    function limit(element)
    {
        var max_chars = 3;
    
        if(element.value.length > max_chars) {
            element.value = element.value.substr(0, max_chars);
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    var convert = function (convert) {
        return $("<span />", { html: convert }).text();
        //return document.createElement("span").innerText;
    };

    sub = document.getElementById("profilepageheaderinfoarea").innerHTML
    sub2 = convert(sub)
    document.getElementById("profilepageheaderinfoarea").innerHTML = sub2.replace("<div><br></div>", "<br>");

    sub3 = document.getElementById("profilepagefootercontentsdescriptioninfo").innerHTML
    sub4 = convert(sub3)
    document.getElementById("profilepagefootercontentsdescriptioninfo").innerHTML = sub4.replace("<div><br></div>", "<br>");

    for (var i = 0; i < document.getElementsByClassName("profilepagefootercontentssubsectionsubmittedpostschildrendivchildrentext").length; i++) {
        str = document.getElementsByClassName("profilepagefootercontentssubsectionsubmittedpostschildrendivchildrentext")[i].innerHTML;
        str2 = convert(str)
        document.getElementsByClassName("profilepagefootercontentssubsectionsubmittedpostschildrendivchildrentext")[i].innerHTML = str2.replace("<div><br></div>", "<br>");
    }
});

document.addEventListener('DOMContentLoaded', () => {
    for (var i = 0; i < document.getElementsByClassName("profilepagefootercontentsubsectionedittablediv").length; i++) {
        var text = document.getElementsByClassName('profilepagefootercontentsubsectionedittablediv')[i];
        function resize() {
            text.style.height = 'auto';
            text.style.height = text.scrollHeight + 'px';
        }
        /* 0-timeout to get the already changed text */
        function delayedResize() {
            window.setTimeout(resize, 0);
        }
        observe(text, 'change', resize);
        observe(text, 'cut', delayedResize);
        observe(text, 'paste', delayedResize);
        observe(text, 'drop', delayedResize);
        observe(text, 'keydown', delayedResize);

        text.focus();
        text.select();
        resize();
    }
});

var observe;
if (window.attachEvent) {
    observe = function (element, event, handler) {
        element.attachEvent('on' + event, handler);
    };
}
else {
    observe = function (element, event, handler) {
        element.addEventListener(event, handler, false);
    };
}

document.addEventListener('DOMContentLoaded', () => {
    const yesyesterday = JSON.parse(document.getElementById('yesyesterday').textContent);
    if (yesyesterday == true) {
        alert("Add a new post-area so you can create posts inside it.")
    }
});

document.addEventListener('DOMContentLoaded', () => {
    var str = document.getElementById('profilepagefootercontentsdescriptionheadingtext').innerHTML;
    if(!str.replace(/\s/g, '').length) {
        document.getElementById("profilepagefootercontentsdescriptionheadingtext").style.display="none";
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const sectionname = document.getElementById("profilepagefootercontentssectiontitle").innerHTML;
    for (var i = 0; i < document.getElementsByClassName("profilepagefootersectionsbuttons").length; i++) {

        if (sectionname == document.getElementsByClassName("profilepagefootersectionsbuttons")[i].innerHTML) {

            document.getElementsByClassName("profilepagefootersectionsbuttons")[i].style.background = '#42464D';
            document.getElementsByClassName("profilepagefootersectionsbuttons")[i].style.padding = '5px';
            document.getElementsByClassName("profilepagefootersectionsbuttons")[i].style.fontWeight = 'bold';
        }
    }
    document.getElementsByClassName("profilepagefootercontentssubsectionpostsmasterdiv")[0].style.display = "flex";
    document.getElementsByClassName("profilepagefootercontentssubsectionheaderplussign")[0].style.display = "none";
    document.getElementsByClassName("profilepagefootercontentssubsectionheaderminussign")[0].style.display = "block";
});

document.addEventListener('DOMContentLoaded', () => {
    const publishablekey = JSON.parse(document.getElementById('publishablekey').textContent);
    const checkout_session = JSON.parse(document.getElementById('checkout_session').textContent);
    var stripe = Stripe(publishablekey);
    var elements = stripe.elements();
    var card = elements.create('card', {
        style: {
            base: {
                iconColor: '#c4f0ff',
                color: '#FFFFFF',
                fontSmoothing: 'antialiased',
                ':-webkit-autofill': {
                    color: '#fce883',
                },
            },
            invalid: {
                iconColor: '#FFC7EE',
                color: '#FFC7EE',
            },
        },
    });
    card.mount('#cardinput');
    const paymentform = document.getElementById('payment-form');
    paymentform.addEventListener('submit', async (event) => {
        event.preventDefault();
        document.getElementById("confirmpaymentfollowbutton").style.backgroundColor = "#1d786a";
        document.getElementById("confirmpaymentfollowbutton").disabled = true;
        document.getElementById("confirmpaymentfollowbutton").style.cursor = "default";
        document.getElementById("confirmpaymentfollowbuttonspinner").style.display = "block";
        document.getElementById("confirmpaymentfollowbuttontext").style.display = "none";
        document.getElementById('card-errors').textContent = "";
        stripe.createToken(card).then(function (result) {
            if (result.error) {
                // Inform the customer that there was an error.
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
                document.getElementById("confirmpaymentfollowbutton").style.backgroundColor = "#29ab97";
                document.getElementById("confirmpaymentfollowbutton").disabled = false;
                document.getElementById("confirmpaymentfollowbuttonspinner").style.display = "none";
                document.getElementById("confirmpaymentfollowbuttontext").style.display = "block";
                document.getElementById("confirmpaymentfollowbutton").style.cursor = "pointer";
            } else {
                // Send the token to your server.
                stripeTokenHandler(result.token);
            }
        });
    });
    function stripeTokenHandler(token) {
        // Insert the token ID into the form so it gets submitted to the server
        var paymentform = document.getElementById('payment-form');
        var hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeToken');
        hiddenInput.setAttribute('value', token.id);
        paymentform.appendChild(hiddenInput);

        // Submit the form
        paymentform.submit();
    }
});

function openunfollowwarning() {
    document.getElementById("unfollowpopupmasterdiv").style.display = "flex";
    document.getElementById("dimscreen3").style.visibility = "visible";
}

function closeunfollowwarning() {
    document.getElementById("unfollowpopupmasterdiv").style.display = "none";
    document.getElementById("dimscreen3").style.visibility = "hidden";
}

function closeprofilesetuphelppopup2(){
    document.getElementById("helpsetupprofilepopup2").style.display="none";
    document.getElementById("dimscreen3").style.visibility = "hidden";
}

function openprofilesetuphelppopup2(){
    document.getElementById("helpsetupprofilepopup2").style.display="flex";
    document.getElementById("dimscreen3").style.visibility = "visible";
}