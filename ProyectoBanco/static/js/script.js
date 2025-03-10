document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const pqrsForm = document.getElementById("pqrsForm");

    if (registerForm) {
        registerForm.addEventListener("submit", (e) => {
            e.preventDefault();
            let newUser = {
                username: document.getElementById("newUsername").value,
                password: document.getElementById("newPassword").value
            };
            localStorage.setItem(newUser.username, JSON.stringify(newUser));
            alert("Registro exitoso. Ahora inicia sesión.");
            window.location.href = "index.html";
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            e.preventDefault();
            let username = document.getElementById("username").value;
            let password = document.getElementById("password").value;
            let storedUser = JSON.parse(localStorage.getItem(username));

            if (storedUser && storedUser.password === password) {
                sessionStorage.setItem("loggedUser", username);
                window.location.href = "dashboard.html";
            } else {
                alert("Usuario o contraseña incorrectos.");
            }
        });
    }

    if (pqrsForm) {
        pqrsForm.addEventListener("submit", (e) => {
            e.preventDefault();
            let mensaje = document.getElementById("pqrsMensaje").value;
            let nombre = document.getElementById("nombre").value;
            let correo = document.getElementById("correo").value;
            let telefono = document.getElementById("telefono").value;

            fetch("/pqrs", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mensaje, nombre, correo, telefono })
            })
            .then(response => response.json())
            .then(data => {
                alert("PQRS enviada. Estado: " + data.estado);
                document.getElementById(data.estado).classList.add("active");
            })
            .catch(error => console.error("Error:", error));
        });
    }
});
