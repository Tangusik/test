var clients = document.getElementById("all_clients");
var groups = document.getElementById("all_groups");
var sports = document.getElementById("all_sports");


function showAllClients() {
  if (clients.classList.contains("hidden")) {
    clients.classList.remove("hidden");
    groups.classList.add("hidden");
    sports.classList.add("hidden");

    let button = document.getElementById("all_clients_btn");
    setActiveButton(button);
  } else {
    clients.classList.add("hidden");
  }
}


function showAllGroups(){
  if (groups.classList.contains("hidden")) {
    groups.classList.remove("hidden");
    clients.classList.add("hidden");
    sports.classList.add("hidden");

    let button = document.getElementById("all_groups_btn");
    setActiveButton(button);
  } else {
    groups.classList.add("hidden");
  }
}


function showAllSports()  {
  if (sports.classList.contains("hidden")) {
    sports.classList.remove("hidden");
    groups.classList.add("hidden");
    clients.classList.add("hidden");

    let button = document.getElementById("all_sports_btn");
    setActiveButton(button);
  } else {
    sports.classList.add("hidden");
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
