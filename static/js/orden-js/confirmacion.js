const form = document.getElementById('formPromo-codigo')

form.addEventListener('submit', function(e) {
    e.preventDefault()
        const input = this.codigo
        const codigo = input.value
        const url = this.action

        fetch(url)
            .then(response => response.json())
            .then(response => {
                console.log(response.id)
            })
})