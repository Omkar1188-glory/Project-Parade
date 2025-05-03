document.addEventListener('DOMContentLoaded', function() {
    const errorMessage = document.getElementById('errorMessage');

    // Check if the error message exists and is visible
    if (errorMessage && errorMessage.innerText.trim() !== '') {
        errorMessage.style.display = 'block'; // Make sure it's visible
        
        // Set a timeout to hide the error message after 2 seconds
        setTimeout(() => {
            errorMessage.style.display = 'none'; // Hide the message
        }, 2000); // 2000 milliseconds = 2 seconds
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    togglePassword.addEventListener('click', function() {
        // Toggle the type attribute
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        // Toggle the eye icon based on the password visibility
        this.src = type === 'password' 
            ? "{{ url_for('static', filename='images/invisible.png') }}" // Invisible icon
            : "{{ url_for('static', filename='images/eye.png') }}"; // Visible icon
    });
});