

let selectUserName = document.getElementById('user-field')
let inputUserName1 = document.getElementById('input-user-name1')
let inputUserName2 = document.getElementById('input-user-name2')
let inputUserName3 = document.getElementById('input-user-name3')


selectUserName.addEventListener('change', () => {

    let selectedValue = selectUserName.value
    // console.log(selectedValue)
    inputUserName1.value = inputUserName2.value = inputUserName3.value = selectedValue
})

let closeButtoon = document.getElementById('closeOrder')

closeButtoon.addEventListener('click', () => {

    Toastify({

        text: "La orden esta siendo cerrada. Aguarde",
        duration: 6000,
        gravity: "top",
        position: "center",
        stopOnFocus: false, // Prevents dismissing of toast on hover
        style: {
            background: "#5c0c19",
            background: "linear-gradient(90deg, rgba(92, 12, 25, 1) 0%, rgba(198, 12, 48, 1) 100%)",
            // background: "linear-gradient(to right, #00b06dff, #028646ff)",
        },

    }).showToast();
})