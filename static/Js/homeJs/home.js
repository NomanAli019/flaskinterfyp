function moveto_employesignup(){
    const joinsection1 = document.getElementById("joinus-sect1");
    const joinsection2 = document.getElementById("joinussect2");

    joinsection2.classList.remove("joinus-sect2contdisp");
    joinsection1.style.display = "none";
}

function moveto_joinus(){
    const joinsection1 = document.getElementById("joinus-sect1");
    const joinsection2 = document.getElementById("joinussect2");

    joinsection2.classList.add("joinus-sect2contdisp");
    joinsection1.style.display = "block";
}

var globalFullNameemp;
var globalEmailemp;
var globalPasswordemp;
var phonenumberemp;
var youraddressemp;
var countryemp;

function validateForm() {
    globalFullNameemp = document.getElementById("fullName").value.trim();
    globalEmailemp = document.getElementById("email").value.trim();
    globalPasswordemp = document.getElementById("password").value.trim();
    
    console.log("Full Name:", globalFullNameemp);
    console.log("Email:", globalEmailemp);
    console.log("Password:", globalPasswordemp);

    moveto_employeecont();
    return false;
}

function validatecompForm(event) {
    event.preventDefault();

    phonenumberemp = document.getElementById("phonenumber").value.trim();
    youraddressemp = document.getElementById("Youraddress").value.trim();
    countryemp = document.getElementById("country").value.trim();

    if (!phonenumberemp || !youraddressemp || !countryemp) {
        alert("Please fill out all fields.");
        return false;
    }

    

    registerEmployee();
}
// function registerEmployee() {
//     // Get values from input fields
//     phonenumberemp = document.getElementById("phonenumber")?.value?.trim();
//     youraddressemp = document.getElementById("Youraddress")?.value?.trim();
//     countryemp = document.getElementById("country")?.value?.trim();

//     // Check if global variables are defined
//     if (!globalFullNameemp || !globalEmailemp || !globalPasswordemp ||
//         !phonenumberemp || !youraddressemp || !countryemp) {
//         alert("All fields are required.");
//         return; // Stop execution if any field is missing
//     }

//     const employeeData = {
//         full_name: globalFullNameemp,
//         email: globalEmailemp,
//         password: globalPasswordemp,
//         phone_number: phonenumberemp,
//         house_address: youraddressemp,
//         country: countryemp
//     };

//     console.log("Sending Data:", JSON.stringify({ employeeData })); // Debugging log

//     fetch('/register-employee', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ employeeData }),
//     })
//     .then(response => {
//         console.log("Raw Response:", response); // Debugging log
//         if (response.status === 201 || response.ok) {  // Handle 201 properly
//             return response.json();
//         } 
//         throw new Error(`HTTP Error! Status: ${response.status}`);
//     })
//     .then(result => {
//         console.log("Response Data:", result); // Debugging log
//         if (result.exists) {
//             alert('User already exists');
//         } else if (result.success) {
//             alert('Account created successfully');
//         } else {
//             alert(result.message || 'Something went wrong. Please try again.');
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('User Already Exists !!!.');
//     });
    
// }

// function registerEmployee() {
//     // Get values from input fields
//     phonenumberemp = document.getElementById("phonenumber")?.value?.trim();
//     youraddressemp = document.getElementById("Youraddress")?.value?.trim();
//     countryemp = document.getElementById("country")?.value?.trim();

//     // Check if global variables are defined
//     if (!globalFullNameemp || !globalEmailemp || !globalPasswordemp ||
//         !phonenumberemp || !youraddressemp || !countryemp) {
//         alert("All fields are required.");
//         return; // Stop execution if any field is missing
//     }

//     const employeeData = {
//         full_name: globalFullNameemp,
//         email: globalEmailemp,
//         password: globalPasswordemp,
//         phone_number: phonenumberemp,
//         house_address: youraddressemp,
//         country: countryemp
//     };

//     fetch('/register-employee', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ employeeData }),
//     })
//     .then(response => {
//         if (response.status === 200) {
//             alert('Account created successfully');
//             window.location.href = '/login'; // Redirect to /login
//         } else if (response.status === 400) {
//             alert('User already exists');
//         } else {
//             alert('Something went wrong. Please try again.');
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('An error occurred. Please try again.');
//     });
// }

function registerEmployee(event) {
    if (event) event.preventDefault(); // ✅ Prevent page reload if event exists

    // Get values from input fields
    let phonenumberemp = document.getElementById("phonenumber")?.value?.trim();
    let youraddressemp = document.getElementById("Youraddress")?.value?.trim();
    let countryemp = document.getElementById("country")?.value?.trim();

    // Check if global variables are defined
    if (!globalFullNameemp || !globalEmailemp || !globalPasswordemp ||
        !phonenumberemp || !youraddressemp || !countryemp) {
        alert("All fields are required.");
        return; // Stop execution if any field is missing
    }

    const employeeData = {
        full_name: globalFullNameemp,
        email: globalEmailemp,
        password: globalPasswordemp,
        phone_number: phonenumberemp,
        house_address: youraddressemp,
        country: countryemp
    };

    fetch('/register-employee', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employeeData }),
    })
    .then(response => response.json())  // ✅ Parse JSON response
    .then(data => {
        console.log("Server Response:", data); // Debugging

        if (data.exists) {
            alert("User already exists");  // ✅ Show only this if user exists
        } else {
            alert("Account created successfully");  
            window.location.href = "/login";  // ✅ Redirect only on success
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("User already exists");  // ✅ Default to this on any failure
    });
}

// ✅ Prevent page reload by using an event listener
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("registerButton").addEventListener("click", registerEmployee);
});




function moveto_employeecont() {
    const joinsection2 = document.getElementById("joinussect2");
    const joinsection3 = document.getElementById("joinus-sect3");

    joinsection3.style.display = "block";
    joinsection2.style.display = "none";
}

function moveto_joinsect2(){
    const joinsection2 = document.getElementById("joinussect2");
    const joinsection3 = document.getElementById("joinus-sect3");

    joinsection3.classList.add("joinus-sect2contdisp");
    joinsection2.classList.remove("joinus-sect2contdisp");
}


function submitJob() {
    // Get values by ID
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let job_description = document.getElementById("job_description").value.trim();
    let job_salary = document.getElementById("jobsalary").value.trim();
    let job_title = document.getElementById("job_title").value.trim();
    let source = document.getElementById("source").value;

    // Validation check
    if (!name || !email || !job_salary || !job_title || !phone || !job_description || source === "How did you find us?") {
        alert("All fields are required!");
        return;
    }

    // Create data object
    let formData = {
        name: name,
        email: email,
        phone: phone,
        job_title: job_title,
        job_salary: job_salary,
        job_description: job_description,
        source: source
    };

    // Send data to Flask route
    fetch('/submit-job', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Show success or error message
        if (data.message === "Job posted successfully!") {
            document.getElementById("jobForm").reset(); // Clear the form
        }
    })
    .catch(error => console.error('Error:', error));
}
