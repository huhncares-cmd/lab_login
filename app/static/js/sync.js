document.querySelectorAll(".states").forEach(element => {
    let program_name = element.innerHTML
    document.querySelectorAll(".conf-checkbox").forEach(checkbox => {
        if (checkbox.name == program_name) {
            checkbox.checked = true
        }
    })
})

document.querySelectorAll(".conf-checkbox").forEach(element => {
    element.addEventListener("change", () => {
        let name = element.name
        let todo_status = element.checked
        
        fetch(`/program_config/update/?name=${name}&state=${todo_status}`)
    })
})