let usernames = [];

$(document).ready(function () {
    $("#mysearchchatinput").keyup(function () {
        var input = $(this).val().toLowerCase();
        if (input != "") {
            var x = document.getElementsByClassName("contactspot");
            for (var i = 0; i < x.length; i++) {
                document.getElementsByClassName("contactspot")[i].style.display = "none";
            }
            input = '@' + input;
            const isVisible = usernames.includes(input)
            if (isVisible == true) {
                var buttons = document.getElementsByClassName('contactname')
                i = 0;
                found = false
                do {
                    currentusernameinarr = buttons[i].innerHTML;
                    if (currentusernameinarr == input) {
                        found = true
                    }
                    if (found == false) {
                        i = i + 1;
                    }
                }
                while (found == false);
                document.getElementsByClassName("contactspot")[i].style.display = "flex";
            }
        }
        else {
            var x = document.getElementsByClassName("contactspot");
            for (var i = 0; i < x.length; i++) {
                document.getElementsByClassName("contactspot")[i].style.display = "flex";
            }
        }
    })
});

function messagesearchopen() {
    document.getElementById("crossimagebutton").style.visibility = "visible";
    document.getElementById("mysearchchatinput").style.display = "block";
    document.getElementById("messagestext").style.display = "none";
}

function messagesearchcollapse() {
    document.getElementById("messagestext").style.display = "block";
    document.getElementById("mysearchchatinput").style.display = "none";
    document.getElementById("crossimagebutton").style.visibility = "hidden";
    var x = document.getElementsByClassName("contactspot");
    for (var i = 0; i < x.length; i++) {
        document.getElementsByClassName("contactspot")[i].style.display = "flex";
    }
}

function closemorebuttonpop() {
    document.getElementById("dimscreen1").style.visibility = "hidden";
    document.getElementById("mymorebuttonpopup").style.visibility = "hidden";
}

function openmorebuttonpop() {
    document.getElementById("dimscreen1").style.visibility = "visible";
    document.getElementById("mymorebuttonpopup").style.visibility = "visible";
}

function startconversation() {
    let query = window.matchMedia("(max-width: 1023px)");
    // const otheruser=JSON.parse(document.getElementById("other-user"))
    // usercontains=false;
    // if (otheruser != null){
    //     usercontains=true;
    // }
    // else{
    //     usercontains=false;
    // }
    if (query.matches) {
        // mobile
        setTimeout(() => {
            document.getElementById("myinfoarea").style.visibility = "hidden";
            document.getElementById("myinfoarea").style.display = "none";
            document.getElementById("mymessagesarea").style.visibility = "visible";
            document.getElementById("mymessagesarea").style.display = "flex";
            document.getElementById("mymessageinputdiv").style.visibility = "visible";
            // document.getElementById("mymessagespace").style.visibility = "visible";
            document.getElementById("mymessageareaheader").style.visibility = "visible";
        }, 100);
    }
    else {
        // desktop
        setTimeout(() => {
            document.getElementById("mymessageinputdiv").style.visibility = "visible";
            // document.getElementById("mymessagespace").style.visibility = "visible";
            document.getElementById("mymessageareaheader").style.visibility = "visible";
            // document.getElementById("nochatselected").innerHTML = "";
            // document.getElementById("myclientmessages").style.display = "block";
        }, 100);
    }
}

function backtoconversations() {
    document.getElementById("myinfoarea").style.visibility = "visible";
    document.getElementById("myinfoarea").style.display = "flex";
    document.getElementById("mymessagesarea").style.visibility = "hidden";
    document.getElementById("mymessagesarea").style.display = "none";
    document.getElementById("mymessageinputdiv").style.visibility = "hidden";
    document.getElementById("mymessagespace").style.visibility = "hidden";
    document.getElementById("mymessageareaheader").style.visibility = "hidden";
    document.getElementById("myusernamemessageareaheaderlink").textContent = "";
}

setTimeout(() => {
    var buttons = document.querySelectorAll('.contactsarea button')
    for (var i = 0; i < buttons.length; i++) {
        contactusername = document.getElementsByClassName("contactname")[i].innerHTML;
        usernames.push(contactusername);
    }
    screendiv = document.getElementById("mymessagespace");
    screendiv.scrollTop = screendiv.scrollHeight;
}, 100);

setTimeout(() => {
    const id = JSON.parse(document.getElementById('other-user-id').textContent);
    const myusername = JSON.parse(document.getElementById('myusername').textContent)
    let form = document.getElementById("sendmessageform");
    // let url = 'ws://' + window.location.host + '/ws/' + id + '/'
    // let form = document.getElementById("sendmessageform")
    // const chatSocket = new WebSocket(url)

    // chatSocket.onopen = function (e) {
    //     console.log("connection established")
    // }

    // chatSocket.onmessage = function (e) {
    //     let data = JSON.parse(e.data)
    //     if (data.username == myusername) {
    //         let messages = document.getElementById('mymessagespace');
    //         let newmsg = document.createElement('div');
    //         newmsg.innerHTML = data.message;
    //         newmsg.setAttribute("id", "messagesmy");
    //         messages.appendChild(newmsg);
    //         screendiv = document.getElementById("mymessagespace")
    //         screendiv.scrollTop = screendiv.scrollHeight;
    //     }
    //     else {
    //         let messages = document.getElementById('mymessagespace');
    //         let newmsg = document.createElement('div');
    //         newmsg.innerHTML = data.message;
    //         newmsg.setAttribute("id", "messagesreceived");
    //         messages.appendChild(newmsg);
    //         screendiv = document.getElementById("mymessagespace")
    //         screendiv.scrollTop = screendiv.scrollHeight;
    //     }
    // }

    // form.addEventListener('submit', (e) => {
    //     e.preventDefault()
    //     if (/\S/.test(document.getElementById("mymessageinput").value)) {
    // let message = e.target.message.value
    // chatSocket.send(JSON.stringify({
    //     'message': message,
    //     'username': myusername
    // }));
    //     }
    //     form.reset();
    // })
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (/\S/.test(document.getElementById("mymessageinput").value)) {
            $.ajax({
                type: 'POST',
                url: 'sendmessage/',
                data: {
                    message: $('#mymessageinput').val(),
                    myusername: myusername,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (data) {
                    // if (data.username == myusername) {
                    //     let messages = document.getElementById('mymessagespace');
                    //     let newmsg = document.createElement('div');
                    //     newmsg.innerHTML = data.message;
                    //     newmsg.setAttribute("id", "messagesmy");
                    //     messages.appendChild(newmsg);
                    //     screendiv = document.getElementById("mymessagespace")
                    //     screendiv.scrollTop = screendiv.scrollHeight;
                    // }
                }

            })
        }
        form.reset();
    })
}, 100);

setInterval(function () {
    const myusername = JSON.parse(document.getElementById('myusername').textContent)
    const check=isScrolledToBottom(document.getElementById('mymessagespace'));
    if (check==true){
        $.ajax({
            type: 'GET',
            url: 'getmessages/',
            success: function (response) {
                var el = document.getElementById('mymessagespace');
                while (el.firstChild) el.removeChild(el.firstChild);
                for (let [key, data] of Object.entries(response)) {
                    for (var i = data.length-1; i > -1; i--) {
                        if (data[i].sender == myusername) {
                            let messages = document.getElementById('mymessagespace');
                            let newmsg = document.createElement('div');
                            newmsg.innerHTML = data[i].message;
                            newmsg.setAttribute("id", "messagesmy");
                            messages.appendChild(newmsg);
                        }
                        else {
                            let messages = document.getElementById('mymessagespace');
                            let newmsg = document.createElement('div');
                            newmsg.innerHTML = data[i].message;
                            newmsg.setAttribute("id", "messagesreceived");
                            messages.appendChild(newmsg);
                        }
                    }
                }
                screendiv = document.getElementById("mymessagespace");
                screendiv.scrollTop = screendiv.scrollHeight;
            }
        });
    }
}, 500);

function isScrolledToBottom(el) {
    var $el = $(el);
    return el.scrollHeight - $el.scrollTop() - $el.outerHeight() < 1;
}