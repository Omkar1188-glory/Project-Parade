// Function to open the upload project popup
function openUploadPopup() {
    document.getElementById('uploadProjectPopup').style.display = 'block';
}

// Function to close the upload project popup
function closeUploadPopup() {
    document.getElementById('uploadProjectPopup').style.display = 'none';
}

// Function to upload the project and add it to the table
function uploadProject() {
    const projectTitle = document.getElementById('projectTitle').value;
    const uploadedBy = document.getElementById('uploadedBy').value;
    const college = document.getElementById('college').value;
    const uploadDate = document.getElementById('uploadDate').value;
    const projectFiles = document.getElementById('projectFiles').files;

    if (!projectTitle || !uploadedBy || !college || !uploadDate || projectFiles.length === 0) {
        alert("Please fill in all fields and upload at least one file.");
        return;
    }

    // Creating a new row in the projects table
    const projectsTable = document.getElementById('global-projects-list');
    const newRow = projectsTable.insertRow();

    newRow.insertCell(0).innerText = projectTitle;
    newRow.insertCell(1).innerText = uploadedBy;
    newRow.insertCell(2).innerText = college;
    newRow.insertCell(3).innerText = uploadDate;

    // Prepare file links
    const fileLinks = Array.from(projectFiles).map(file => {
        return `<a href="${URL.createObjectURL(file)}" download>${file.name}</a>`;
    }).join(', ');

    newRow.insertCell(4).innerHTML = fileLinks;

    const actionCell = newRow.insertCell(5);
    const downloadBtn = document.createElement("button");
    downloadBtn.innerText = "Download All";
    downloadBtn.className = "download-all-btn";
    downloadBtn.onclick = () => {
        // Implement download logic here (if needed)
        alert("Download logic is not implemented in this demo.");
    };
    actionCell.appendChild(downloadBtn);

    // Clear the form fields
    document.getElementById('projectTitle').value = '';
    document.getElementById('uploadedBy').value = '';
    document.getElementById('college').value = '';
    document.getElementById('uploadDate').value = '';
    document.getElementById('projectFiles').value = '';

    // Close the popup
    closeUploadPopup();
}

// upload.js
function goToPollsPage() {
    // Redirect to the polls_page template
    window.location.href = "/polls"; // Update the URL to match your routing setup
}
