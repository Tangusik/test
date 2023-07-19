function showGroupForm() {
    var form = document.getElementById("form_add_team");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}


function showClientForm() {
    var form = document.getElementById("form_add_client");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}


function showTrainerForm() {
    var form = document.getElementById("form_add_trainer");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}


var clients = document.getElementById("all_clients");
var groups = document.getElementById("all_groups");
var sports = document.getElementById("all_sports");

function showAllClients() {
    if (clients.style.display === "none") {
        clients.style.display = "block";
        groups.style.display = "none";
        sports.style.display = "none";

        let button = document.getElementById("all_clients_btn");
        setActiveButton(button);

    } else {
        clients.style.display = "none";
    }
}


function showAllGroups() {
    if (groups.style.display === "none") {
        groups.style.display = "block";
        clients.style.display = "none";
        sports.style.display = "none";

        let button = document.getElementById("all_groups_btn");
        setActiveButton(button);

    } else {
        groups.style.display = "none";
    }
}


function showAllSports() {
    if (sports.style.display === "none") {
        sports.style.display = "block";
        groups.style.display = "none";
        clients.style.display = "none";

        let button = document.getElementById("all_sports_btn");
        setActiveButton(button);

    } else {
        sports.style.display = "none";
    }
}

function setActiveButton(button) {
    let buttons = document.querySelectorAll(".change_btn");

    buttons.forEach(function (btn) {
        if (btn !== button) {
            btn.classList.remove("active");
        }
    });

    button.classList.add("active");
}

// let trainer_search_div = document.getElementById("search_cards");
// function search_trainers() {
//     if (trainer_search_div.style.display === "none") {
//         trainer_search_div.style.display = "block";
//     } else {
//         trainer_search_div.style.display = "none";
//     }
// }