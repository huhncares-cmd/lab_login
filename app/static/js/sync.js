function getAllActivePrograms() {
    let names = []
    document.querySelectorAll(".conf-checkbox").forEach(element => {
        if (element.checked) {
            names.push(element.name)
        }
    })
    return names

}

function updateProgramConfig() {
    document.querySelectorAll(".conf-checkbox").forEach(element => {
        element.checked = false
    })
    
    document.querySelectorAll(".state[value=true]").forEach(element => {
        let program_config = element.id.split(" ")
        let esp = document.querySelector("#esp-selector").value 
        if(program_config[0] == esp) {
            let checkbox = document.querySelector(`input[name="${program_config[1]}"]`)
            checkbox.checked = true
        }
    
    })    
}

document.querySelectorAll(".conf-checkbox").forEach(element => {
    element.addEventListener("change", () => {
        let names = getAllActivePrograms()
        let name_string = ""

        let esp_name = document.querySelector("#esp-selector").value;

        let state_config = document.querySelector(".state-config")
        let states = document.querySelectorAll(".state")
        let found = false
        states.forEach(state => {
            if (state.id == `${esp_name} ${element.name}`) {
                state.setAttribute("value", element.checked)
                found = true
            }
        })
        if(!found) {
            state_config.innerHTML += `<div class="state" value="${element.checked}" id="${esp_name} ${element.name}"></div>`
        }
        for (let i = 0; i < names.length; i++) {
            if (i == names.length - 1) {
                name_string += names[i]
                continue
            }
            name_string += names[i] + "&name="
        }
        
        fetch(`/program_config/update/?esp=${esp_name}&name=${name_string}`)
    })
})

document.querySelector("#esp-selector").addEventListener("change", () => {
    updateProgramConfig()
})

document.querySelector("#start").addEventListener("click", () => {
    let esp_name = document.querySelector("#esp-selector").value;
    fetch(`/workspace/start/?esp=${esp_name}`)
    .then(response => response.json())
    .then(data => {
        if(data["success"]) {
            document.querySelector("#success").innerHTML = data["success"]
            document.querySelector("#error").innerHTML = ""
        } else {
            document.querySelector("#success").innerHTML = ""
            document.querySelector("#error").innerHTML = data["error"]
        }
    })
})


document.querySelector("#stop").addEventListener("click", () => {
    let esp_name = document.querySelector("#esp-selector").value;
    fetch(`/workspace/stop/?esp=${esp_name}`)
    .then(response => response.json())
    .then(data => {
        if(data["success"]) {
            document.querySelector("#success").innerHTML = data["success"]
            document.querySelector("#error").innerHTML = ""
        } else {
            document.querySelector("#success").innerHTML = ""
            document.querySelector("#error").innerHTML = data["error"]
        }
    })
})

updateProgramConfig()