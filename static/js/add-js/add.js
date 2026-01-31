/*VARIABLES A TRABAJAR*/
const add = document.getElementById("add")
const remove = document.getElementById("remove")
const quantity = document.getElementById("quantity")

/*FUNCIONALIDAD DE AGREGAR Y REMOVER*/
add.addEventListener("click", function(){
    quantity.value = parseInt(quantity.value) + 1
})

remove.addEventListener("click", function(){
    value = parseInt(quantity.value)

    if(value !=1){
        value = value - 1
    }
    quantity.value = value
})