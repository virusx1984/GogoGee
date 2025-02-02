document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('login-btn');
    const errorMessage = document.getElementById('error-message');

    loginBtn.addEventListener('click', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;

        try {
            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    remember: remember
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store the token in localStorage
                localStorage.setItem('token', data.token);
                // Redirect to dashboard
                window.location.href = '/pages/dashboard.html';
            } else {
                errorMessage.textContent = data.message || 'Login failed';
                errorMessage.classList.remove('d-none');
            }
        } catch (error) {
            errorMessage.textContent = 'Network error. Please try again.';
            errorMessage.classList.remove('d-none');
        }
    });
}); 