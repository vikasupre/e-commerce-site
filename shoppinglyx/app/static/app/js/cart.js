const plus = document.querySelector('.plus-cart')
console.log(plus)


plus.addEventListener('click', increase)

function increase() {
    console.log('plus')
    let id = this.getAttribute('pid').toString()
    data={prod_id:id}
    console.log(id)
    const xhr = new XMLHttpRequest();

    xhr.open('GET', '/pluscart?'+'prod_id=id', true)

    xhr.onload = () => {
        if (this.status == 200 && this.readyState == 4) {
            console.log('clicked')
            console.log('clicked')
        } else {
            console.log('error')
        }
    }
    data={prod_id:id}
    xhr.send()
}

