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
    } else {
        clients.style.display = "none";
    }
}



function showAllGroups() {
    if (groups.style.display === "none") {
        groups.style.display = "block";
        clients.style.display = "none";
                   sports.style.display = "none";
    } else {
        groups.style.display = "none";
    }
}


function showAllSports() {
    if (sports.style.display === "none") {
        sports.style.display = "block";
          groups.style.display = "none";
           clients.style.display = "none";

    } else {
        sports.style.display = "none";
    }
}