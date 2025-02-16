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
                credentials: 'include',
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (data.success) {
                // Store the token and its expiration
                localStorage.setItem('token', data.token);
                localStorage.setItem('tokenExpires', Date.now() + (data.expires_in * 1000));
                
                // Get user info
                const userResponse = await fetch('http://localhost:5000/api/auth/user', {
                    headers: {
                        'Authorization': `Bearer ${data.token}`,
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include'
                });
                
                const userData = await userResponse.json();
                if (userData.success) {
                    // Store user info
                    localStorage.setItem('user', JSON.stringify({
                        id: userData.id,
                        username: userData.username,
                        name_eng: userData.name_eng
                    }));
                }

                // Redirect to dashboard
                window.location.href = '../pages/show_dashboard.html';
            } else {
                errorMessage.textContent = data.message || 'Login failed';
                errorMessage.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = 'Network error. Please try again.';
            errorMessage.classList.remove('d-none');
        }
    });

    // Add keypress event listener for Enter key
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            loginBtn.click();
        }
    });
}); 