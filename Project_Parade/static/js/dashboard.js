function toggleNotifications() {
    const notificationsSection = document.getElementById('notificationsSection');
    notificationsSection.style.display = notificationsSection.style.display === 'none' ? 'block' : 'none';
}

function createPost() {
    alert('Create Post functionality can be implemented here.');
}

function addStory() {
    alert('Add Story functionality can be implemented here.');
}

document.addEventListener('DOMContentLoaded', function () {
    // Fetch the username from the DOM
    const usernameElement = document.getElementById('username');
    const username = usernameElement.textContent;

    // Additional logic based on the username (if needed)
    // For example, showing/hiding elements, etc.
});


// Function to open the modal with the image
function openModal(imageSrc) {
    document.getElementById('imageModal').style.display = 'flex';
    document.getElementById('modalImage').src = imageSrc;
}

// Function to close the modal
function closeModal() {
    document.getElementById('imageModal').style.display = 'none';
}

// Close the modal if the user clicks outside of the image
window.onclick = function(event) {
    if (event.target == document.getElementById('imageModal')) {
        closeModal();
    }
}
