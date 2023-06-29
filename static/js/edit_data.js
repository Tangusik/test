let modal = document.querySelector('.modal');

function edit_data() {
    modal.style.display = 'block';
}

let btn = document.querySelector('.close');

btn.onclick = function () {
    modal.style.display = 'none';
}
