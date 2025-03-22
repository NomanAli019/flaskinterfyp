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
 