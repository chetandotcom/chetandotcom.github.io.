document.getElementById("signupForm").addEventListener("submit", function(event) {
    let valid = true;

    // Username validation
    let username = document.getElementById("username").value;
    if (username.length < 3) {
        document.getElementById("usernameError").textContent = "Username must be at least 3 characters long.";
        valid = false;
    } else {
        document.getElementById("usernameError").textContent = "";
    }

    // Email validation
    let email = document.getElementById("email").value;
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        document.getElementById("emailError").textContent = "Invalid email format.";
        valid = false;
    } else {
        document.getElementById("emailError").textContent = "";
    }

    // Password validation
    let password = document.getElementById("password").value;
    if (password.length < 6) {
        document.getElementById("passwordError").textContent = "Password must be at least 6 characters long.";
        valid = false;
    } else {
        document.getElementById("passwordError").textContent = "";
    }

    if (!valid) {
        event.preventDefault();
    }
});
