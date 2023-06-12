/*******************
  1. window.name  
*******************/ 

var dog = window.name
document.getElementById('displayArea').innerHTML = dog

var dog = window.name
function displayMessage(a,b,c) {
  document.getElementById('displayArea').innerHTML = b;
}
displayMessage('l',dog,'k')

var dog = window.name
document.getElementById('displayArea').outerHTML = dog

var dog = window.name
function displayMessage(a,b,c) {
  document.getElementById('displayArea').outerHTML = b;
}
displayMessage('l',dog,'k')

/*******************
  2. location.hash  
*******************/ 

