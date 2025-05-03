document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');
    const inputs = document.querySelectorAll('#profile-form input, #profile-form textarea');
    const fileInput = document.getElementById('fileInput');

    const linkedinInput = document.getElementById('linkedin');
    const githubInput = document.getElementById('github');
    const linkedinVisitBtn = document.getElementById('linkedin-visit');
    const linkedinSaveBtn = document.getElementById('linkedin-save');
    const githubVisitBtn = document.getElementById('github-visit');
    const githubSaveBtn = document.getElementById('github-save');

    // Enable edit functionality
    editBtn.addEventListener('click', function () {
        toggleEditMode(true);
    });

    // Save the changes
    saveBtn.addEventListener('click', function (event) {
        event.preventDefault();
        saveChanges();
        toggleEditMode(false);
    });

    // Toggle edit mode
    function toggleEditMode(enable) {
        inputs.forEach(input => input.disabled = !enable);
        fileInput.disabled = !enable;
        linkedinInput.disabled = !enable;
        githubInput.disabled = !enable;
        linkedinVisitBtn.disabled = false;
        linkedinSaveBtn.disabled = !enable;
        githubVisitBtn.disabled = false;
        githubSaveBtn.disabled = !enable;
        
        editBtn.style.display = enable ? 'none' : 'block';
        saveBtn.disabled = !enable;
    }

    // Function to save changes
    function saveChanges() {
        const profileData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            location: document.getElementById('location').value,
            phone: document.getElementById('phone').value,
            about: document.getElementById('about').value,
            linkedin: document.getElementById('linkedin').value,
            github: document.getElementById('github').value
        };

        fetch('/save_profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profileData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || 'Error: ' + data.error);
        })
        .catch(error => console.error('Error:', error));
    }

    // Preview Image functionality
    function previewImage(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('profileImage').src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    }
    window.previewImage = previewImage;

    // Function to visit the URL
    function visitUrl(platform) {
        const url = document.getElementById(platform).value;
        if (url) {
            window.open(url, '_blank');
        } else {
            alert('URL not provided');
        }
    }
    window.visitUrl = visitUrl;

    // Function to save the URL
    function saveUrl(platform) {
        const url = document.getElementById(platform).value;
        if (url) {
            alert(`${platform.charAt(0).toUpperCase() + platform.slice(1)} URL saved: ${url}`);
        } else {
            alert('Please enter a valid URL');
        }
    }
    window.saveUrl = saveUrl;

    // Display success message
    function showSuccessMessage() {
        const successMessage = document.createElement('div');
        successMessage.className = 'success-message';
        successMessage.textContent = 'Profile saved successfully!';
        document.body.appendChild(successMessage);
        
        setTimeout(() => successMessage.classList.add('fade-out'), 3000);
        successMessage.addEventListener('transitionend', () => successMessage.remove());
    }
});
