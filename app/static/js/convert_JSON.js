document.getElementById('auth_form').addEventListener('submit', submitForm);
//document.getElementById('reg_form').addEventListener('submit', submitForm);


async function submitForm(event) {

    event.preventDefault(); // Decline the browser's default form submission behavior

    let formData = new FormData(event.target); // event.target — HTML element <form>

    // Gathering form data into an object
    let obj = {};
    formData.forEach((value, key) => {
        obj[key] = value;
    });

    // Constructing the server request
    let request = new Request(event.target.action, {
        method: "POST",
        body: JSON.stringify(obj),
        headers: {
            "Content-Type": "application/json"
        }
    });

    let response = await fetch(request);
    let data = await response.json();

    if (data.success) {
        window.location.href = `/profile/${data.username}`;
    } 
    else {
        // change a content of the element with id = error_message
        let errorElement = document.getElementById("error_message");
        errorElement.textContent = data.error; 
    }
}