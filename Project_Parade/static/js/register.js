function validateRegisterForm() {
    const username = document.getElementById('new-username').value;
    const password = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (username === '' || password === '' || confirmPassword === '') {
        alert('All fields are required!');
        return false;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return false;
    }

    alert('Registration successful for username: ' + username);

    // Placeholder for registration logic
    return false;  // Prevent form submission for demonstration
}



