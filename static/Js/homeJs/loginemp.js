function check_login() {
    var email = document.getElementById("emaillg")?.value?.trim();
    var password = document.getElementById("passwordlg")?.value?.trim();

    if (!email || !password) {
        alert("All fields are required.");
        return;
    }

    const employeelg = { email: email, password: password };

    fetch('/check-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employeelg }),
    })
    .then(response => response.json()) // Parse JSON response
    .then(data => {
        if (data.success) {
            alert('Login successful');
            window.location.href = '/dashhome'; // Redirect to dashboard or another page
        } else {
            alert(data.message || 'Wrong credentials');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    });
}
