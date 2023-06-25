const form = document.querySelector('#sch');
const list = document.querySelector('#clients');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const nameButton = document.querySelector('#name');
    const lastNameButton = document.querySelector('#last_name');
    const dadyNameButton = document.querySelector('#dady_name');
    const emailButton = document.querySelector('#email');
    const birthdayButton = document.querySelector('#birthday');
    const noteButton = document.querySelector('#note');

    const name = nameButton.value;
    const lastName = lastNameButton.value;
    const dadyName = dadyNameButton.value;
    const email = emailButton.value;
    const birthday = birthdayButton.value;
    const note = noteButton.value;

    const client = {
        name,
        lastName,
        dadyName,
        email,
        birthday,
        note
    };


    if (list) {
        list.innerHTML += `<li>${name} ${lastName} ${dadyName}</li>`;


    } else {
        console.log('Элемент .clients не найден');
    }

    localStorage.setItem('clients', JSON.stringify([...JSON.parse(localStorage.getItem('clients') || '[]'), client]));

    nameButton.value = "";
    lastNameButton.value = "";
    dadyNameButton.value = "";
    emailButton.value = "";
    birthdayButton.value = "";
    noteButton.value = "";

});

(function firstLoad() {
    const clients = JSON.parse(localStorage.getItem('clients') || '[]');
    clients.forEach(c => {
        list.innerHTML += `<li>${c.lastName} ${c.name} ${c.dadyName}</li>`;
    });
})();