var dog = window.name

function displayMessage(a) {
  document.getElementById('displayArea').innerHTML = a;
  document.getElementById('displayArea').outerHTML = a;
}

// document.getElementById('displayArea').innerHTML = dog;
// document.getElementById('displayArea').outerHTML = dog;
displayMessage(dog)