document.querySelector("form").addEventListener("submit", submitForm); // call the function using the first css-selector "form" found as an argument


async function submitForm(event) {

    event.preventDefault(); // Decline the browser's default form submission behavior

    let formData = new FormData(event.target); // event.target — HTML element <form>

     // Gathering form data into an object
    let obj = {};
    formData.forEach((value, key) => {
        if (key == "username") {value = value.toLowerCase()}
        obj[key] = value;
    });

    let request;

    if (event.target.id == "auth_form") {
        request = new Request(event.target.action, {
            method: "POST",
            body: formData
        })  
    }
    else {
    // Constructing the server request
    request = new Request(event.target.action, {
        method: "POST",
        body: JSON.stringify(obj),
        headers: {
            "Content-Type": "application/json"
        }
    });
};
    console.log(request)
    let response = await fetch(request);

    let data = await response.json();

    console.log(data)

    if (response.ok) {
        console.log(obj)
        window.location.href = `/profile/${obj.username}`;
    } 
    else {
        // change a content of the element with id = error_message
        let errorElement = document.getElementById("error_message");
        errorElement.textContent = data.error; 
    }
}