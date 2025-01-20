// Fetch and display users
async function fetchUsers() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/users');
        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }
        const users = await response.json();

        // Clear the table body
        const tbody = document.querySelector('#users-table tbody');
        tbody.innerHTML = '';

        // Populate the table with users
        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.username}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

// Add a new user
async function addUser(event) {
    event.preventDefault(); // Prevent form submission

    const form = event.target;
    const formData = new FormData(form);

    const user = {
        username: formData.get('username'),
        email: formData.get('email')
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (!response.ok) {
            throw new Error('Failed to add user');
        }

        // Clear the form
        form.reset();

        // Refresh the user list
        fetchUsers();
    } catch (error) {
        console.error('Error adding user:', error);
    }
}

// Attach event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Fetch and display users when the page loads
    fetchUsers();

    // Add event listener for the form
    const form = document.getElementById('add-user-form');
    form.addEventListener('submit', addUser);
});