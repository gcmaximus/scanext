/*******************
  1. window.name  
*******************/ 

// case 1
var case1 = window.name
document.getElementById('displayArea').innerHTML = case1

// case 2
var button = document.getElementById('buttonId')
case2 = window.name
button.addEventListener('click', function CaoNiMa() {
  document.getElementById('displayArea').innerHTML = case2
})

// case 3 (NO RESULTS)
var button = document.getElementById('buttonId')
button.addEventListener('click', function CaoNiMa() {
  console.log('hi')
})

// case 4
document.getElementById('buttonId').addEventListener('click', function() {
  var case4 = window.name
  document.getElementById('displayArea').innerHTML = case4
})

// case 5
function displayMessage(a,b,c) {
  document.getElementById('displayArea').innerHTML = b;
}
var case5 = window.name
displayMessage('l',case5,'k')

// case 6 (NO RESULT)
function displayMessage(a,b,c) {
  document.getElementById('displayArea').innerHTML = b;
}
displayMessage('asas','l','k')

// case 7
function displayMessage(a,b,c) {
  document.getElementById('displayArea').innerHTML = b;
}
displayMessage(window.name,'l','k')

/*******************
  2. location.hash  
*******************/ 

