const loginForm = document.querySelector("#login-form");
const loginError = document.querySelector("#login-error");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(loginForm);
        try {
            const data = await window.hrrgApi.postJson("/api/auth/login", {
                username: formData.get("username"),
                password: formData.get("password"),
                profile: formData.get("profile"),
            });
            window.location.href = data.redirect_url;
        } catch (error) {
            if (loginError) {
                loginError.hidden = false;
                loginError.textContent = error.message;
            }
        }
    });
}
