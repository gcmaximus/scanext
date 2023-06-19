/*******************
  1. window.name  
*******************/ 

// case 1
// var dog = window.name
// document.getElementById('displayArea').innerHTML = dog

// case 2
// var dog = window.name
// function displayMessage(a,b,c) {
//   document.getElementById('displayArea').innerHTML = b;
// }
// displayMessage('l',dog,'k')

// case 3
// var button = document.getElementById('buttonId')
// button.addEventListener('click', function CaoNiMa() {
//   document.getElementById('displayArea').innerHTML = dog
// })

// case 3.5
// var button = document.getElementById('buttonId')
// button.addEventListener('click', function CaoNiMa() {
//   console.log('hi')
// })

// case 4
// document.getElementById('buttonId').addEventListener('click', function() {
//   var dog = window.name
//   document.getElementById('displayArea').innerHTML = dog
// })

// case 5
// function displayMessage(a,b,c) {
//   document.getElementById('displayArea').innerHTML = b;
// }
// var dog = window.name
// displayMessage('l',dog,'k')

// case 6
// document.getElementById('buttonId').addEventListener('click', function() {
//   var dog = window.name
//   document.getElementById('displayArea').outerHTML = dog
// })

// case 7
// var dog = window.name
// $("button").click(function(){
//   $("p").html(dog);
// });

// case 8
var dog = window.name
$("button").click(function(){
    $(dog).appendTo("p");
})

/*******************
  2. location.hash  
*******************/ 

