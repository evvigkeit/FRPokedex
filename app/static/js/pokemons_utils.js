document.querySelectorAll("form").forEach(form => {   //finds ALL the elements with "form" selectors. For each of them adds event listeners
    form.addEventListener("submit", submitForm)
})

async function submitForm(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const searchParams = new URLSearchParams(formData);

    const response = await fetch(`/pokemons?${searchParams}`);
    const data = await response.json();

    const container = document.querySelector("#container");   // finds the first element of the document with "container" selector
    container.innerHTML = "";

    if (data.pokemons.length == 0) {
        container.innerHTML += `
        <p style="text-align: center; font-weight: 700; font-size: 28px; color: #007060; ">
            Nothing was found :( <br> 
            Please try again!
        </p>`
    }
    else{

        for (let [pokemon, pic] of data.pokemons){
            console.log(pokemon);
            container.innerHTML += `
            <div class=pokemon_card>
                <a href="../pokemons/${pokemon}"><img class=pokemon_pic src="/static/pics/${pic}"></a>
                <p class=pokemon_name>${pokemon}</p>
            </div>
            `
        }         
    };
}


