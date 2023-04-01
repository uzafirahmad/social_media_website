document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("confirmconditionsbuttoncheckmark").style.display = "none";
    const signupform = document.getElementById('signupform');
    signupform.addEventListener('submit', async (event) => {
        event.preventDefault();
        document.getElementById("ptag").innerHTML = "";
        document.getElementById("loginbuttonid").style.backgroundColor = "#1d786a";
        document.getElementById("loginbuttonid").disabled = true;
        document.getElementById("loginbuttonid").style.cursor = "default";
        document.getElementById("confirmpaymentfollowbuttonspinner").style.display = "block";
        document.getElementById("confirmpaymentfollowbuttontext").style.display = "none";
        let text = document.getElementById("emailinput").value;
        let result = text.includes("@");
        let pass1 = document.getElementById("passwordinput1").value;
        let pass2 = document.getElementById("passwordinput2").value;
        let result2 = text.includes(".");
        if (document.getElementById("confirmconditionsbuttoncheckmark").style.display == "block") {
            if (pass1.length > 4 && pass2.length > 4) {
                if (result == true && result2 == true) {
                    $.ajax({
                        type: 'POST',
                        url: 'getsignupvalidation/',
                        data: {
                            username: document.getElementById("usernameinput").value,
                            email: document.getElementById("emailinput").value,
                            password: document.getElementById("passwordinput1").value,
                            confirmpassword: document.getElementById("passwordinput2").value,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        },
                        success: function (data) {
                            if (data.context['errormessage'] != 'Done') {
                                document.getElementById("ptag").innerHTML = data.context['errormessage'];
                                document.getElementById("loginbuttonid").style.backgroundColor = "#29ab97";
                                document.getElementById("loginbuttonid").disabled = false;
                                document.getElementById("loginbuttonid").style.cursor = "pointer";
                                document.getElementById("confirmpaymentfollowbuttonspinner").style.display = "none";
                                document.getElementById("confirmpaymentfollowbuttontext").style.display = "block";
                            }
                            else {
                                signupform.submit();
                            }
                        }

                    })
                }
                else {
                    document.getElementById("loginbuttonid").style.backgroundColor = "#29ab97";
                    document.getElementById("ptag").innerHTML = "Invalid Email";
                    document.getElementById("loginbuttonid").disabled = false;
                    document.getElementById("loginbuttonid").style.cursor = "pointer";
                    document.getElementById("confirmpaymentfollowbuttonspinner").style.display = "none";
                    document.getElementById("confirmpaymentfollowbuttontext").style.display = "block";
                }
            }
            else {
                document.getElementById("loginbuttonid").style.backgroundColor = "#29ab97";
                document.getElementById("ptag").innerHTML = "Password is too short";
                document.getElementById("loginbuttonid").disabled = false;
                document.getElementById("loginbuttonid").style.cursor = "pointer";
                document.getElementById("confirmpaymentfollowbuttonspinner").style.display = "none";
                document.getElementById("confirmpaymentfollowbuttontext").style.display = "block";
            }
        }
        else {
            document.getElementById("loginbuttonid").style.backgroundColor = "#29ab97";
            document.getElementById("ptag").innerHTML = "Accept conditions to Sign up";
            document.getElementById("loginbuttonid").disabled = false;
            document.getElementById("loginbuttonid").style.cursor = "pointer";
            document.getElementById("confirmpaymentfollowbuttonspinner").style.display = "none";
            document.getElementById("confirmpaymentfollowbuttontext").style.display = "block";
        }
    });
});

function RestrictSpace() {
    if (event.keyCode == 32) {
        return false;
    }
}

function checkbox() {
    if (document.getElementById("confirmconditionsbuttoncheckmark").style.display == "none") {
        document.getElementById("confirmconditionsbuttoncheckmark").style.display = "block";
    }
    else {
        document.getElementById("confirmconditionsbuttoncheckmark").style.display = "none";
    }
}