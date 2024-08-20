function signup() {
    if (controlEmail() && controlName() && controlPassword() && controlPasswordMatch()) {
        const form = document.getElementById("signupform");
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            if (value == "1") {
                value = 1
            }
            else if (value == "0") {
                value = 0
            }
            jsonData[key] = value;
        });
        console.log(jsonData)

        $.ajax({
            url: 'http://127.0.0.1:5000/auth/register',
            method: 'POST',
            data: JSON.stringify(jsonData),
            processData: false,
            contentType: 'application/json',
            success: function (response) {
                console.log(response);
                window.location.href = "log-in.html";
                alert("Sign up is successful.");
            },
            error: function (xhr, status, error) {
                if (xhr.status === 409) {
                    alert("This email is already in use.");
                } else {
                    alert("An error occurred: " + error);
                }
            }
        });
    }
}


function login() {
    var email = $("#email").val();
    var password = $("#password").val();
    user_type = localStorage.getItem("user_type")
    user_type = parseInt(user_type)

    $.ajax({
        url: "http://127.0.0.1:5000/auth/login",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            user_type: user_type,
            email: email,
            password: password
        }),
        success: function (response) {
            console.log(response);
            localStorage.setItem("name", response.user.name)
            localStorage.setItem("JWT", response.access_token)
            if (user_type == 1) {
                localStorage.setItem("name", response.user.student_name)
                window.location.href = "student_homepage.html";
            }
            else if (user_type == 2) {
                window.location.href = "company_applicants.html"
            }
            else if (user_type == 3) {
                window.location.href = "coordinator_applications.html"
            }
            else if (user_type == 4) {
                window.location.href = "secratary_homepage.html"
            }
        },
        error: function (xhr, status, error) {
            console.error(error);
            var response = JSON.parse(xhr.responseText);
            alert(response.message);

        }
    });
}

function changeUserType(userType) {
    localStorage.setItem("user_type", userType)
    var tabs = document.querySelectorAll('.btn-group .btn');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    event.currentTarget.classList.add('active');
}



function generateLetter() {
    const form = document.getElementById("application");
    const formData = new FormData(form);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });
    console.log(jsonData)
    localStorage.setItem("applied_to", jsonData["mail"])
    var token = localStorage.getItem("JWT");
    $.ajax({
        url: "http://127.0.0.1:5000/student/",
        method: "POST",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        data: JSON.stringify(jsonData),
        success: function (response) {
            console.log("Success:", response);
            window.location.href = "my_applications.html"
            alert("Application letter is sent to company")

        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
            console.error("Server response:", xhr.responseText);
            var response = JSON.parse(xhr.responseText);
            alert(response.message);
        }
    });
}

function myApplications() {
    var token = localStorage.getItem("JWT");
    $.ajax({
        url: "http://127.0.0.1:5000/student/",
        method: "GET",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        success: function (response) {
            console.log("Success:", response);
            var myApplicationsCard = document.getElementById("myApplications");
            myApplicationsCard.innerHTML = ""; // Önceden var olan içerikleri temizler

            for (var i = 0; i < response.Letters.length; i++) {
                var base64String = response.Letters[i].file;

                var application = document.createElement('div');
                application.className = "d-flex align-items-center mb-3"; // Flexbox kullanarak hizalama sağlar

                var company = document.createElement("h2");
                company.className = "flex-grow-1 mb-0";
                company.textContent = response.Letters[i].company_name;
                console.log(response.Letters[i].state)

                var btn = document.createElement("button");
                btn.textContent = "see application letter";
                btn.className = "btn btn-danger btn-sm me-3 ms-3 mt-3 mb-3 rounded-pill";
                btn.addEventListener("click", function () {
                    const filename = "Summer Practice Application Letter.docx";
                    downloadBase64File(base64String, filename);
                });


                var finalize = document.createElement("button");
                finalize.textContent = "finalize";
                finalize.className = "btn btn-success me-3 ms-3 mt-3 mb-3 rounded-pill";
                finalize.style = "display:none"
                finalize.setAttribute("data-index", i); // Index'i data attribute olarak ekleyin
                var status = document.createElement("button");
                var icon = document.createElement("i");
                if (response.Letters[i].state == 1) {
                    finalize.style = "display:inline"
                    icon.className = "bi bi-check-circle";
                    status.appendChild(icon);
                    status.className = "btn btn-success btn-sm rounded-pill";
                }

                else if (response.Letters[i].state == 0) {
                    icon.className = "bi bi-clock";
                    status.appendChild(icon);
                    status.className = "btn btn-warning btn-sm rounded-pill";
                }
                else if (response.Letters[i].state == -1) {
                    icon.className = "bi bi-x-circle";
                    status.appendChild(icon);
                    status.className = "btn btn-danger btn-sm rounded-pill";
                }
                else if (response.Letters[i].state == 2) {
                    icon.className = "bi bi-clock";
                    status.appendChild(icon);
                    status.className = "btn btn-warning btn-sm rounded-pill";
                    waiting_coordinator = document.createElement("p")
                    waiting_coordinator.innerHTML = "Waiting for coordinator checking"
                    application.appendChild(waiting_coordinator)
                }
                else if (response.Letters[i].state == 4) {
                    icon.className = "bi bi-check-circle";
                    status.appendChild(icon);
                    status.className = "btn btn-success btn-sm rounded-pill";
                    waiting_coordinator = document.createElement("p")
                    waiting_coordinator.innerHTML = "Your internship is approved"
                    application.appendChild(waiting_coordinator)
                }
                else if (response.Letters[i].state == -2) {
                    icon.className = "bi bi-x-circle";
                    status.appendChild(icon);
                    status.className = "btn btn-danger btn-sm rounded-pill";
                    waiting_coordinator = document.createElement("p")
                    waiting_coordinator.innerHTML = "Your internship is declined by coordinator"
                    application.appendChild(waiting_coordinator)
                }

                application.appendChild(company);
                application.appendChild(btn);
                application.appendChild(finalize);
                application.appendChild(status);

                myApplicationsCard.appendChild(application);

                finalize.addEventListener("click", function () {
                    var index = this.getAttribute("data-index");
                    var letter = response.Letters[index];
                    var student_id = parseInt(letter.student_id);
                    var cid = parseInt(letter.company_id);

                    $.ajax({
                        url: "http://127.0.0.1:5000/student/finalize",
                        method: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({
                            id: student_id,
                            cid: cid
                        }),
                        success: function (response) {
                            console.log(response);
                        },
                        error: function (xhr, status, error) {
                            console.error(error);
                            alert("Error finalizing: " + error);
                        }
                    });
                });





                // Sadece son eleman değilse çizgi ekle
                if (i < response.Letters.length - 1) {
                    var hr = document.createElement('hr');
                    myApplicationsCard.appendChild(hr);
                }
            }
        },
        error: function (xhr, status, error) {
            alert("Error fetching content: " + error);
        }
    });
}





function applicantsList() {
    var token = localStorage.getItem("JWT");
    $.ajax({
        url: "http://127.0.0.1:5000/company/",
        method: "GET",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        success: function (response) {
            console.log("Success:", response);
            for (i = 0; i < response.Letters.length; i++) {
                applicants = document.getElementById("applicantsList")
                const application = document.createElement('p');
                const btn = document.createElement("button")
                btn.textContent = "see application"
                btn.className = "see-btn btn ms-3 me-3 rounded-pill btn-danger btn-sm"
                btn.setAttribute("id", i);
                application.textContent = response.Letters[i].student_name
                application.appendChild(btn)
                applicants.appendChild(application)
            }

            var buttons = document.querySelectorAll('.see-btn');
            buttons.forEach(function (button) {
                button.addEventListener('click', function () {
                    console.log('Tıklanan butonun ID\'si: ' + this.id);
                    console.log(response.Letters[this.id])
                    localStorage.setItem("applicant", JSON.stringify(response.Letters[this.id]))
                    window.location.href = "company_see_application.html"
                });
            });

        },
        error: function (xhr, status, error) {
            console.log(error)
            console.error("Server response:", xhr.responseText);
        }
    });
}



function downloadBase64File(base64, filename) {
    const link = document.createElement("a");
    link.href = `data:application/octet-stream;base64,${base64}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function controlName() {
    company_name = document.getElementById("name").value
    if (!company_name) {
        alert("Sign up failed. Company name field cannot be empty");
        return false
    } else {
        return true
    }
}
function controlEmail() {
    email = document.getElementById("email").value
    if (!email) {
        alert("Company email field cannot be empty");
        return false;
    } else {
        let pattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        let result = pattern.test(email);
        if (result != true) {
            alert("Sign up failed. Wrong email format");
            return false;
        } else {
            return true;
        }
    }
}

function controlPassword() {
    password = document.getElementById("password").value
    if (password.length < 8) {
        alert("Sign up failed. Password must be at least 8 characters length");
        return false
    } else {
        return true
    }
}
function controlPasswordMatch() {
    password1 = document.getElementById("password").value
    password2 = document.getElementById("password2").value
    if (password1 !== password2) {
        alert("Sign up failed. Passwords do not match")
        return false
    } else {
        return true;
    }
}

function makeAnnouncement() {
    var title = $("#title").val();
    var content = $("#content").val();
    token = localStorage.getItem("JWT")
    $.ajax({
        url: "http://127.0.0.1:5000/company/",  // Correct endpoint
        method: "POST",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        data: JSON.stringify({  // Correct data format
            title: title,
            content: content,
        }),
        success: function (response) {
            console.log("Success:", response);
            window.location.href = "company_applicants.html"
            alert("Announcement is sent to coordinator for checking.")
        },
        error: function (xhr, status, error) {
            console.log("Error:", error);
            console.error("Server response:", xhr.responseText);
        }
    });
}

function getWaitingAnnouncements() {
    var token = localStorage.getItem("JWT");
    var announcementContainer = document.getElementById("announcementContainer");

    $.ajax({
        url: "http://127.0.0.1:5000/coordinator/",
        method: "GET",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        success: function (response) {
            console.log("Success:", response);
            for (var i = 0; i < response.length; i++) {
                var announcementRow = document.createElement("div");
                announcementRow.className = "col-9 col-md-6 col-lg-4 mb-4";
                var announcementCard = document.createElement("div");
                announcementCard.className = "card";
                var announcementCardBody = document.createElement("div");
                announcementCardBody.className = "card-body";
                var title = document.createElement("h1");
                title.className = "card-title";
                title.textContent = response[i].title;
                var company_name = document.createElement("h3");
                company_name.className = "card-title";
                company_name.textContent = response[i].company_name;
                var announcementContent = document.createElement("p");
                announcementContent.className = "card-text";
                announcementContent.textContent = response[i].content;
                var company_email = document.createElement("p");
                company_email.textContent = response[i].company_email;
                var declineBtn = document.createElement("a");
                declineBtn.className = "btn btn-danger me-2 declineButton";
                declineBtn.setAttribute("data-id", response[i].id);
                declineBtn.textContent = "Decline";
                var approveBtn = document.createElement("a");
                approveBtn.className = "btn btn-success me-2 approveButton";
                approveBtn.setAttribute("data-id", response[i].id);
                approveBtn.textContent = "Approve";

                announcementRow.appendChild(announcementCard);
                announcementCardBody.appendChild(title);
                announcementCardBody.appendChild(company_name);
                announcementCardBody.appendChild(announcementContent);
                announcementCardBody.appendChild(company_email);
                announcementCardBody.appendChild(declineBtn);
                announcementCardBody.appendChild(approveBtn);
                announcementCard.appendChild(announcementCardBody);
                announcementContainer.appendChild(announcementRow);

                declineBtn.addEventListener('click', function () {
                    var id = this.getAttribute("data-id");
                    console.log('Decline button ID:', id);
                    localStorage.setItem("announcement", id);
                    declineWaitingAnnouncement();
                });

                approveBtn.addEventListener('click', function () {
                    var id = this.getAttribute("data-id");
                    console.log('Approve button ID:', id);
                    localStorage.setItem("announcement", id);
                    approveWaitingAnnouncement();
                });
            }
        },
        error: function (xhr, status, error) {
            console.log("Error:", error);
            console.error("Server response:", xhr.responseText);
        }
    });
}

function approveWaitingAnnouncement() {

    token = localStorage.getItem("JWT")
    id = localStorage.getItem("announcement")
    id = parseInt(id)
    console.log(id)
    $.ajax({
        url: "http://127.0.0.1:5000/coordinator/",  // Correct endpoint
        method: "POST",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        data: JSON.stringify({  // Correct data format
            id: id
        }),
        success: function (response) {
            console.log("Success:", response);
            alert("Announcement is published to students")
        },
        error: function (xhr, status, error) {
            console.log("Error:", error);
            console.error("Server response:", xhr.responseText);
        }
    });

}

function declineWaitingAnnouncement() {
    token = localStorage.getItem("JWT")
    id = localStorage.getItem("announcement")
    id = parseInt(id)
    console.log(id)
    $.ajax({
        url: "http://127.0.0.1:5000/coordinator/decline",  // Correct endpoint
        method: "POST",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        data: JSON.stringify({  // Correct data format
            id: id
        }),
        success: function (response) {
            console.log("Success:", response);
            alert("Announcement is deleted.")
        },
        error: function (xhr, status, error) {
            console.log("Error:", error);
            console.error("Server response:", xhr.responseText);
        }
    });
}
function getCheckedAnnouncements() {
    var token = localStorage.getItem("JWT");
    var announcementContainer = document.getElementById("announcementContainer");

    $.ajax({
        url: "http://127.0.0.1:5000/student/announcement",
        method: "GET",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        success: function (response) {
            console.log("Success:", response);
            for (var i = 0; i < response.length; i++) {
                var announcementRow = document.createElement("div");
                announcementRow.className = "col-9 col-md-6 col-lg-4 mb-4";
                var announcementCard = document.createElement("div");
                announcementCard.className = "card";
                var announcementCardBody = document.createElement("div");
                announcementCardBody.className = "card-body";
                var title = document.createElement("h1");
                title.className = "card-title";
                title.textContent = response[i].title;
                var company_name = document.createElement("h3");
                company_name.className = "card-title";
                company_name.textContent = response[i].company_name;
                var announcementContent = document.createElement("p");
                announcementContent.className = "card-text";
                announcementContent.textContent = response[i].content;
                var company_email = document.createElement("p");
                company_email.textContent = response[i].company_email;
                announcementRow.appendChild(announcementCard);
                announcementCardBody.appendChild(title);
                announcementCardBody.appendChild(company_name)
                announcementCardBody.appendChild(announcementContent);
                announcementCardBody.appendChild(company_email);
                announcementCard.appendChild(announcementCardBody);
                announcementContainer.appendChild(announcementRow);

            }
        },
        error: function (xhr, status, error) {
            console.log("Error:", error);
            console.error("Server response:", xhr.responseText);
        }
    });
}

function seeApplicant() {
    applicant = localStorage.getItem("applicant")
    applicant = JSON.parse(applicant)
    console.log(typeof (applicant))
    pdfLink = document.getElementById("pdfLink")
    pdfLink.innerHTML = "<i class='bi bi-filetype-pdf'></i>" + applicant.student_name + "application_letter.docx"
    base64String = applicant.file
    student_name = document.querySelector(".name")
    student_name.innerHTML = applicant.student_name
    student_mail = document.querySelector(".student_mail")
    student_mail.innerHTML = applicant.email
    class_ = document.querySelector(".class")
    class_.innerHTML = applicant.student_class
    gpa = document.querySelector(".gpa")
    gpa.innerHTML = applicant.gpa
    console.log(gpa)
    extra = document.querySelector(".extra")
    extra.innerHTML = applicant.extra_informations
    console.log(extra)

    pdfLink.addEventListener("click", function () {
        const filename = applicant.student_name + "application_letter.docx";
        downloadBase64File(base64String, filename);
    });

}
function declineStudent() {
    student = localStorage.getItem("applicant")
    student = JSON.parse(student)
    student_id = student.id
    student_id = parseInt(student_id)
    cid = student.company_id
    cid = parseInt(cid)

    $.ajax({
        url: "http://127.0.0.1:5000/company/decline",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            id: student_id,
            cid: cid
        }),
        success: function (response) {
            console.log(response);
            window.location.href = "company_applicants.html"
            alert("Student is rejected.")

        },
        error: function (xhr, status, error) {
            console.error(error);
            alert(response.message);

        }
    });
}

function approveStudent() {
    student = localStorage.getItem("applicant")
    student = JSON.parse(student)
    student_id = student.id
    student_id = parseInt(student_id)
    cid = student.company_id
    cid = parseInt(cid)
    console.log(student_id)
    console.log(cid)

    $.ajax({
        url: "http://127.0.0.1:5000/company/approve",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            id: student_id,
            cid: cid
        }),
        success: function (response) {
            console.log(response);
            window.location.href = "company_applicants.html"
            alert("Student is accepted.")

        },
        error: function (xhr, status, error) {
            console.error(error);
            alert(response.message);

        }
    });

}

function company_upload_form() {
    document.getElementById('uploadButton').addEventListener('click', function () {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            alert('Please select a file!');
            return;
        }

        const applicant = JSON.parse(localStorage.getItem("applicant"));
        const sid = parseInt(applicant.student_id);
        const cid = parseInt(applicant.company_id);

        const reader = new FileReader();
        reader.onload = function () {
            const base64File = reader.result.split(',')[1];  // Split to get only the base64 part

            console.log('Base64 File:', typeof (base64File)); // Debugging
            console.log('Student ID:', sid); // Debugging
            console.log('Company ID:', cid); // Debugging

            $.ajax({
                url: 'http://127.0.0.1:5000/company/upload',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    file: base64File,
                    sid: sid,
                    cid: cid
                }),
                success: function (data) {
                    console.log(data)
                    window.location.href="company_applicants.html"
                    alert('File uploaded successfully');

                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error('Error:', errorThrown);
                    alert('An error occurred while uploading the file');
                }
            });
        };
        reader.readAsDataURL(file);
    });
}

function finalizedList() {
    var token = localStorage.getItem("JWT");
    $.ajax({
        url: "http://127.0.0.1:5000/company/finalized",
        method: "GET",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        success: function (response) {
            console.log("Success:", response);
            for (i = 0; i < response.Letters.length; i++) {
                applicants = document.getElementById("applicantsList")
                const application = document.createElement('p');
                const btn = document.createElement("button")
                btn.textContent = "Upload summer practice application form"
                btn.className = "see-btn btn ms-3 me-3 rounded-pill btn-danger btn-sm"
                btn.setAttribute("id", i);
                application.textContent = response.Letters[i].student_name
                application.appendChild(btn)
                applicants.appendChild(application)
            }

            var buttons = document.querySelectorAll('.see-btn');
            buttons.forEach(function (button) {
                button.addEventListener('click', function () {
                    console.log('Tıklanan butonun ID\'si: ' + this.id);
                    console.log(response.Letters[this.id])
                    localStorage.setItem("applicant", JSON.stringify(response.Letters[this.id]))
                    window.location.href = "company_upload_form.html"
                });
            });

        },
        error: function (xhr, status, error) {
            console.log(error)
            console.error("Server response:", xhr.responseText);
        }
    });
}

function coordinator_finalizeds() {
    var token = localStorage.getItem("JWT");
    $.ajax({
        url: "http://127.0.0.1:5000/coordinator/finalized",
        method: "GET",
        contentType: "application/json",
        // headers: {
        //     Authorization: 'Bearer ' + token
        // },
        success: function (response) {
            console.log("Success:", response);
            for (i = 0; i < response.Letters.length; i++) {
                applicants = document.getElementById("applicantsList")
                const application = document.createElement('p');
                const btn = document.createElement("button")
                btn.textContent = "Check Summer Practice Application Form"
                btn.className = "see-btn btn ms-3 me-3 rounded-pill btn-danger btn-sm"
                btn.setAttribute("id", i);
                application.textContent = response.Letters[i].student_name
                application.appendChild(btn)
                applicants.appendChild(application)
            }

            var buttons = document.querySelectorAll('.see-btn');
            buttons.forEach(function (button) {
                button.addEventListener('click', function () {
                    console.log('Tıklanan butonun ID\'si: ' + this.id);
                    console.log(response.Letters[this.id])
                    localStorage.setItem("applicant", JSON.stringify(response.Letters[this.id]))
                    window.location.href = "coordinator_see_application.html"
                });
            });

        },
        error: function (xhr, status, error) {
            console.log(error)
            console.error("Server response:", xhr.responseText);
        }
    });
}


function updateProfile() {

    var extra = $("#extra").val();
    token = localStorage.getItem("JWT")
    $.ajax({
        url: "http://127.0.0.1:5000/student/profile",  // Correct endpoint
        method: "POST",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        data: JSON.stringify({  // Correct data format
            extra_information: extra,
        }),
        success: function (response) {
            console.log("Success:", response);
            window.location.href = "student_homepage.html"
            alert("Profile updated.")
        },
        error: function (xhr, status, error) {
            console.log("Error:", error);
            console.error("Server response:", xhr.responseText);
        }
    });

}

function coordinator_see_application() {
    applicant = localStorage.getItem("applicant")
    applicant = JSON.parse(applicant)
    console.log(typeof (applicant))
    pdfLink = document.getElementById("pdfLink")
    pdfLink.innerHTML = applicant.student_name + "_summer_practice_application_form.pdf"
    base64String = applicant.file

    pdfLink.addEventListener("click", function () {
        const filename = applicant.student_name + "summer_practice_application_form.pdf";
        downloadBase64File(base64String, filename);
    });
}

function coordinator_decline() {
    student = localStorage.getItem("applicant")
    student = JSON.parse(student)
    student_id = student.student_id
    student_id = parseInt(student_id)
    cid = student.company_id
    cid = parseInt(cid)

    $.ajax({
        url: "http://127.0.0.1:5000/coordinator/decline_app",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            id: student_id,
            cid: cid
        }),
        success: function (response) {
            console.log(response);
            alert("Student is rejected.")

        },
        error: function (xhr, status, error) {
            console.error(error);
            alert(response.message);

        }
    });
}

function coordinator_approve() {
    student = localStorage.getItem("applicant")
    student = JSON.parse(student)
    student_id = student.student_id
    student_id = parseInt(student_id)
    cid = student.company_id
    cid = parseInt(cid)
    console.log(student_id)
    console.log(cid)

    $.ajax({
        url: "http://127.0.0.1:5000/coordinator/approve_app",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            id: student_id,
            cid: cid
        }),
        success: function (response) {
            console.log(response);
            alert("Student is accepted.")

        },
        error: function (xhr, status, error) {
            console.error(error);
            alert(response.message);

        }
    });
}

function SGKlist() {
    var token = localStorage.getItem("JWT");
    $.ajax({
        url: "http://127.0.0.1:5000/secratary/",
        method: "GET",
        contentType: "application/json",
        // headers: {
        //     Authorization: 'Bearer ' + token
        // },
        success: function (response) {
            // console.log("Success:", response);
            for (i = 0; i < response.Letters.length; i++) {
                applicants = document.getElementById("applicantsList")
                const application = document.createElement('p');
                const btn = document.createElement("button")
                btn.textContent = "Download all documents"
                btn.className = "see-btn btn ms-3 me-3 rounded-pill btn-danger btn-sm"
                btn.setAttribute("id", i);
                application.textContent = response.Letters[i].student_name
                application.appendChild(btn)
                applicants.appendChild(application)
            }

            var buttons = document.querySelectorAll('.see-btn');
            buttons.forEach(function (button) {
                button.addEventListener('click', function () {
                    console.log('Tıklanan butonun ID\'si: ' + this.id);
                    localStorage.setItem("applicant", JSON.stringify(response.Letters[this.id]))
                    student = localStorage.getItem("applicant")
                    student = JSON.parse(student)
                    student_id = student.student_id
                    student_id = parseInt(student_id)
                    cid = student.company_id
                    cid = parseInt(cid)

                    $.ajax({
                        url: "http://127.0.0.1:5000/secratary/download",
                        method: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({
                            id: student_id,
                            cid: cid
                        }),
                        success: function (response) {
                            console.log(response);
                            document1 = response.Letter.file
                            document2 = response.Form.file
                            filename1 = response.Letter.student_name + "_application_letter.docx"
                            filename2 = response.Form.student_name + "_application_form.pdf"
                            console.log(response.Letter)
                            console.log(response.Form)
                            downloadBase64File(document1, filename1);
                            downloadBase64File(document2, filename2);


                        },
                        error: function (xhr, status, error) {
                            console.error(error);
                            alert(response.message);

                        }
                    });
                });
            });

        },
        error: function (xhr, status, error) {
            console.log(error)
            console.error("Server response:", xhr.responseText);
        }
    });
}

function download_documents() {
    student = localStorage.getItem("applicant")
    student = JSON.parse(student)
    student_id = student.id
    student_id = parseInt(student_id)
    cid = student.company_id
    cid = parseInt(cid)

    $.ajax({
        url: "http://127.0.0.1:5000/company/decline",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            id: student_id,
            cid: cid
        }),
        success: function (response) {
            console.log(response);
            alert("Student is rejected.")

        },
        error: function (xhr, status, error) {
            console.error(error);
            alert(response.message);

        }
    });
}

function downloadFormTemplate() {
    var token = localStorage.getItem("JWT");
    $.ajax({
        url: "http://127.0.0.1:5000/company/template",
        method: "GET",
        contentType: "application/json",
        headers: {
            Authorization: 'Bearer ' + token
        },
        success: function (response) {
            console.log("Success:", response);

            document1 = response.Form.file
            filename1 =  "application_form_template.docx"
            downloadBase64File(document1, filename1);

        },
        error: function (xhr, status, error) {
            console.log(error)
            console.error("Server response:", xhr.responseText);
        }
    });
}
