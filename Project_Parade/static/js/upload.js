document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const uploadedFilesList = document.getElementById('uploaded-files-list');
    const saveAllBtn = document.getElementById('saveAllBtn');
    const successMessage = document.getElementById('successMessage');
    const closeMessage = document.getElementById('closeMessage');

    fileInput.addEventListener('change', function(event) {
        const files = event.target.files;
        displayUploadedFiles(files);
        
        // Show success message
        successMessage.style.display = 'flex';
        successMessage.style.opacity = '1';

        // Automatically hide the message after 3 seconds
        setTimeout(() => {
            successMessage.classList.add('fade-out');
        }, 3000);

        // Hide the element completely after the fade-out transition
        successMessage.addEventListener('transitionend', () => {
            if (successMessage.classList.contains('fade-out')) {
                successMessage.style.display = 'none';
                successMessage.classList.remove('fade-out');
                successMessage.style.opacity = '1';
            }
        });
    });

    function displayUploadedFiles(files) {
        Array.from(files).forEach(file => {
            const tr = document.createElement('tr');

            // File Name
            const fileNameTd = document.createElement('td');
            fileNameTd.textContent = file.name;
            tr.appendChild(fileNameTd);

            // Upload Date
            const uploadDateTd = document.createElement('td');
            uploadDateTd.textContent = new Date().toLocaleDateString(); // Current date
            tr.appendChild(uploadDateTd);

            // Size
            const sizeTd = document.createElement('td');
            sizeTd.textContent = (file.size / 1024).toFixed(2) + ' KB'; // Size in KB
            tr.appendChild(sizeTd);

            // Action
            const actionTd = document.createElement('td');
            const removeBtn = document.createElement('span');
            removeBtn.textContent = 'Remove';
            removeBtn.classList.add('remove-file');
            removeBtn.onclick = () => {
                tr.remove();
            };
            actionTd.appendChild(removeBtn);
            tr.appendChild(actionTd);

            uploadedFilesList.appendChild(tr);
        });
    }

    // This function simulates the file upload process and displays a success message
function handleFileUpload() {
    // Simulate the file upload process here
    // e.g., upload file logic

    // After a successful file upload
    const successMessage = document.getElementById('successMessage');
    successMessage.style.display = 'block'; // Show the success message

    // Hide the success message after 2 seconds
    setTimeout(() => {
        successMessage.style.display = 'none'; // Hide the message
    }, 2000); // 2000 milliseconds = 2 seconds
}

// Attach the handleFileUpload function to the file input change event
document.getElementById('fileInput').addEventListener('change', handleFileUpload);


    saveAllBtn.addEventListener('click', function() {
        alert('Files saved successfully!');
    });

    closeMessage.addEventListener('click', () => {
        successMessage.style.display = 'none';
    });
});
