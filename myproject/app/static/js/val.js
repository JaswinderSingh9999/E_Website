// javascript
// ================= PAGE NAVIGATION =================

document.addEventListener("DOMContentLoaded", function () {

    const navLinks = document.querySelectorAll(".nav-link");
    const sections = document.querySelectorAll("section, footer");

    function showSection(targetId) {

        sections.forEach(section => {
            section.style.display = "none";
            section.classList.remove("show-section");
        });

        const target = document.getElementById(targetId);

        if (target) {

            target.style.display = "block";

            setTimeout(function () {
                target.classList.add("show-section");
            }, 10);

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }
    }

    navLinks.forEach(link => {

        link.addEventListener("click", function (e) {

            e.preventDefault();

            const href = this.getAttribute("href");

            if (!href) return;

            const targetId = href.substring(1);

            navLinks.forEach(nav => nav.classList.remove("active"));
            this.classList.add("active");

            showSection(targetId);

        });

    });

    showSection("registration");

});



// ================= REGISTER VALIDATION =================

function validateRegister(event) {

    event.preventDefault();

    const form = event.currentTarget;
    const msg = document.getElementById("registerMessage");
    const submitBtn = form.querySelector("button");

    const username = document.getElementById("reg_username").value.trim();
    const email = document.getElementById("reg_email").value.trim();
    const password = document.getElementById("reg_password").value.trim();
    const confirm = document.getElementById("reg_confirm").value.trim();

    msg.innerText = "";
    msg.classList.remove("error", "success");

    // ===== VALIDATION =====
    if (username === "") {
        msg.innerText = "Enter username";
        msg.classList.add("error");
        return false;
    }

    if (!email.includes("@")) {
        msg.innerText = "Enter valid email";
        msg.classList.add("error");
        return false;
    }

    if (password.length < 6) {
        msg.innerText = "Password must be 6+ characters";
        msg.classList.add("error");
        return false;
    }

    if (password !== confirm) {
        msg.innerText = "Passwords do not match";
        msg.classList.add("error");
        return false;
    }

    submitBtn.disabled = true;

    // ===== API CALL =====
    fetch(form.action, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]')?.value || ""
        },
        body: new FormData(form)
    })
    .then(res => res.json())
    .then(data => {

        submitBtn.disabled = false;

        if (data.status === "error") {

            msg.innerText = data.message;
            msg.classList.add("error");

        } else if (data.status === "success") {

            msg.innerText = "Registration Successful";
            msg.classList.add("success");

            // ✅ Close modal instantly
            let registerEl = document.getElementById("registerModal");
            let registerModal = bootstrap.Modal.getInstance(registerEl) 
                                || new bootstrap.Modal(registerEl);
            registerModal.hide();

            // ✅ Prevent reopen
            localStorage.setItem("registerSuccess", "true");

            // ✅ Reload instantly
            location.reload();
        }

    })
    .catch(err => {
        submitBtn.disabled = false;
        console.log(err);
    });

    return false;
}

// ================= LOGIN VALIDATION =================

function validateLogin(event) {

    event.preventDefault();

    var msg = document.getElementById("loginMessage");

    const username = document.getElementById("login_username").value.trim();
    const password = document.getElementById("login_password").value.trim();

    msg.innerText = "";
    msg.classList.remove("error", "success");

    if (username === "") {
        msg.innerText = "Enter username";
        msg.classList.add("error");
        return false;
    }

    if (password === "") {
        msg.innerText = "Enter password";
        msg.classList.add("error");
        return false;
    }

    let form = event.target;

    fetch(form.action, {

        method: "POST",

        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },

        body: new FormData(form)

    })

    .then(response => response.json())

    .then(data => {

        if (data.status === "error") {

            msg.innerText = data.message;
            msg.classList.add("error");

        }

        else if (data.status === "success") {

            msg.innerText = "Login successful!";
            msg.classList.add("success");

            window.location.href = data.redirect;

        }

    })

    .catch(error => console.log(error));

    return false;

}



// ================= COURSE BUTTON =================

const enrollButtons = document.querySelectorAll(".enroll-btn");

enrollButtons.forEach(btn => {

    btn.addEventListener("click", function () {

        const courseName = this.closest(".card")
            .querySelector(".card-title").innerText;

        alert("You selected: " + courseName);

    });

});


// ================= CONTACT MODAL =================

const footerModal = document.getElementById("footerModal");

if (footerModal) {

    footerModal.addEventListener("shown.bs.modal", function () {

        setTimeout(function () {

            const modal = bootstrap.Modal.getInstance(footerModal);

            if (modal) modal.hide();

        }, 4000);

    });

}



// ================= COURSE MODAL =================

const courseModal = document.getElementById("courseModal");

if (courseModal) {

    courseModal.addEventListener("show.bs.modal", function () {

        setTimeout(function () {

            const modal = bootstrap.Modal.getInstance(courseModal);

            if (modal) modal.hide();

        }, 2000);

    });

}

// ================= COUNTRY DROPDOWN =================

$(document).ready(function () {

    $('#registerModal').on('shown.bs.modal', function () {

        fetch("https://restcountries.com/v3.1/all?fields=name,flags")
        .then(res => res.json())
        .then(data => {

            data.sort((a,b)=>a.name.common.localeCompare(b.name.common));

            let countries = data.map(c => ({
                id: c.name.common,
                text: c.name.common,
                flag: c.flags.png
            }));

            $("#countrySelect").select2({
                placeholder: "Select Country",
                dropdownParent: $("#registerModal"),
                data: countries,
                templateResult: formatCountry,
                templateSelection: formatCountry,
                escapeMarkup: m => m,
                width: '100%'
            });

        });

    });

});

function formatCountry(country){
    if(!country.id) return country.text;

    return `
    <span>
        <img src="${country.flag}" style="width:20px;margin-right:8px;">
        ${country.text}
    </span>`;
}

// password hidd
function togglePassword(id, icon){

const input = document.getElementById(id);

if(input.type === "password"){
input.type = "text";
icon.innerHTML = "🙈";
}
else{
input.type = "password";
icon.innerHTML = "👁";
}

}


// let option = document.createElement("option");
// option.value = country.name.common;
// option.textContent = country.name.common;


select.appendChild(option);

// email 
document.getElementById("newsletterForm").addEventListener("submit", function(e){
    e.preventDefault();

    let formData = new FormData(this);

    fetch("", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === "subscribed"){
            Swal.fire({
                icon: 'success',
                title: 'Subscribed!',
                text: 'You have joined our newsletter.'
            });

            document.getElementById("newsletterForm").reset();
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("contactForm");

    form.addEventListener("submit", function(e) {

        e.preventDefault(); // always stop first

        let isValid = true;

        let name = form.querySelector('[name="name"]');
        let email = form.querySelector('[name="email"]');
        let subject = form.querySelector('[name="subject"]');
        let message = form.querySelector('[name="message"]');

        let emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

        // Clear old errors
        document.getElementById("nameError").innerText = "";
        document.getElementById("emailError").innerText = "";
        document.getElementById("subjectError").innerText = "";
        document.getElementById("messageError").innerText = "";

        // Remove red borders
        form.querySelectorAll(".form-control").forEach(el => {
            el.classList.remove("is-invalid");
        });

        // Name
        if (name.value.trim() === "") {
            document.getElementById("nameError").innerText = "Name is required";
            name.classList.add("is-invalid");
            isValid = false;
        }

        // Email
        if (email.value.trim() === "") {
            document.getElementById("emailError").innerText = "Email is required";
            email.classList.add("is-invalid");
            isValid = false;
        } else if (!emailPattern.test(email.value)) {
            document.getElementById("emailError").innerText = "Enter valid email";
            email.classList.add("is-invalid");
            isValid = false;
        }

        // Subject
        if (subject.value.trim() === "") {
            document.getElementById("subjectError").innerText = "Subject is required";
            subject.classList.add("is-invalid");
            isValid = false;
        }

        // Message
        if (message.value.trim() === "") {
            document.getElementById("messageError").innerText = "Message is required";
            message.classList.add("is-invalid");
            isValid = false;
        } else if (message.value.trim().length < 10) {
            document.getElementById("messageError").innerText = "Minimum 10 characters required";
            message.classList.add("is-invalid");
            isValid = false;
        }

        //  If all valid → submit form
        if (isValid) {
            form.submit();
        }

    });

});



// //  chat bot 
// console.log("Chatbot Loaded ✅");

// // Open Chat
// document.getElementById("chatLauncher").onclick = function () {
//     document.getElementById("chatModal").style.display = "block";
// };

// // Close Chat
// document.getElementById("closeChat").onclick = function () {
//     document.getElementById("chatModal").style.display = "none";
// };

// // Start Chat (Lead Form Submit)
// function startChat() {
//     let name = document.getElementById("name").value;
//     let email = document.getElementById("email").value;

//     if (name === "" || email === "") {
//         alert("Please fill all fields");
//         return;
//     }

//     document.getElementById("leadForm").style.display = "none";
//     document.getElementById("chatSection").style.display = "block";

//     addMessage("Bot", "Hello " + name + "! How can I help you?");
// }

// // Send Message
// function sendMessage() {
//     let input = document.getElementById("userInput");
//     let message = input.value;

//     if (message === "") return;

//     addMessage("You", message);

//     // Dummy bot reply
//     setTimeout(() => {
//         addMessage("Bot", "You said: " + message);
//     }, 500);

//     input.value = "";
// }

// // Add Message to Chat
// function addMessage(sender, text) {
//     let chat = document.getElementById("chatMessages");

//     let msg = document.createElement("div");
//     msg.innerHTML = "<b>" + sender + ":</b> " + text;

//     chat.appendChild(msg);
//     chat.scrollTop = chat.scrollHeight;
// }