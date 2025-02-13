let imprimir= document.getElementById('prn-btn')

imprimir.addEventListener('click', () => {
// Get the element to be printed

const section = document.getElementById('order-prn');

const tempElement = document.createElement('div');
tempElement.style.display = 'none';
tempElement.appendChild(section.cloneNode(true));
document.body.appendChild(tempElement);
setTimeout(() => {
    window.print();
    // document.body.removeChild(tempElement);
}, 1000)

})