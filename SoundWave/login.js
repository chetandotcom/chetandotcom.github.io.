document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form from reloading page
    alert("Login Successful :)");
  document.getElementById("signupForm").reset();
});