window.onload = function() {
    let dragTheme = localStorage.getItem('dark'); //get the privious seted value
    let themeCheckBox = document.getElementById('color_mode'); // get the checkbox element
    themeCheckBox.checked = (dragTheme === "true") ? true : false; // set checkbox conditionally base on privious set value if not s
    themeCheckBox.onchange = function myFunction() { // triger when change value of checkbox
        if (themeCheckBox.checked) {
            document.body.setAttribute('dark', '');
            localStorage.setItem('dark', true);
        } else {
            document.body.removeAttribute('dark');
            localStorage.setItem('dark', false);
        }
    }
    themeCheckBox.onchange();
}
