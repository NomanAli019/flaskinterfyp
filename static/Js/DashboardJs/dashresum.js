function uploadResume() {
    let formData = new FormData();
    let fileInput = document.getElementById('resumeFile');

    if (fileInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
    }

    let file = fileInput.files[0];
    formData.append("resume", file);

    fetch('/upload_resume', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);  // Success Message
            $('#exampleModal').modal('hide');  // Close Modal
        } else {
            alert(data.error);  // Error Message
        }
    })
    .catch(error => console.error("Error:", error));
}
 

function uploadProfilePicture() {
    let formData = new FormData();
    let fileInput = document.getElementById("profilePicture");

    if (fileInput.files.length === 0) {
        alert("Please select an image file.");
        return;
    }

    formData.append("profile_picture", fileInput.files[0]);

    fetch("/upload_profile_picture", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            location.reload(); // Reload the page if upload is successful
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while uploading.");
    });
}
