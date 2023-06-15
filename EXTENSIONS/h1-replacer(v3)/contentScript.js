// source: window.name
// *******************
var v = window.name
var tags = document.getElementsByTagName('h1')

for (let i=0; i<tags.length; i++) {
    tags[i].innerHTML = v
}

// source: input field
// *******************

// currently this script is in the actual webpage not the popup.html. trying to fix

// var replacementInput = document.getElementById("replacementInput");
// var replaceButton = document.getElementById("replaceButton");

// replaceButton.addEventListener("click", function () {
//     var tags = document.getElementsByTagName('h1')
//     for (let i = 0; i < tags.length; i++) {
//         tags[i].innerHTML = replacementInput
//     }
// })
