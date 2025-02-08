
let selectUserName = document.getElementById('user-field')
let inputUserName1 = document.getElementById('input-user-name1')
let inputUserName2 = document.getElementById('input-user-name2')
let inputUserName3 = document.getElementById('input-user-name3')

console.log(selectUserName)
console.log(inputUserName1)

selectUserName.addEventListener('change', () =>  {
    
    let selectedValue = selectUserName.value
    console.log(selectedValue)
    inputUserName1.value = inputUserName2.value = inputUserName3.value = selectedValue
})