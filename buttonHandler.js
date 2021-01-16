var button = document.getElementById("btn");
var form_height= document.getElementsByClassName('form-control-height')[0];

// Disable the button on initial page load
button.disabled = true;

//add button event listener
clickBtn.addEventListener('form-control-height', function(event) {
    button.disabled = !button.disabled;
});

// button.addEventListener('form-control-height', function(event) {
//     alert('Enabled!');
// });